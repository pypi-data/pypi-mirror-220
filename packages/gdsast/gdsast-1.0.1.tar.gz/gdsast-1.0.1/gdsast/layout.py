from .gdsast import *
from .geoms import Vector2D

def _gds_element_flip_rotate_pt(el, pt):
    if "mag" in el and el["element"] == "sref":
        raise NotImplemented
    flip = "strans" in el and el["strans"]&0x8000 # flipped
    angle = el.get("angle", 0)
    return gds_flip_rotate_pt(pt, flip, angle)

def _gds_element_update_pt(el, pt):
    pt = _gds_element_flip_rotate_pt(el, pt)
    x, y = el["xy"][0]
    return pt[0] + x, pt[1] + y

def _flip_rotate_orient(orient, flip, angle):
    if flip:
        if orient == "N":
            orient = 'S'
        elif orient == 'S':
            orient = 'N'
    if not angle:
        pass
    elif angle == 90:
        orient = {'N':'W','W':'S','S':'E','E':'N'}[orient]
    elif angle == 180:
        orient = {'N':'S','W':'E','S':'N','E':'W'}[orient]
    elif angle == 270:
        orient = {'N':'E','W':'N','S':'W','E':'S'}[orient]
    else:
        assert(False),"Expecting angle be 0, 90, 180 or 270"
    return orient


def _flip_rotate_pins(pins, flip, angle):
    _pins = {}
    for _orient, labs in pins.items():
        _labs = _pins[_flip_rotate_orient(_orient, flip, angle)] = {}
        for label, info in labs.items():
            _info = _labs[label] = {}
            for layer, ptsw in info.items():
                _ptsw = _info[layer] = {(gds_flip_rotate_pt(ptw[0], flip, angle),ptw[1]) for ptw in ptsw}
    return _pins


def _point_inside_geom(_geom, pt):
    v = Vector2D(pt[0], pt[1])
    if _geom["element"] == "boundary":
        return v.inside(_geom["xy"])
    elif _geom["element"] == "path":
        width = _geom["width"]
        def _boundary_pts():
            back = []
            def _ofs(pt1, pt2):
                dv = Vector2D(pt2[0] - pt1[0], pt2[1] - pt1[1]).normal().sized(width / 2)
                dv.x = int(round(dv.x))
                dv.y = int(round(dv.y))
                yield pt1 + dv
                yield pt2 + dv
                back.insert(0, pt1 - dv)
                back.insert(0, pt2 - dv)
            prev = None
            for pt in _geom["xy"]:
                if prev is not None:
                    yield from _ofs(prev, pt)
                prev = pt
            yield from back
        return v.inside(_boundary_pts())

def _box_pts(pts):
    xy = list(zip(*pts))    # -> [[all Xs], [all Ys]]
    if xy:
        yield list(map(min,xy)) # [min of all Xs, min of all Ys]
        yield list(map(max,xy)) # [max of all Xs, max of all Ys]

class GDSLayout:
    def __init__(self):
        self.gds = None # AST
        self.sts = {}   # structures map by name

    def init(self, lib_name, units = None):
        self.sts = {}
        if not units:
            units = [0.001, 1e-9]
        self.gds = gds_create(lib_name, units)

    def u2units(self, microns): # return GDS units from micrometers (1e-9 meters)
        units = self.gds["units"]
        return int(round(units[1] / units[0] / 1e-9 * microns))

    def units2u(self, units): # return microns (1e-9 meters) from GDS units
        _units = self.gds["units"]
        return units * _units[0] / (_units[1] * 1e+9)

    def load_file(self, filename):
        with open(filename,"rb") as f:
            _gds = gds_read(f)
            if self.gds is None:
                self.gds = _gds
                for st in _gds["structures"]:
                    self.sts[st["name"]] = st
            else:
                units = self.gds["units"]
                _units = _gds["units"]
                if units != _units:
                    raise NotImplemented
                for st in _gds["structures"]:
                    name = st["name"]
                    if name in self.sts:
                        # TODO: check is same
                        print(f"GDS is reusing structure '{name}' while loading '{filename}'")
                        continue
                    self.sts[name] = st
                    self.gds["structures"].append(st)

    def get_structure(self, name):
        return self.sts.get(name)

    def new_structure(self, name):
        st = self.get_structure(name)
        if st is not None:
            self.gds["structures"].remove(st)
        st = gds_create_structure(name)
        self.gds["structures"].append(st)
        self.sts[name] = st
        return st

    def rename_structure(self, from_name, to_name):
        if from_name == to_name:
            return
        assert(to_name not in self.sts),f"Can't rename structure '{from_name}' to '{to_name}' as name been used"
        st = self.get_structure(from_name)
        self.sts[from_name]
        st["name"] = to_name
        self.sts[to_name] = st

    @staticmethod
    def _is_el_match(el, filt):
        if not filt:
            return False
        def _match(name, val):
            if name in el:
                if isinstance(val, (set, tuple, list)):
                    return el[name] in val
                else:
                    return el[name] == val
            return False
        if isinstance(filt, dict):
            for name, _filt in filt.items():
                if _match(name, _filt):
                    return True
        else:
            return _match("element", filt)

    def get_structure_geom_points(self, st, ignore = "text"):
        for el in st["elements"]:
            yield from self.get_element_geom_points(el, ignore)

    def get_element_geom_points(self, el, ignore = "text"):
        if not self._is_el_match(el, ignore):
            if el["element"] == "sref":
                if "mag" in el:
                    raise NotImplemented
                x, y = el["xy"][0] # sref position
                for pt in self.get_structure_geom_points(el["name"]):
                    pt = _gds_element_flip_rotate_pt(el, pt)
                    yield pt[0] + x, pt[1] + y
            elif "xy" in el:
                yield from el["xy"]

    def get_structure_geom_box(self, name, ignore = "text"):
        st = self.sts[name]
        def _pts():
            for el in st["elements"]:
                yield from self.get_element_geom_box(el, ignore)
        return list(_box_pts(_pts()))

    def get_element_geom_box(self, el, ignore = "text"):
        def _pts():
            if not self._is_el_match(el, ignore) and "xy" in el:
                xy = el["xy"]
                if el["element"] == "sref":
                    if "mag" in el:
                        raise NotImplemented
                    x, y = xy[0] # sref position
                    for pt in self.get_structure_geom_box(el["name"], ignore):
                        pt = _gds_element_flip_rotate_pt(el, pt)
                        yield pt[0] + x, pt[1] + y
                else:
                    yield from _box_pts(xy)
        return list(_box_pts(_pts()))

    def _ordered_names_with_deps(self, st_names):
        names = set()
        def _srefs(st):
            for el in st["elements"]:
                if el["element"] == "sref":
                    yield el
        def _populate(name):
            names.add(name)
            st = self.get_structure(name)
            assert(st), f"GDS referencing non existing structure '{name}"
            for el in _srefs(st):
                el_name = el["name"]
                if el_name in names:
                    continue
                _populate(el_name)
        for name in st_names:
            _populate(name)
        # dependancy sort
        ordered_names = sorted(names)
        i = 0
        nerr = 0
        while i<len(ordered_names):
            name = ordered_names[i]
            st = self.get_structure(name)
            if any(map(lambda el: el["name"] in  names, _srefs(st))):
                ordered_names.pop(i)
                ordered_names.append(name)
                nerr += 1
                assert(nerr < len(names)), "GDS structures have elements with cross dependancies"
            else:
                names.discard(name)
                i += 1
                nerr = 0
        return ordered_names

    def new_gds(self, lib_name, st_names): # create new GDSLayout with only selected structures
        gds = GDSLayout()
        gds.init(lib_name, self.gds["units"])
        for name in self._ordered_names_with_deps(st_names):
            st = self.get_structure(name)
            gds.gds["structures"].append(st)
        return gds

    def save_structures(self, filename, lib_name, st_names):
        gds = self.new_gds(lib_name, st_names)
        gds.save_file(filename)

    def save_file(self, filename):
        with open(filename, "wb") as f:
            gds_write(f, self.gds)

    def extract_pins(self, cell_name, ignore = None):
        st = self.get_structure(cell_name)
        assert(st),f"Unknown '{cell_name}' cell"
        def _labels(st):
            for el in st["elements"]:
                if el["element"] == "text":
                    yield el["xy"][0], el["layer"], el["text"]
                elif el["element"] == "sref":
                    for pt, layer, text in _labels(self.get_structure(el["name"])):
                        yield _gds_element_update_pt(el, pt), layer, text
        layer2labs = {}
        for pt, layer, label in _labels(st):
            if layer in layer2labs:
                labs = layer2labs[layer]
            else:
                labs = layer2labs[layer] = {}
            if label in labs:
                pts = labs[label]
            else:
                pts = labs[label] = set()
            pts.add(pt)
        pmin, pmax = self.get_structure_geom_box(cell_name, ignore)
        def _update_xy(sref, xy):
            for pt in xy:
                yield _gds_element_update_pt(sref, pt)
        def _geoms(st): # all geometries in the structure
            for el in st["elements"]:
                el_type = el["element"]
                if el_type == "sref":
                    for geom in _geoms(self.get_structure(el["name"])):
                        _geom = geom.copy()
                        _geom["xy"] = list(_update_xy(el, geom["xy"]))
                        yield _geom
                if el_type in ("boundary", "path"):
                    yield el
        def _edge_geoms(): # only geometries that touch edges
            for _geom in _geoms(st):
                for pt in _geom["xy"]:
                    if (pt[0] == pmin[0] or
                        pt[1] == pmin[1] or
                        pt[0] == pmax[0] or
                        pt[1] == pmax[1]):
                        yield _geom
                        break
        def _find_geom_label(_geom):
            layer = _geom["layer"]
            if layer in layer2labs:
                for label, pts in layer2labs[layer].items():
                    for pt in pts:
                        if _point_inside_geom(_geom,pt):
                            return label
        def _labeled_edge_geoms(): # all geometries that have label inside them
            for _geom in _edge_geoms():
                label = _find_geom_label(_geom)
                if label:
                    yield label, _geom
        pins = {} # map chain: orient->label->layer->(pt,width) 
        def _add_pin(orient, label, layer, pt, width):
            if orient in pins:
                side_pins = pins[orient]
            else:
                side_pins = pins[orient] = {}
            key = (label, layer)
            if label in side_pins:
                lmap = side_pins[label]
            else:
                lmap = side_pins[label] = {}
            if layer in lmap:
                pts = lmap[layer]
            else:
                pts = lmap[layer] = set()
            pts.add((pt, width))
        for label, _geom in _labeled_edge_geoms():
            if _geom["element"] == "path":
                width = _geom["width"]
                layer = _geom["layer"]
                for pt in _geom["xy"]:
                    if pt[0] == pmin[0]:
                        _add_pin('W', label, layer, pt, width)
                    elif pt[0] == pmax[0]:
                        _add_pin('E', label, layer, pt, width)
                    elif pt[1] == pmin[1]:
                        _add_pin('S', label, layer, pt, width)
                    elif pt[1] == pmax[1]:
                        _add_pin('N', label, layer, pt, width)
            elif _geom["element"] == "boundary":
                layer = _geom["layer"]
                prev = None
                for pt in _geom["xy"]:
                    if prev is not None:
                        if prev[0] == pt[0]:
                            if pt[0] == pmin[0]:
                                _add_pin('W', label, layer, (pt[0], (prev[1]+pt[1]+1)//2), abs(pt[1] - prev[1]))
                            elif pt[0] == pmax[0]:
                                _add_pin('E', label, layer, (pt[0], (prev[1]+pt[1]+1)//2), abs(pt[1] - prev[1]))
                        elif prev[1] == pt[1]:
                            if pt[1] == pmin[1]:
                                _add_pin('S', label, layer, ((prev[0]+pt[0]+1)//2, pt[1]), abs(pt[0] - prev[0]))
                            elif pt[1] == pmax[1]:
                                _add_pin('N', label, layer, ((prev[0]+pt[0]+1)//2, pt[1]), abs(pt[0] - prev[0]))
                    prev = pt
        return pins  # map chain: orient->label->layer->[(pt,width)] of edge points of labeled geometries

    def _sref_pins(self, sref, pins):
        flip = "strans" in sref and sref["strans"]&0x8000 # flipped
        angle = sref.get("angle", 0)
        return _flip_rotate_pins(pins, flip, angle)

# helper class to work with GDS structure existing or new
class GDSStructure:
    def __init__(self, gds, name):
        self.gds = gds
        st = gds.get_structure(name)
        if st is None:
            st = gds.new_structure(name)
        self.items = st["elements"]
        self.srefs = {}

    def add_sref(self, sref_name, ref_name, flipped, angle):
        assert(ref_name in self.gds.sts),f"Referencing unknown '{ref_name}' structure"
        item = {
            "element" : "sref",
            "name" : ref_name,
#            "sref_name" : sref_name
            "xy" : [(0, 0)]
            }
        if angle or flipped:
            item["strans"] = 0x8000 if flipped else 0
        if angle:
            item["angle"] = float(angle)
        self.items.append(item)
        self.srefs[sref_name] = item
        return item

    def add_path(self, pt1, pt2, width, layer):
        item = {
            "element" : "path",
            "layer": int(layer),
            "datatype": 0,
            "width": int(width),
            "xy" : [tuple(pt1), tuple(pt2)]
            }
        self.items.append(item)
        return item

    def add_rect(self, box, layer):
        def _pts():
            x_min = min(box[0][0], box[1][0])
            x_max = max(box[0][0], box[1][0])
            y_min = min(box[0][1], box[1][1])
            y_max = max(box[0][1], box[1][1])
            yield (x_min, y_min)
            yield (x_max, y_min)
            yield (x_max, y_max)
            yield (x_min, y_max)
            yield (x_min, y_min)
        item = {
            "element" : "boundary",
            "layer": int(layer),
            "datatype": 0,
            "xy" : list(_pts())
            }
        self.items.append(item)
        return item

    #def add_via(self, box, size, layer, spacing = None, nx = None, ny = None, grid = None):
        #if not spacing:
            #spacing = size
        #width = box[1][0] - box[0][0]
        #height = box[1][1] - box[0][1]
        #if not nx:
            #nx = (width - spacing) // (size + spacing)
        #if not ny:
            #ny = (height - spacing) // (size + spacing)
        #xofs = box[0][0] + (width - nx * (size + spacing) + spacing) // 2
        #yofs = box[0][1] + (height - ny * (size + spacing) + spacing) // 2
        #if grid:
            #def _grid_update(v):
                #diff = v % grid
                #if diff *2 < grid:
                    #diff = -diff
                #else:
                    #diff = grid - diff
                #return v + diff
            #xofs = _grid_update(xofs)
            #yofs = _grid_update(yofs)
        ##print(f"VIA: x={xofs} y={yofs} size={size} nx={nx} ny={ny} width={width} height={height}")
        #for j in range(ny):
            #for i in range(nx):
                #x = xofs + i * (size + spacing)
                #y = yofs + j * (size + spacing) + size // 2
                #self.add_path((x, y), (x + size, y), size, layer)
