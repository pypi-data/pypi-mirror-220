import struct
import time
import math

GDS_NO_DATA, GDS_BIT_ARRAY, GDS_INT16, GDS_INT32, GDS_REAL32, GDS_REAL64, GDS_STR = range(7)

def GDS_REC16(rec_id, gds_type):
    return (rec_id<<8)|gds_type

GDS_HEADER       = GDS_REC16(0x00, GDS_INT16)
GDS_BGNLIB       = GDS_REC16(0x01, GDS_INT16)
GDS_LIBNAME      = GDS_REC16(0x02, GDS_STR)
GDS_UNITS        = GDS_REC16(0x03, GDS_REAL64)
GDS_ENDLIB       = GDS_REC16(0x04, GDS_NO_DATA)
GDS_BGNSTR       = GDS_REC16(0x05, GDS_INT16)
GDS_STRNAME      = GDS_REC16(0x06, GDS_STR)
GDS_ENDSTR       = GDS_REC16(0x07, GDS_NO_DATA)
GDS_BOUNDARY     = GDS_REC16(0x08, GDS_NO_DATA)
GDS_PATH         = GDS_REC16(0x09, GDS_NO_DATA)
GDS_SREF         = GDS_REC16(0x0A, GDS_NO_DATA)
GDS_AREF         = GDS_REC16(0x0B, GDS_NO_DATA)
GDS_TEXT         = GDS_REC16(0x0C, GDS_NO_DATA)
GDS_LAYER        = GDS_REC16(0x0D, GDS_INT16)
GDS_DATATYPE     = GDS_REC16(0x0E, GDS_INT16)
GDS_WIDTH        = GDS_REC16(0x0F, GDS_INT32)
GDS_XY           = GDS_REC16(0x10, GDS_INT32)
GDS_ENDEL        = GDS_REC16(0x11, GDS_NO_DATA)
GDS_SNAME        = GDS_REC16(0x12, GDS_STR)
GDS_COLROW       = GDS_REC16(0x13, GDS_INT16)
GDS_TEXTNODE     = GDS_REC16(0x14, GDS_NO_DATA)
GDS_NODE         = GDS_REC16(0x15, GDS_NO_DATA)
GDS_TEXTTYPE     = GDS_REC16(0x16, GDS_INT16)
GDS_PRESENTATION = GDS_REC16(0x17, GDS_BIT_ARRAY)
GDS_STRING       = GDS_REC16(0x19, GDS_STR)
GDS_STRANS       = GDS_REC16(0x1A, GDS_BIT_ARRAY)
GDS_MAG          = GDS_REC16(0x1B, GDS_REAL64)
GDS_ANGLE        = GDS_REC16(0x1C, GDS_REAL64)
GDS_REFLIBS      = GDS_REC16(0x1F, GDS_STR)
GDS_FONTS        = GDS_REC16(0x20, GDS_STR)
GDS_PATHTYPE     = GDS_REC16(0x21, GDS_INT16)
GDS_GENERATIONS  = GDS_REC16(0x22, GDS_INT16)
GDS_ATTRTABLE    = GDS_REC16(0x23, GDS_STR)
GDS_ELFLAGS      = GDS_REC16(0x26, GDS_BIT_ARRAY)
GDS_NODETYPE     = GDS_REC16(0x2A, GDS_INT16)
GDS_PROPATTR     = GDS_REC16(0x2B, GDS_INT16)
GDS_PROPVALUE    = GDS_REC16(0x2C, GDS_STR)
GDS_BOX          = GDS_REC16(0x2D, GDS_NO_DATA)
GDS_BOXTYPE      = GDS_REC16(0x2E, GDS_INT16)
GDS_PLEX         = GDS_REC16(0x2F, GDS_INT32)
GDS_BGNEXTN      = GDS_REC16(0x30, GDS_INT32)
GDS_ENDEXTN      = GDS_REC16(0x31, GDS_INT32)
GDS_TAPENUM      = GDS_REC16(0x32, GDS_INT16)
GDS_TAPECODE     = GDS_REC16(0x33, GDS_INT16)
GDS_STRCLASS     = GDS_REC16(0x34, GDS_BIT_ARRAY)
GDS_FORMAT       = GDS_REC16(0x36, GDS_INT16)
GDS_MASK         = GDS_REC16(0x37, GDS_STR)
GDS_ENDMASKS     = GDS_REC16(0x38, GDS_NO_DATA)

GDS_VALID_TAGS = {
    GDS_HEADER,
    GDS_BGNLIB,
    GDS_LIBNAME,
    GDS_UNITS,
    GDS_ENDLIB,
    GDS_BGNSTR,
    GDS_STRNAME,
    GDS_ENDSTR,
    GDS_BOUNDARY,
    GDS_PATH,
    GDS_SREF,
    GDS_AREF,
    GDS_TEXT,
    GDS_LAYER,
    GDS_DATATYPE,
    GDS_WIDTH,
    GDS_XY,
    GDS_ENDEL,
    GDS_SNAME,
    GDS_COLROW,
    GDS_TEXTNODE,
    GDS_NODE,
    GDS_TEXTTYPE,
    GDS_PRESENTATION,
    GDS_STRING,
    GDS_STRANS,
    GDS_MAG,
    GDS_ANGLE,
    GDS_REFLIBS,
    GDS_FONTS,
    GDS_PATHTYPE,
    GDS_GENERATIONS,
    GDS_ATTRTABLE,
    GDS_ELFLAGS,
    GDS_NODETYPE,
    GDS_PROPATTR,
    GDS_PROPVALUE,
    GDS_BOX,
    GDS_BOXTYPE,
    GDS_PLEX,
    GDS_BGNEXTN,
    GDS_ENDEXTN,
    GDS_TAPENUM,
    GDS_TAPECODE,
    GDS_STRCLASS,
    GDS_FORMAT,
    GDS_MASK,
    GDS_ENDMASKS,
    }

def _gds_unpack_no_data(data):
    return None

def _gds_pack_no_data(v):
    return b''

def _gds_unpack_bit_array(data):
    return data

def _gds_pack_bit_array(v):
    return v

def _gds_unpack_int16(data):
    nums = list(map(lambda v: v[0],struct.iter_unpack(">h",data)))
    if len(nums)==1:
        return nums[0]
    return nums

def _gds_pack_int16(v):
    if isinstance(v,int):
        return struct.pack('>h',v)
    data = b''
    for _v in v:
        data += struct.pack('>h',_v)
    return data

def _gds_unpack_uint16(data):
    nums = list(map(lambda v: v[0],struct.iter_unpack(">H",data)))
    if len(nums)==1:
        return nums[0]
    return nums

def _gds_pack_uint16(v):
    if isinstance(v,int):
        return struct.pack('>H',v)
    data = b''
    for _v in v:
        data += struct.pack('>H',_v)
    return data

def _gds_unpack_int32(data):
    nums = list(map(lambda v: v[0],struct.iter_unpack(">i",data)))
    if len(nums)==1:
        return nums[0]
    return nums

def _gds_pack_int32(v):
    if isinstance(v,int):
        return struct.pack('>i',v)
    data = b''
    for _v in v:
        data += struct.pack('>i',_v)
    return data

def _gds_unpack_real32(data):
    assert((len(data)&3)==0),"Expecting multiple of 4 bytes data"
    def _nums():
        for i in range(0,len(data),4):
            b1 = data[i]
            v32 = struct.unpack(">I",b'\0'+data[i+1:i+4])[0]
            v = math.ldexp(v32, ((b1&0x7F)*4)-280)
            if b1 & 0x80:
                yield -v
            else:
                yield v
    nums = list(_nums())
    if len(nums)==1:
        return nums[0]
    return nums

def _gds_pack_real32(v):
    def _pack(_v):
        if _v<0:
            b1 = 0x80
            _v = -_v
        else:
            b1 = 0
        m, exp = math.frexp(_v)
        m = int(m * math.pow(2, 24))
        exp -= 24
        while exp&3:
            exp += 1
            m >>= 1
        exp = (exp + 280)>>2
        data = struct.pack('>I', m)
        return struct.pack('B', b1|(exp&0x7F))+data[1:]
    if isinstance(v, (int, str)):
        v = float(v)
    if isinstance(v, float):
        return _pack(v)
    data = b''
    for _v in v:
        data += _pack(_v)
    raise data

def _gds_unpack_real64(data):
    assert((len(data)&7)==0),"Expecting multiple of 8 bytes data"
    def _nums():
        for i in range(0,len(data),8):
            b1 = data[i]
            v64 = struct.unpack(">Q",b'\0'+data[i+1:i+8])[0]
            v = math.ldexp(v64, ((b1&0x7F)*4)-312)
            if b1 & 0x80:
                yield -v
            else:
                yield v
    nums = list(_nums())
    if len(nums)==1:
        return nums[0]
    return nums

def _gds_pack_real64(v):
    def _pack(_v):
        if _v<0:
            b1 = 0x80
            _v = -_v
        else:
            b1 = 0
        m, exp = math.frexp(_v)
        m = int(m * math.pow(2, 56))
        exp -= 56
        while exp&3:
            exp += 1
            m >>= 1
        exp = (exp + 312)>>2
        data = struct.pack('>Q', m)
        return struct.pack('B', b1|(exp&0x7F))+data[1:]
    if isinstance(v, (int, str)):
        v = float(v)
    if isinstance(v, float):
        return _pack(v)
    data = b''
    for _v in v:
        data += _pack(_v)
    return data

def _gds_unpack_str(data):
    i = data.find(b'\0')
    if i>=0:
        data = data[:i]
    return data.decode('utf-8')

def _gds_pack_str(v):
    if isinstance(v, str):
        data = v.encode('utf-8')
        if len(data)&1:
            data += b'\0'
    else:
        raise NotImplemented
    return data

def _gds_unpack_xy(data):
    def _pts():
        xy = iter(_gds_unpack_int32(data))
        while True:
            try:
                x = next(xy)
                y = next(xy)
                yield (x, y)
            except StopIteration:
                break
    return list(_pts())

def _gds_pack_xy(v):
    def _xy():
        for pt in v:
            yield pt[0]
            yield pt[1]
    return _gds_pack_int32(_xy())

_gds_unpack_map = {
    GDS_NO_DATA   : _gds_unpack_no_data,
    GDS_BIT_ARRAY : _gds_unpack_uint16,
    GDS_INT16     : _gds_unpack_int16,
    GDS_INT32     : _gds_unpack_int32,
    GDS_REAL32    : _gds_unpack_real32,
    GDS_REAL64    : _gds_unpack_real64,
    GDS_STR       : _gds_unpack_str,
    GDS_XY        : _gds_unpack_xy
}

_gds_pack_map = {
    GDS_NO_DATA   : _gds_pack_no_data,
    GDS_BIT_ARRAY : _gds_pack_uint16,
    GDS_INT16     : _gds_pack_int16,
    GDS_INT32     : _gds_pack_int32,
    GDS_REAL32    : _gds_pack_real32,
    GDS_REAL64    : _gds_pack_real64,
    GDS_STR       : _gds_pack_str,
    GDS_XY        : _gds_pack_xy
}

def _gds_unpack_data(rec_id, data):
    unpack_proc = _gds_unpack_map.get(rec_id)
    if unpack_proc is None:
        unpack_proc = _gds_unpack_map[rec_id&0xFF]
    return unpack_proc(data)

def _gds_pack_data(rec_id, value):
    pack_proc = _gds_pack_map.get(rec_id)
    if pack_proc is None:
        pack_proc = _gds_pack_map[rec_id&0xFF]
    return pack_proc(value)

GDS_OPTIONAL   = 0x800000
GDS_NON_TOKEN  = 0x010000
GDS_ARRAY      = 0x020000
GDS_INCLUDE    = 0x040000
GDS_CHOICE     = 0x080000
GDS_TAGMASK    = 0x01FFFF
GDS_NONTAGMASK = 0xFF0000
GDS_LIBRARY       =  0|GDS_NON_TOKEN
GDS_FORMATTYPE    =  1|GDS_NON_TOKEN
GDS_STRUCTURE     =  2|GDS_NON_TOKEN
GDS_MASKS         =  3|GDS_NON_TOKEN
GDS_ELEMENT       =  4|GDS_NON_TOKEN
GDS_PROPERTY      =  5|GDS_NON_TOKEN
GDS_BOUNDARY_ELEM =  6|GDS_NON_TOKEN
GDS_PATH_ELEM     =  7|GDS_NON_TOKEN
GDS_SREF_ELEM     =  8|GDS_NON_TOKEN
GDS_AREF_ELEM     =  9|GDS_NON_TOKEN
GDS_TEXT_ELEM     = 10|GDS_NON_TOKEN
GDS_NODE_ELEM     = 11|GDS_NON_TOKEN
GDS_BOX_ELEM      = 12|GDS_NON_TOKEN
GDS_STRANS_GROUP  = 13|GDS_NON_TOKEN
GDS_TEXTBODY      = 14|GDS_NON_TOKEN

_gds_parse_schema = {
    GDS_LIBRARY: [
        (GDS_HEADER,"version"),
        (GDS_BGNLIB,"timestamp"),
        (GDS_LIBNAME,'name'),
        (GDS_REFLIBS|GDS_OPTIONAL,"reflibs"),
        (GDS_FONTS|GDS_OPTIONAL,"fonts"),
        (GDS_ATTRTABLE|GDS_OPTIONAL,"attributes"),
        #(GDS_STYPTABLE|GDS_OPTIONAL,""),
        (GDS_GENERATIONS|GDS_OPTIONAL,"gens"),
        (GDS_FORMATTYPE|GDS_OPTIONAL,"format_type"),
        (GDS_UNITS,"units"),
        (GDS_STRUCTURE|GDS_OPTIONAL|GDS_ARRAY,"structures"),
        (GDS_ENDLIB,None)
        ],
    GDS_FORMATTYPE: [
        (GDS_FORMAT,"format"),
        (GDS_MASKS|GDS_INCLUDE|GDS_OPTIONAL,None),
        ],
    GDS_MASKS: [
        (GDS_MASK|GDS_ARRAY,"masks"),
        (GDS_ENDMASKS,None)
        ],
    GDS_STRUCTURE: [
        (GDS_BGNSTR,"timestamp"),
        (GDS_STRNAME,"name"),
        (GDS_STRCLASS|GDS_OPTIONAL,"class"),
        #(GDS_STRTYPE|GDS_OPTIONAL,"type"),
        (GDS_ELEMENT|GDS_ARRAY|GDS_OPTIONAL,"elements"),
        (GDS_ENDSTR,None)
        ],
    GDS_ELEMENT: [
        (GDS_CHOICE, [
            GDS_BOUNDARY_ELEM,
            GDS_PATH_ELEM,
            GDS_SREF_ELEM,
            GDS_AREF_ELEM,
            GDS_TEXT_ELEM,
            GDS_NODE_ELEM,
            GDS_BOX_ELEM]),
        #(GDS_ELKEY|GDS_OPTIONAL,"key"),
        (GDS_PROPERTY|GDS_OPTIONAL|GDS_ARRAY,"properties"),
        (GDS_ENDEL,None)
        ],
    GDS_BOUNDARY_ELEM: [
        (GDS_BOUNDARY,{"element": "boundary"}),
        (GDS_ELFLAGS|GDS_OPTIONAL,"flags"),
        (GDS_PLEX|GDS_OPTIONAL,"plex"),
        (GDS_LAYER,"layer"),
        (GDS_DATATYPE,"datatype"),
        (GDS_XY,"xy")
        ],
    GDS_PATH_ELEM: [
        (GDS_PATH,{"element": "path"}),
        (GDS_ELFLAGS|GDS_OPTIONAL,"flags"),
        (GDS_PLEX|GDS_OPTIONAL,"plex"),
        (GDS_LAYER,"layer"),
        (GDS_DATATYPE,"datatype"),
        (GDS_PATHTYPE|GDS_OPTIONAL,"pathtype"),
        (GDS_WIDTH|GDS_OPTIONAL,"width"),
        (GDS_BGNEXTN|GDS_OPTIONAL,"begin_ext"),
        (GDS_ENDEXTN|GDS_OPTIONAL,"end_ext"),
        (GDS_XY,"xy")
        ],
    GDS_SREF_ELEM: [
        (GDS_SREF,{"element": "sref"}),
        (GDS_ELFLAGS|GDS_OPTIONAL,"flags"),
        (GDS_PLEX|GDS_OPTIONAL,"plex"),
        (GDS_SNAME,"name"),
        (GDS_STRANS_GROUP|GDS_OPTIONAL|GDS_INCLUDE,None),
        (GDS_XY,"xy")
        ],
    GDS_AREF_ELEM: [
        (GDS_AREF,{"element": "aref"}),
        (GDS_ELFLAGS|GDS_OPTIONAL,"flags"),
        (GDS_PLEX|GDS_OPTIONAL,"plex"),
        (GDS_SNAME,"name"),
        (GDS_STRANS_GROUP|GDS_OPTIONAL|GDS_INCLUDE,None),
        (GDS_COLROW,"colrow"),
        (GDS_XY,"xy")
        ],
    GDS_TEXT_ELEM: [
        (GDS_TEXT,{"element": "text"}),
        (GDS_ELFLAGS|GDS_OPTIONAL,"flags"),
        (GDS_PLEX|GDS_OPTIONAL,"plex"),
        (GDS_LAYER,"layer"),
        (GDS_TEXTBODY|GDS_INCLUDE,None)
        ],
    GDS_NODE_ELEM: [
        (GDS_NODE,{"element": "node"}),
        (GDS_ELFLAGS|GDS_OPTIONAL,"flags"),
        (GDS_PLEX|GDS_OPTIONAL,"plex"),
        (GDS_LAYER,"layer"),
        (GDS_NODETYPE,"type"),
        (GDS_XY,"xy")
        ],
    GDS_BOX_ELEM: [
        (GDS_BOX,{"element": "box"}),
        (GDS_ELFLAGS|GDS_OPTIONAL,"flags"),
        (GDS_PLEX|GDS_OPTIONAL,"plex"),
        (GDS_LAYER,"layer"),
        (GDS_BOXTYPE,"type"),
        (GDS_XY,"xy")
        ],
    GDS_STRANS_GROUP: [
        (GDS_STRANS,"strans"),
        (GDS_MAG|GDS_OPTIONAL,"mag"),
        (GDS_ANGLE|GDS_OPTIONAL,"angle"),
        ],
    GDS_TEXTBODY: [
        (GDS_TEXTTYPE,"type"),
        (GDS_PRESENTATION|GDS_OPTIONAL,"presentation"),
        (GDS_PATHTYPE|GDS_OPTIONAL,"pathtype"),
        (GDS_WIDTH|GDS_OPTIONAL,"width"),
        (GDS_STRANS_GROUP|GDS_OPTIONAL|GDS_INCLUDE,None),
        (GDS_XY,"xy"),
        (GDS_STRING,"text")
        ],
    GDS_PROPERTY: [
        (GDS_PROPATTR,"name"),
        (GDS_PROPVALUE,"value")
        ]
}

def gds_read(stream):
    def _gds_read_stream():
        while True:
            hdr = stream.read(4)
            if not hdr:
                break
            size, rec_id = struct.unpack(">HH", hdr)
            assert(rec_id in GDS_VALID_TAGS), f"Unknown GDS record encountered {hex(rec_id)}"
            data = stream.read(size - 4)
            yield rec_id, _gds_unpack_data(rec_id, data)
            if rec_id == GDS_ENDLIB:
                break
    rec_iter = iter(_gds_read_stream())
    rec_id, rec_val = (None, None)
    def _next_rec():
        nonlocal rec_id, rec_val
        try:
            rec_id, rec_val = next(rec_iter)
        except StopIteration:
            rec_id, rec_val = (None, None)
    _next_rec()
    def _try_tag(tag):
        if tag&GDS_NON_TOKEN:
            res = {}
            for _tag, name in _gds_parse_schema[tag]:
                if _tag == GDS_CHOICE:
                    v = None
                    for _tag in name:
                        v = _try_tag(_tag)
                        if v is not None:
                            _tag |= GDS_INCLUDE
                            break
                    name = None
                elif _tag&GDS_ARRAY:
                    v = list(_try_tag_array(_tag&GDS_TAGMASK))
                    if not v:
                        v = None
                else:
                    v = _try_tag(_tag&GDS_TAGMASK)
                if v is None:
                    if _tag&GDS_OPTIONAL:
                        continue
                    return None
                if _tag&GDS_INCLUDE:
                    res.update(v)
                elif name is not None:
                    if isinstance(name, str):
                        res[name] = v
                    else:
                        res.update(name)
            return res
        else:
            if rec_id == tag:
                v = rec_val
                _next_rec()
                return {} if v is None else v
    def _try_tag_array(tag):
        while True:
            v = _try_tag(tag)
            if v is None:
                break
            yield v
    return _try_tag(GDS_LIBRARY)

def gds_write(stream, gds):
    def _tag_val_match(tag, v):
        assert(tag in _gds_parse_schema),f"Wrong choice {hex(tag)} element in GDS schema"
        for _tag, name in _gds_parse_schema[tag]:
            if isinstance(name, str):
                if name in v:
                    continue
                if _tag&GDS_OPTIONAL:
                    continue
            elif isinstance(name, dict):
                for nm, _v in name.items():
                    if nm not in v or v[nm] != _v:
                        return False
        return True
    def _write_tag(tag, v):
        if tag&GDS_NON_TOKEN:
            for _tag, name in _gds_parse_schema[tag]:
                ok = False
                if _tag == GDS_CHOICE:
                    for _tag in name:
                        if _tag_val_match(_tag, v):
                            #print("match:",hex(_tag),v)
                            if _write_tag(_tag, v):
                                ok = True
                                break
                    assert(ok),f"GDS tree has wrong data for element {hex(tag)}: {v}"
                elif _tag&GDS_ARRAY:
                    if name in v:
                        for _v in v[name]:
                            if not _write_tag(_tag&GDS_TAGMASK, _v):
                                assert(False),f"GDS array {hex(_tag)} has wrong item value: {_v}"
                        ok = True
                elif _tag&GDS_INCLUDE:
                    ok =  _write_tag(_tag&GDS_TAGMASK, v)
                elif _tag&0xFF == GDS_NO_DATA:
                    ok =  _write_tag(_tag&GDS_TAGMASK, None)
                elif name in v:
                    ok =  _write_tag(_tag&GDS_TAGMASK, v[name])
                if not ok:
                    if _tag&GDS_OPTIONAL:
                        continue
                    return False
        else:
            data = _gds_pack_data(tag, v)
            hdr = struct.pack(">HH", len(data)+4, tag)
            stream.write(hdr)
            stream.write(data)
        return True
    return _write_tag(GDS_LIBRARY, gds)

def gds_new_timestamp():
    tm = list(time.localtime()[:6])
    return tm+tm

def gds_create(lib_name, units = None):
    if not units:
        units = [0.001, 1e-09]
    return {"version": 5,
            "timestamp": gds_new_timestamp(),
            "name": lib_name,
            "units": units,
            "structures": []
           }

def gds_find_structure(gds, name):
    for st in gds["structures"]:
        if st["name"] == name:
            return st

def gds_get_structures(gds):
    return {st["name"]:st for st in gds["structures"]}

def gds_get_structures_names(gds):
    return [st["name"] for st in gds["structures"]]

def gds_create_structure(name):
    return {"timestamp": gds_new_timestamp(),
            "name": name,
            "elements": []}

def gds_flip_rotate_pt(pt, flip, angle):
    if flip:
        pt = (pt[0], -pt[1])
    if not angle:
        return pt
    elif angle == 90:
        return (-pt[1], pt[0])
    elif angle == 180:
        return (-pt[0], -pt[1])
    elif angle == 270:
        return (pt[1], -pt[0])
    angle = math.radians(angle)
    sn = math.sin(angle)
    cs = math.cos(angle)
    return (int(pt[0]*cs - pt[1]*sn), int(pt[0]*sn + pt[1]*cs))


def gds_get_structures_names_with_deps(gds, st_names):
    names = set()
    def _srefs(st):
        for el in st["elements"]:
            if el["element"] == "sref":
                yield el
    def _populate(name):
        names.add(name)
        st = gds_find_structure(gds, name)
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
        st = gds_find_structure(gds, name)
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
