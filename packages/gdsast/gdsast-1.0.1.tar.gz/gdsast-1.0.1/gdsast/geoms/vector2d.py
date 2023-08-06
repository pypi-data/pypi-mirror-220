import math

pi_half = math.pi / 2

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def dot(self, v):
        return self.x*v.x + self.y*v.y

    def size(self):
        return math.sqrt(self.size2())

    def size2(self):
        return self.x**2 + self.y**2

    def sized(self, sz):
        _sz = self.size()
        return Vector2D(self.x * sz / _sz, self.y * sz / _sz)

    def rotated(self, angle):
        # cos(a+b)=cos(a)*cos(b)-sin(a)*sin(b)
        # sin(a+b)=sin(a)*cos(b)+cos(a)*sin(b)
        v = Vector2D(math.cos(angle), -math.sin(angle))
        return Vector2D(self.dot(v), self.normal().dot(v))

    def normal(self):
        return Vector2D(self.y, -self.x)

    def tangent(self):
        return self.y / self.x

    def angle(self):
        if self.x == 0:
            return -pi_half if self.y <0 else pi_half
        if self.y == 0:
            return math.pi if self.x < 0 else 0
        angle = math.atan(self.tangent())
        if self.x < 0:
            angle += -math.pi if self.y < 0 else math.pi
        return angle

    def winding_angle(self, start, end):
        if start == end:
            return 0
        # cos(A-B)=cos(A)*cos(B)+sin(a)*sin(B)
        # sin(A-B)=sin(A)*cos(B)-cos(a)*sin(B)
        v1 = start - self
        v2 = end - self
        v = Vector2D(v1.dot(v2),v1.dot(v2.normal())) # angle(v)=angle(v2)-angle(v1), size(v)=size(v1)*size(v2)
        return v.angle()

    def __add__(self, v):
        if isinstance(v, Vector2D):
            x = v.x
            y = v.y
        else:
            x, y = v
        return Vector2D(self.x + x, self.y + y)

    def __radd__(self, v):
        return self + v

    def __sub__(self, v):
        if isinstance(v, Vector2D):
            x = v.x
            y = v.y
        else:
            x, y = v
        return Vector2D(self.x - x, self.y - y)

    def __rsub__(self, v):
        if isinstance(v, Vector2D):
            x = v.x
            y = v.y
        else:
            x, y = v
        return Vector2D(x - self.x, y - self.y)

    def inside(self, pts):
        pts = iter(pts)
        pstart = next(pts)
        prev = pstart
        wangle = 0
        while True:
            try:
                pt = next(pts)
                wangle += self.winding_angle(prev, pt)
                prev = pt
            except StopIteration:
                break
        if prev != pstart:
            wangle += self.winding_angle(prev, pstart)
        return abs(wangle) > 0.1 # should be zero (up to accuracy) if outside
