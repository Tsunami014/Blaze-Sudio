import math
from decimal import Decimal # For use whenever we need really precise numbers
from typing import Union
Number = Union[int, float]

def Dec(num: Number) -> Decimal:
    return Decimal(str(num))

class Shape:
    # This class always collides; so *can* be used as an infinite plane, but why?
    
    def collides(self, othershape: Union['Shape','Shapes',list['Shape']]):
        if isinstance(othershape, Shape):
            return self._collides(othershape)
        for s in othershape:
            if s._collides(self):
                return True
        return False
    
    def whereCollides(self, othershape: Union['Shape','Shapes',list['Shape']]) -> list[list[Number]]:
        if isinstance(othershape, Shape):
            return self._where(othershape)
        points = []
        for s in othershape:
            points.extend(s._where(self))
        return points
    
    def check_rects(self, othershape: 'Shape'):
        thisr, otherr = self.rect(), othershape.rect()
        return thisr[0] <= otherr[2] and thisr[2] >= otherr[0] and thisr[1] <= otherr[3] and thisr[3] >= otherr[1]
    
    def __repr__(self): return str(self)
    
    # Replace these
    def _collides(self, othershape: 'Shape') -> bool:
        return True
    
    def _where(self, othershape: 'Shape') -> list[list[Number]]:
        return []
    
    def closestPointTo(self, point: list[Number]) -> list[Number]:
        return point
    
    def tangent(self, point: list[Number]) -> Number:
        return 0
    
    def rect(self) -> list[Number]:
        return -float('inf'), -float('inf'), float('inf'), float('inf')
    
    def copy(self) -> 'Shape':
        return Shape()
    
    def __str__(self):
        return '<Shape>'

class Shapes:
    def __init__(self, *shapes: list[Shape]):
        self.shapes = list(shapes)
    
    def add_shape(self, shape: Shape) -> None:
        self.shapes.append(shape)
    
    def add_shapes(self, *shapes: list[Shape]) -> None:
        self.shapes.extend(list(shapes))
    
    def collides(self, shapes: Union[Shape,'Shapes',list[Shape]]) -> bool:
        for s in self.shapes:
            if s.collides(shapes):
                return True
        return False

    def whereCollides(self, shapes: Union[Shape,'Shapes',list[Shape]]) -> list[list[Number]]:
        points = []
        for s in self.shapes:
            points.extend(s.whereCollides(shapes))
        return points
    
    def closestPointTo(self, point: list[Number]) -> list[list[Number]]:
        points = []
        for s in self.shapes:
            points.append(s.closestPointTo(point))
        return points
    
    def tangent(self, point: list[Number]) -> list[Number]:
        points = []
        for s in self.shapes:
            points.append(s.tangent(point))
        return points
    
    def copy(self) -> 'Shapes':
        return Shapes(s.copy() for s in self.shapes)
    
    def __iter__(self):
        return iter(self.shapes)
    
    def __getitem__(self, index):
        return self.shapes[index]
    
    def __repr__(self): return str(self)
    
    def __str__(self):
        return f'<Shapes with {len(self.shapes)} shapes>'

# The below are in order of collision:
# Each defines how it collides if it hits anything below it, and calls the other object for collisions above.
# Also each is in order of complexity.

class Point(Shape):
    def __init__(self, x: Number, y: Number):
        self.x, self.y = x, y
    
    def rect(self) -> list[Number]:
        return self.x, self.y, self.x, self.y
    
    def _collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return self.x == othershape.x and self.y == othershape.y
        return othershape._collides(self)
    
    def _where(self, othershape: Shape) -> list[list[Number]]:
        if isinstance(othershape, Point):
            return [[self.x, self.y]] if (self.x == othershape.x and self.y == othershape.y) else []
        return othershape._where(self)
    
    def closestPointTo(self, point: list[Number]) -> list[Number]:
        return (self.x, self.y)

    def copy(self) -> 'Point':
        return Point(self.x, self.y)

    def __getitem__(self, item: Number) -> Number|None:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
    
    def __str__(self):
        return f'<Point @ ({self.x}, {self.y})>'

pointLike = Union[Point, list[Number]]

class Line(Shape):
    def __init__(self, p1: pointLike, p2: pointLike):
        self.p1, self.p2 = p1, p2
    
    # Some code yoinked off of https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/ modified for this use case and debugged
    
    @staticmethod
    def _onSegment(p, a, b):
        """
        Given three collinear points p, a, b, the function checks if point p lies on line segment 'ab'
        """
        # Calculate the cross product
        cross_product = (p[1] - a[1]) * (b[0] - a[0]) - (p[0] - a[0]) * (b[1] - a[1])
        
        # If the cross product is not zero, the point is not on the line
        if abs(cross_product) != 0:
            return False
        
        # Check if the point is within the bounding box of the line segment
        return min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    
    def rect(self) -> list[Number]:
        return min(self.p1[0], self.p2[0]), min(self.p1[1], self.p2[1]), max(self.p1[0], self.p2[0]), max(self.p1[1], self.p2[1])
    
    def _collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return self.check_rects(othershape) and self._onSegment([othershape.x, othershape.y], self.p1, self.p2)
        if isinstance(othershape, Line):
            if not self.check_rects(othershape):
                return False
            # Calculate the direction of the lines
            def direction(xi, yi, xj, yj, xk, yk):
                return (xk - xi) * (yj - yi) - (yk - yi) * (xj - xi)
            
            d1 = direction(othershape.p1[0], othershape.p1[1], othershape.p2[0], othershape.p2[1], self.p1[0], self.p1[1])
            d2 = direction(othershape.p1[0], othershape.p1[1], othershape.p2[0], othershape.p2[1], self.p2[0], self.p2[1])
            d3 = direction(self.p1[0], self.p1[1], self.p2[0], self.p2[1], othershape.p1[0], othershape.p1[1])
            d4 = direction(self.p1[0], self.p1[1], self.p2[0], self.p2[1], othershape.p2[0], othershape.p2[1])
            
            # Check if the line segments straddle each other
            if d1 * d2 < 0 and d3 * d4 < 0:
                return True
            
            # Check if the points are collinear and on the segments
            return (d1 == 0 and self._onSegment((self.p1[0], self.p1[1]), (othershape.p1[0], othershape.p1[1]), (othershape.p2[0], othershape.p2[1]))) or \
                   (d2 == 0 and self._onSegment((self.p2[0], self.p2[1]), (othershape.p1[0], othershape.p1[1]), (othershape.p2[0], othershape.p2[1]))) or \
                   (d3 == 0 and self._onSegment((othershape.p1[0], othershape.p1[1]), (self.p1[0], self.p1[1]), (self.p2[0], self.p2[1]))) or \
                   (d4 == 0 and self._onSegment((othershape.p2[0], othershape.p2[1]), (self.p1[0], self.p1[1]), (self.p2[0], self.p2[1])))
        
        return othershape._collides(self)
    
    def _where(self, othershape: Shape) -> list[list[Number]]:
        if isinstance(othershape, Point):
            return [[othershape.x, othershape.y]] if self.collides(othershape) else []
        if isinstance(othershape, Line):
            if not self.collides(othershape):
                return []
            # This finds where the lines are colliding if they are infinite, which is why we check if they collide first
            def toDec(li):
                return [Dec(li[0]), Dec(li[1])]
            def line(p1, p2):
                A = (p1[1] - p2[1])
                B = (p2[0] - p1[0])
                C = (p1[0]*p2[1] - p2[0]*p1[1])
                return A, B, -C
            L1, L2 = line(toDec(self.p1), toDec(self.p2)), line(toDec(othershape.p1), toDec(othershape.p2))
            D  = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return [[float(x),float(y)]]
            else:
                return []
        return othershape._where(self)
    
    def closestPointTo(self, point: list[Number]) -> list[Number]:
        dx, dy = self.p2[0]-self.p1[0], self.p2[1]-self.p1[1]
        det = dx*dx + dy*dy
        a = (dy*(point[1]-self.p1[1])+dx*(point[0]-self.p1[0]))/det
        a = min(1, max(0, a))
        return self.p1[0]+a*dx, self.p1[1]+a*dy
    
    def tangent(self, point: list[Number]) -> Number:
        x, y = self.p2[0] - self.p1[0], self.p2[1] - self.p1[1]
        phi = (math.degrees(math.atan2(y, x))-90) % 360
        return phi
    
    def copy(self) -> 'Line':
        return Line(self.p1, self.p2)
    
    def __str__(self):
        return f'<Line from {self.p1} to {self.p2}>'

class Circle(Shape):
    def __init__(self, x: Number, y: Number, r: Number):
        self.x, self.y, self.r = x, y, r
    
    def rect(self) -> list[Number]:
        return self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r
    
    def _collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return (self.x - othershape.x)**2 + (self.y - othershape.y)**2 < self.r**2
        if isinstance(othershape, Line):
            if not self.check_rects(othershape):
                return False
            # Calculate the distance from point to the line segment
            line_mag = (othershape.p2[0] - othershape.p1[0]) ** 2 + (othershape.p2[1] - othershape.p1[1]) ** 2
            if line_mag == 0:
                return (self.x - othershape.p1[0]) ** 2 + (self.y - othershape.p1[1]) ** 2 <= self.r ** 2
            
            u = ((self.x - othershape.p1[0]) * (othershape.p2[0] - othershape.p1[0]) + (self.y - othershape.p1[1]) * (othershape.p2[1] - othershape.p1[1])) / line_mag
            u = max(min(u, 1), 0)
            ix = othershape.p1[0] + u * (othershape.p2[0] - othershape.p1[0])
            iy = othershape.p1[1] + u * (othershape.p2[1] - othershape.p1[1])
            return (self.x - ix) ** 2 + (self.y - iy) ** 2 <= self.r ** 2
        if isinstance(othershape, Circle):
            return (self.x - othershape.x)**2 + (self.y - othershape.y)**2 < (self.r + othershape.r)**2
        return othershape._collides(self)
    
    def _where(self, othershape: Shape) -> list[list[Number]]:
        if isinstance(othershape, Point):
            return [[othershape.x, othershape.y]] if ((self.x - othershape.x)**2 + (self.y - othershape.y)**2 == self.r**2) else []
        if isinstance(othershape, Line):
            def sign(x):
                return -1 if x < 0 else 1
            x1 = othershape.p1[0] - self.x
            y1 = othershape.p1[1] - self.y
            x2 = othershape.p2[0] - self.x
            y2 = othershape.p2[1] - self.y
            dx = x2 - x1
            dy = y2 - y1
            dr = math.sqrt(dx*dx + dy*dy)
            if dr == 0:
                return self.whereCollides(Point(*othershape.p1))
            D = x1 * y2 - x2 * y1
            discriminant = self.r*self.r*dr*dr - D*D
            if discriminant < 0:
                return []
            if discriminant == 0:
                xa = (D * dy ) /  (dr * dr)
                ya = (-D * dx ) /  (dr * dr)
                ta = (xa-x1)*dx/dr + (ya-y1)*dy/dr
                return [(xa + self.x, ya + self.y)] if 0 < ta < dr else []
            
            xa = (D * dy + sign(dy) * dx * math.sqrt(discriminant)) / (dr * dr)
            ya = (-D * dx + abs(dy) * math.sqrt(discriminant)) / (dr * dr)
            ta = (xa-x1)*dx/dr + (ya-y1)*dy/dr
            xpt = [(xa + self.x, ya + self.y)] if 0 < ta < dr else []
            
            xb = (D * dy - sign(dy) * dx * math.sqrt(discriminant)) / (dr * dr) 
            yb = (-D * dx - abs(dy) * math.sqrt(discriminant)) / (dr * dr)
            tb = (xb-x1)*dx/dr + (yb-y1)*dy/dr
            xpt += [(xb + self.x, yb + self.y)] if 0 < tb < dr else []
            return xpt
        if isinstance(othershape, Circle):
            # circle 1: (x0, y0), radius r0
            # circle 2: (x1, y1), radius r1

            d=math.sqrt((othershape.x-self.x)**2 + (othershape.y-self.y)**2)
            
            # non intersecting
            if d > self.r + othershape.r :
                return []
            # One circle within other
            if d < abs(self.r-othershape.r):
                return []
            # coincident circles
            if d == 0 and self.r == othershape.r:
                return []
            else:
                a=(self.r**2-othershape.r**2+d**2)/(2*d)
                h=math.sqrt(self.r**2-a**2)
                x2=self.x+a*(othershape.x-self.x)/d   
                y2=self.y+a*(othershape.y-self.y)/d   
                x3=x2+h*(othershape.y-self.y)/d     
                y3=y2-h*(othershape.x-self.x)/d 

                x4=x2-h*(othershape.y-self.y)/d
                y4=y2+h*(othershape.x-self.x)/d
                
                return [[x3, y3], [x4, y4]]
        return othershape._where(self)
    
    def closestPointTo(self, point: list[Number]) -> list[Number]:
        if (self.x - point[0])**2 + (self.y - point[1])**2 < self.r**2:
            return point
        x, y = point[0] - self.x, point[1] - self.y
        phi = (math.degrees(math.atan2(y, x)) - 90) % 360
        angle = math.radians(phi)
        
        qx = self.x - math.sin(angle) * self.r
        qy = self.y + math.cos(angle) * self.r
        return qx, qy

    def tangent(self, point: list[Number]) -> Number:
        if self.x == point[0]:
            return 90
        return math.degrees(math.atan((point[1]-self.y)/(point[0]-self.x))) + (0 if self.x>point[0] else 180)
    
    def copy(self) -> 'Circle':
        return Circle(self.x, self.y, self.r)

    def __str__(self):
        return f'<Circle @ ({self.x}, {self.y}) with radius {self.r}>'

class Rect(Shape):
    def __init__(self, x: Number, y: Number, w: Number, h: Number, offset: pointLike = [0,0]):
        self.offset = offset
        self.x, self.y, self.w, self.h = x+self.offset[0], y+self.offset[1], w, h
    
    @property
    def realPos(self) -> tuple[Number]:
        return self.x - self.offset[0], self.y - self.offset[1]
    
    def rect(self) -> list[Number]:
        return self.x, self.y, self.x + self.w, self.y + self.h
    
    def _collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return self.x <= othershape.x and self.x + self.w >= othershape.x and self.y <= othershape.y and self.y + self.h >= othershape.y
        if isinstance(othershape, Line):
            return self.check_rects(othershape) and (
                   (self.x < othershape.p1[0] and self.x + self.w > othershape.p1[0] and self.y < othershape.p1[1] and self.y + self.h > othershape.p1[1]) or \
                   (self.x < othershape.p2[0] and self.x + self.w > othershape.p2[0] and self.y < othershape.p2[1] and self.y + self.h > othershape.p2[1]) or \
                   any([i.collides(othershape) for i in self.toLines()])
            )
        if isinstance(othershape, Circle):
            return self.check_rects(othershape) and (
                   (self.x - othershape.r < othershape.x and self.x + self.w + othershape.r > othershape.x and self.y < othershape.y and self.y + self.h > othershape.y) or \
                   (self.x < othershape.x and self.x + self.w > othershape.x and self.y - othershape.r < othershape.y and self.y + self.h + othershape.r > othershape.y) or \
                   ((self.x - othershape.x)**2 + (self.y - othershape.y)**2 < othershape.r**2) or \
                   (((self.x + self.w) - othershape.x)**2 + (self.y - othershape.y)**2 < othershape.r**2) or \
                   ((self.x - othershape.x)**2 + ((self.y + self.h) - othershape.y)**2 < othershape.r**2) or \
                   (((self.x + self.w) - othershape.x)**2 + ((self.y + self.h) - othershape.y)**2 < othershape.r**2)
            )
            
        if isinstance(othershape, Rect):
            return self.x <= othershape.x + othershape.w and self.x + self.w >= othershape.x and self.y <= othershape.y + othershape.h and self.y + self.h >= othershape.y
    
    def _where(self, othershape: Shape) -> list[list[Number]]:
        if isinstance(othershape, Point):
            for i in self.toLines():
                if i.collides(othershape):
                    return [[othershape.x, othershape.y]]
            return []
        else:
            points = []
            for i in self.toLines():
                points.extend(i._where(othershape))
            return points
    
    def closestPointTo(self, point: list[Number]) -> list[Number]:
        ps = [i.closestPointTo(point) for i in self.toLines()]
        ps.sort(key=lambda x: abs(x[0]-point[0])**2+abs(x[1]-point[1])**2)
        return ps[0]
    
    def tangent(self, point: list[Number]) -> Number:
        p = Point(*point)
        if Line((self.x, self.y), (self.x + self.w, self.y)).collides(p):
            return 90
        elif Line((self.x + self.w, self.y), (self.x + self.w, self.y + self.h)).collides(p):
            return 180
        elif Line((self.x + self.w, self.y + self.h), (self.x, self.y + self.h)).collides(p):
            return -90
        elif Line((self.x, self.y + self.h), (self.x, self.y)).collides(p):
            return 0
    
    def toLines(self):
        return [
            Line((self.x, self.y), (self.x + self.w, self.y)),
            Line((self.x + self.w, self.y), (self.x + self.w, self.y + self.h)),
            Line((self.x + self.w, self.y + self.h), (self.x, self.y + self.h)),
            Line((self.x, self.y + self.h), (self.x, self.y))
        ]
    
    def handle_collision(self, othershape: Shape, movement: list[Number]) -> None:
        if isinstance(othershape, Rect):
            if self.collides(othershape):
                if movement[0] > 0: # Moving right; Hit the left side of the wall
                    self.x = othershape.x - self.w
                elif movement[0] < 0: # Moving left; Hit the right side of the wall
                    self.x = othershape.x + othershape.w
                if movement[1] > 0: # Moving down; Hit the top side of the wall
                    self.y = othershape.y - self.h
                elif movement[1] < 0: # Moving up; Hit the bottom side of the wall
                    self.y = othershape.y + othershape.h
        # else:
            # raise NotImplementedError("Cannot handle collision between Box and {}".format(type(othershape)))
    
    def copy(self) -> 'Rect':
        return Rect(self.x, self.y, self.w, self.h, self.offset)
    
    def __str__(self):
        if self.offset != [0,0]:
            offtxt = 'without an offset'
        else:
            offtxt = f'on an offset of {self.offset}, realpos: {self.realPos}'
        return f'<Rect @ ({self.x}, {self.y}) with dimensions {self.w}x{self.h} {offtxt}>'

def rotate(origin, point, angle):
    """
    Rotate a point clockwise by a given angle around a given origin.
    The angle should be given in degrees.
    """
    angle = math.radians(angle)
    ox, oy = origin
    px, py = point
    cos = math.cos(angle)
    sin = math.sin(angle)
    ydiff = (py - oy)
    xdiff = (px - ox)
    
    qx = ox + cos * xdiff - sin * ydiff
    qy = oy + sin * xdiff + cos * ydiff
    return qx, qy

AVERYLARGENUMBER = 100000

def handleCollisionsPos(oldPos: list[Number], newPos: list[Number], objs: Shapes|list[Shape], accel: list[Number] = [0,0]) -> tuple[list[Number], list[Number]]:
    mvement = Line(oldPos, newPos)
    if not mvement.collides(objs):
        return newPos, accel
    points = []
    for o in objs:
        cs = o.whereCollides(mvement)
        points.extend(list(zip(cs, [o for _ in range(len(cs))])))
    # Don't let you move when you're in a wall
    if points == []:
        return oldPos, [0, 0]
    points.sort(key=lambda x: abs(x[0][0]-oldPos[0])**2+abs(x[0][1]-oldPos[1])**2)
    closestP = points[0][0]
    closestObj = points[0][1]
    t = closestObj.tangent(closestP)
    normal = t-90
    dist_left = math.sqrt(abs(newPos[0]-closestP[0])**2+abs(newPos[1]-closestP[1])**2)
    x, y = newPos[0] - closestP[0], newPos[1] - closestP[1]
    phi = math.degrees(math.atan2(y, x))-90
    diff = (phi-normal) % 360
    if diff > 180:
        diff = diff - 360
    pos = rotate(closestP, [closestP[0], closestP[1]+dist_left], phi-180-diff*2)
    accel = list(rotate([0, 0], accel, 180-diff*2))
    # HACK
    smallness = rotate([0,0], [0,dist_left/AVERYLARGENUMBER], phi-180-diff*2)
    return handleCollisionsPos((closestP[0]+smallness[0], closestP[1]+smallness[1]), pos, objs, accel)

def handleCollisionsAccel(pos: list[Number], accel: list[Number], objs: Shapes|list[Shape]) -> tuple[list[Number], list[Number]]:
    newpos = [pos[0]+accel[0], pos[1]+accel[1]]
    return handleCollisionsPos(pos, newpos, objs, accel)

# TODO: Box that isn't straight (Polygons)
# TODO: Ovals and ovaloids (Ellipse)
