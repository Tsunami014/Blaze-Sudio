import math
from typing import Union, Iterable
Number = Union[int, float]
pointLike = Union['Point', Iterable[Number]]
AVERYLARGENUMBER = 100000

def rotate(origin, point, angle):
    """
    Rotate a point clockwise by a given angle around a given origin.
    The angle should be given in degrees.
    """
    angle = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    ydiff = (point[1] - origin[1])
    xdiff = (point[0] - origin[0])
    
    qx = origin[0] + cos * xdiff - sin * ydiff
    qy = origin[1] + sin * xdiff + cos * ydiff
    return qx, qy

class Shape:
    # This class always collides; so *can* be used as an infinite plane, but why?
    
    def collides(self, othershape: Union['Shape','Shapes',Iterable['Shape']]):
        if isinstance(othershape, Shape):
            return self._collides(othershape)
        for s in othershape:
            if s._collides(self):
                return True
        return False
    
    def whereCollides(self, othershape: Union['Shape','Shapes',Iterable['Shape']]) -> Iterable[pointLike]:
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
    
    def _where(self, othershape: 'Shape') -> Iterable[Iterable[Number]]:
        return []
    
    def closestPointTo(self, othershape: 'Shape') -> Iterable[Number]:
        return [0, 0]
    
    def tangent(self, point: pointLike, accel: pointLike) -> Number:
        return (math.degrees(math.atan2(accel[1], accel[0]))-180) % 360
    
    def rect(self) -> Iterable[Number]:
        return -float('inf'), -float('inf'), float('inf'), float('inf')
    
    def handleCollisionsPos(self, oldP: 'Shape', newP: 'Shape', objs: Union['Shapes',Iterable['Shape']], accel: pointLike = [0,0]) -> tuple['Shape', pointLike]:
        return newP, accel
    
    def handleCollisionsAccel(self, accel: pointLike, objs: Union['Shapes',Iterable['Shape']]) -> tuple['Shape', pointLike]:
        return self, accel
    
    def copy(self) -> 'Shape':
        return Shape()
    
    def __getitem__(self) -> None:
        pass

    def __setitem__(self) -> None:
        pass
    
    def __str__(self):
        return '<Shape>'

class Shapes:
    def __init__(self, *shapes: Shape):
        self.shapes = list(shapes)
    
    def add_shape(self, shape: Shape) -> None:
        self.shapes.append(shape)
    
    def add_shapes(self, *shapes: Iterable[Shape]) -> None:
        self.shapes.extend(list(shapes))
    
    def remove_shape(self, shape: Shape) -> None:
        self.shapes.remove(shape)
    
    def remove_shapes(self, *shapes: Iterable[Shape]) -> None:
        for s in shapes:
            self.shapes.remove(s)
    
    def collides(self, shapes: Union[Shape,'Shapes',Iterable[Shape]]) -> bool:
        for s in self.shapes:
            if s.collides(shapes):
                return True
        return False

    def whereCollides(self, shapes: Union[Shape,'Shapes',Iterable[Shape]]) -> Iterable[pointLike]:
        points = []
        for s in self.shapes:
            points.extend(s.whereCollides(shapes))
        return points
    
    def closestPointTo(self, othershape: Shape) -> Iterable[pointLike]:
        points = []
        for s in self.shapes:
            points.append(s.closestPointTo(othershape))
        return points
    
    def tangent(self, point: pointLike, accel: pointLike) -> pointLike:
        points = []
        for s in self.shapes:
            points.append(s.tangent(point, accel))
        return points
    
    # TODO: handleCollisions
    
    def copy(self) -> 'Shapes':
        return Shapes(s.copy() for s in self.shapes)
    
    def copy_leave_shapes(self) -> 'Shapes':
        return Shapes(*self.shapes)
    
    def __iter__(self):
        return iter(self.shapes)
    
    def __getitem__(self, index: Number) -> Union[Shape,'Shapes']:
        return self.shapes[index]
    
    def __setitem__(self, index: Number, new: Union[Shape,'Shapes']) -> None:
        self.shapes[index] = new
    
    def __repr__(self): return str(self)
    
    def __str__(self):
        return f'<Shapes with {len(self.shapes)} shapes>'

# The below are in order of collision:
# Each defines how it collides if it hits anything below it, and calls the other object for collisions above.
# Also each is in order of complexity.

class Point(Shape):
    def __init__(self, x: Number, y: Number):
        self.x, self.y = x, y
    
    def rect(self) -> Iterable[Number]:
        return self.x, self.y, self.x, self.y
    
    def _collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return self.x == othershape.x and self.y == othershape.y
        return othershape._collides(self)
    
    def _where(self, othershape: Shape) -> Iterable[pointLike]:
        if isinstance(othershape, Point):
            return [[self.x, self.y]] if (self.x == othershape.x and self.y == othershape.y) else []
        return othershape._where(self)
    
    def closestPointTo(self, othershape: Shape) -> pointLike:
        return (self.x, self.y)
    
    def getTuple(self) -> tuple[Number]:
        return (self.x, self.y)
    
    def handleCollisionsPos(self, oldPoint: Union['Point',pointLike], newPoint: Union['Point',pointLike], objs: Union[Shapes,Iterable[Shape]], accel: pointLike = [0,0], replaceSelf: bool = True) -> tuple['Point', pointLike]:
        mvement = Line(oldPoint, newPoint)
        if not mvement.collides(objs):
            if isinstance(newPoint, Point):
                return newPoint, accel
            return newPoint, accel
        points = []
        for o in objs:
            cs = o.whereCollides(mvement)
            points.extend(list(zip(cs, [o for _ in range(len(cs))])))
        # Don't let you move when you're in a wall
        if points == []:
            if isinstance(oldPoint, Point):
                return oldPoint, [0, 0]
            return Point(*oldPoint), [0, 0]
        points.sort(key=lambda x: abs(x[0][0]-oldPoint[0])**2+abs(x[0][1]-oldPoint[1])**2)
        closestP = points[0][0]
        closestObj = points[0][1]
        t = closestObj.tangent(closestP, accel)
        normal = t-90
        dist_left = math.sqrt(abs(newPoint[0]-closestP[0])**2+abs(newPoint[1]-closestP[1])**2)
        x, y = newPoint[0] - closestP[0], newPoint[1] - closestP[1]
        phi = math.degrees(math.atan2(y, x))-90
        diff = (phi-normal) % 360
        if diff > 180:
            diff = diff - 360
        pos = rotate(closestP, [closestP[0], closestP[1]+dist_left], phi-180-diff*2)
        accel = list(rotate([0, 0], accel, 180-diff*2))
        # HACK
        smallness = rotate([0,0], [0,dist_left/AVERYLARGENUMBER], phi-180-diff*2)
        out, outaccel = self.handleCollisionsPos((closestP[0]+smallness[0], closestP[1]+smallness[1]), pos, objs, accel, False)
        if replaceSelf:
            self.x, self.y = out[0], out[1]
        return out, outaccel

    def handleCollisionsAccel(self, accel: pointLike, objs: Union[Shapes,Iterable[Shape]], replaceSelf: bool = True) -> tuple['Point', pointLike]:
        out, outaccel = self.handleCollisionsPos(self, (self.x+accel[0], self.y+accel[1]), objs, accel, False)
        if replaceSelf:
            self.x, self.y = out[0], out[1]
        return out, outaccel

    def copy(self) -> 'Point':
        return Point(self.x, self.y)

    def __getitem__(self, item: Number) -> Number:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError(
                'List index out of range! Must be 0-1, found: '+str(item)
            )
    
    def __setitem__(self, item: Number, new: Number) -> None:
        if item == 0:
            self.x = new
        elif item == 1:
            self.y = new
        else:
            raise IndexError(
                'List index out of range! Must be 0-1, found: '+str(item)
            )
    
    def __str__(self):
        return f'<Point @ ({self.x}, {self.y})>'

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
    
    def rect(self) -> Iterable[Number]:
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
    
    def _where(self, othershape: Shape) -> Iterable[pointLike]:
        if isinstance(othershape, Point):
            return [[othershape.x, othershape.y]] if self.collides(othershape) else []
        if isinstance(othershape, Line):
            if not self.collides(othershape):
                return []
            # This finds where the lines are colliding if they are infinite, which is why we check if they collide first
            def line(p1, p2):
                A = (p1[1] - p2[1])
                B = (p2[0] - p1[0])
                C = (p1[0]*p2[1] - p2[0]*p1[1])
                return A, B, -C
            L1, L2 = line(self.p1, self.p2), line(othershape.p1, othershape.p2)
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
    
    def closestPointTo(self, othershape: Shape) -> pointLike:
        if isinstance(othershape, Point):
            dx, dy = self.p2[0] - self.p1[0], self.p2[1] - self.p1[1]
            det = dx * dx + dy * dy
            a = (dy * (othershape[1] - self.p1[1]) + dx * (othershape[0] - self.p1[0])) / det
            a = min(1, max(0, a))
            return self.p1[0] + a * dx, self.p1[1] + a * dy
        elif isinstance(othershape, Line):
            colls = self.whereCollides(othershape)
            if colls != []:
                return colls[0]
            def calculate(ln, point, recalculate):
                p2 = ln.closestPointTo(Point(*point))
                olineP = point
                if recalculate:
                    olineP = p2
                    p2 = self.closestPointTo(Point(*p2))
                return p2, abs(p2[0]-olineP[0])**2+abs(p2[1]-olineP[1])**2
            tries = [
                calculate(self, othershape.p1, False),
                calculate(self, othershape.p2, False),
                calculate(othershape, self.p1, True),
                calculate(othershape, self.p2, True),
            ]
            tries.sort(key=lambda x: x[1])
            return tries[0][0]
        elif isinstance(othershape, Circle):
            return self.closestPointTo(Point(othershape.x, othershape.y))
        else: # Rects, Rotated rects and polygons
            colls = self.whereCollides(othershape)
            if colls != []:
                return colls[0]
            def calculate(ln, point, recalculate):
                p2 = ln.closestPointTo(Point(*point))
                olineP = point
                if recalculate:
                    olineP = p2
                    p2 = self.closestPointTo(Point(*p2))
                return p2, abs(p2[0]-olineP[0])**2+abs(p2[1]-olineP[1])**2
            tries = [
                calculate(self, p, False) for p in othershape.toPoints()
            ] + [
                calculate(ln, self.p1, True) for ln in othershape.toLines()
            ] + [
                calculate(ln, self.p2, True) for ln in othershape.toLines()
            ]
            tries.sort(key=lambda x: x[1])
            return tries[0][0]
    
    def tangent(self, point: pointLike, accel: pointLike) -> Number:
        def fixangle(angle):
            angle = angle % 360
            if angle > 180:
                angle = angle - 360
            return abs(angle) # Because we don't need to use this for anything else
        toDeg = (math.degrees(math.atan2(accel[1], accel[0]))-180) % 360
        x, y = self.p2[0] - self.p1[0], self.p2[1] - self.p1[1]
        phi = (math.degrees(math.atan2(y, x))-90)
        tries = [fixangle(phi-toDeg), fixangle(phi-toDeg-180)]
        return [(phi-180)%360, phi % 360][tries.index(min(tries))]
    
    def handleCollisionsPos(self, oldLine: 'Line', newLine: 'Line', objs: Union[Shapes,Iterable[Shape]], accel: pointLike = [0,0], replaceSelf: bool = True) -> tuple['Line', pointLike]:
        mvement = Polygon(oldLine.p1, oldLine.p2, newLine.p2, newLine.p1)
        if not mvement.collides(objs):
            return newLine, accel
        points = []
        for o in objs:
            p = o.closestPointTo(oldLine)
            cPoint = oldLine.closestPointTo(Point(*p))
            points.append([p, o, cPoint, abs(p[0]-cPoint[0])**2+abs(p[1]-cPoint[1])**2])
            #points.extend(list(zip(cs, [o for _ in range(len(cs))])))
        # Don't let you move when you're in a wall
        if points == []:
            return oldLine, [0, 0]
        points.sort(key=lambda x: x[3])
        closestP = points[0][0] # Closest point on the OTHER object
        cPoint = points[0][2] # Closest point on THIS line
        closestObj = points[0][1]
        t = closestObj.tangent(closestP, accel)
        normal = t-90
        # The total movement - the distance between the closest point on the other object and the corresponding point on this one
        dist_left = math.sqrt((closestP[0]-cPoint[0])**2 + (closestP[1]-cPoint[1])**2)
        x, y = cPoint[0] - closestP[0], cPoint[1] - closestP[1]
        phi = math.degrees(math.atan2(y, x))-90 # The angle of incidence
        diff = (phi - normal) % 360 # The difference between the angle of incidence and the normal
        if diff > 180:
            diff -= 360
        pos = rotate(closestP, [closestP[0], closestP[1] + dist_left], normal - diff)
        accel = list(rotate([0, 0], accel, 180-diff*2))
        diff2Point = (cPoint[0]-closestP[0], cPoint[1]-closestP[1])
        odiff = (pos[0]-cPoint[0], pos[1]-cPoint[1])
        # HACK
        smallness = rotate([0,0], [0,dist_left/AVERYLARGENUMBER], phi-180-diff*2)
        newp1, newp2 = (oldLine.p1[0]+odiff[0], oldLine.p1[1]+odiff[1]), (oldLine.p2[0]+odiff[0], oldLine.p2[1]+odiff[1])
        out, outaccel = self.handleCollisionsPos(
            Line((oldLine.p1[0]+diff2Point[0]+smallness[0], oldLine.p1[1]+diff2Point[1]+smallness[1]), 
                 (oldLine.p2[0]+diff2Point[0]+smallness[0], oldLine.p2[1]+diff2Point[1]+smallness[1])), 
            Line(newp1, newp2), objs, accel, False)
        if replaceSelf:
            self.p1, self.p2 = out.p1, out.p2
        return out, outaccel

    def handleCollisionsAccel(self, accel: pointLike, objs: Union[Shapes,Iterable[Shape]], replaceSelf: bool = True) -> tuple['Line', pointLike]:
        out, outaccel = self.handleCollisionsPos(self, Line((self.p1[0]+accel[0], self.p1[1]+accel[1]), (self.p2[0]+accel[0], self.p2[1]+accel[1])), objs, accel, False)
        if replaceSelf:
            self.p1, self.p2 = out.p1, out.p2
        return out, outaccel
    
    def copy(self) -> 'Line':
        return Line(self.p1, self.p2)
    
    def __getitem__(self, item: Number) -> pointLike:
        if item == 0:
            return self.p1
        elif item == 1:
            return self.p2
        else:
            raise IndexError(
                'List index out of range! Must be 0-1, found: '+str(item)
            )
    
    def __setitem__(self, item: Number, new: pointLike) -> None:
        if item == 0:
            self.p1 = new
        elif item == 1:
            self.p2 = new
        else:
            raise IndexError(
                'List index out of range! Must be 0-1, found: '+str(item)
            )
    
    def __str__(self):
        return f'<Line from {self.p1} to {self.p2}>'

class Circle(Shape):
    def __init__(self, x: Number, y: Number, r: Number):
        self.x, self.y, self.r = x, y, r
    
    def rect(self) -> Iterable[Number]:
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
    
    def _where(self, othershape: Shape) -> Iterable[pointLike]:
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
    
    def closestPointTo(self, othershape: Shape) -> pointLike:
        if isinstance(othershape, Point):
            x, y = othershape.x - self.x, othershape.y - self.y
            #if abs(x)**2 + abs(y)**2 < self.r**2:
            #    return othershape
            phi = (math.degrees(math.atan2(y, x)) - 90) % 360
            angle = math.radians(phi)
            
            qx = self.x - math.sin(angle) * self.r
            qy = self.y + math.cos(angle) * self.r
            return qx, qy
        elif isinstance(othershape, Line):
            return self.closestPointTo(Point(*othershape.closestPointTo(Point(self.x, self.y))))
        elif isinstance(othershape, Circle):
            return self.closestPointTo(Point(othershape.x, othershape.y))
        else:
            ps = []
            for ln in othershape.toLines():
                ps.append(ln.closestPointTo(self))
            ps.sort(key=lambda x: (x[0]-self.x)**2+(x[1]-self.y)**2)
            return self.closestPointTo(Point(*ps[0]))

    def tangent(self, point: pointLike, accel: pointLike) -> Number:
        if self.x == point[0]:
            return 90
        return math.degrees(math.atan((point[1]-self.y)/(point[0]-self.x))) + (0 if self.x>point[0] else 180)

    def handleCollisionsAccel(self, accel: pointLike, objs: Union[Shapes,Iterable[Shape]], replaceSelf: bool = True) -> tuple['Circle', pointLike]:
        out, outaccel = self.handleCollisionsPos(self, (self.x+accel[0], self.y+accel[1], self.r), objs, accel, False)
        if replaceSelf:
            self.x, self.y = out.x, out.y
        return out, outaccel
    
    def copy(self) -> 'Circle':
        return Circle(self.x, self.y, self.r)
    
    def __getitem__(self, item: Number) -> Number:
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.r
        else:
            raise IndexError(
                'List index out of range! Must be 0-2, found: '+str(item)
            )
    
    def __setitem__(self, item: Number, new: Number) -> None:
        if item == 0:
            self.x = new
        elif item == 1:
            self.y = new
        elif item == 2:
            self.r = new
        else:
            raise IndexError(
                'List index out of range! Must be 0-2, found: '+str(item)
            )

    def __str__(self):
        return f'<Circle @ ({self.x}, {self.y}) with radius {self.r}>'

class ClosedShape(Shape): # I.e. rect, polygon, etc.
    def _where(self, othershape: Shape) -> Iterable[pointLike]:
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
    
    def tangent(self, point: pointLike, accel: pointLike) -> Number:
        p = Point(*point)
        ps = [[i.closestPointTo(p), i] for i in self.toLines()]
        origps = [[pt[1].tangent(pt[0], accel), pt[0]] for pt in ps]
        ps = origps.copy()
        ps.sort(key=lambda x: abs(x[1][0]-point[0])**2+abs(x[1][1]-point[1])**2)
        if ps[0][1] == ps[1][1]:
            def degrees_to_vector(angle):
                # Convert an angle to a unit vector
                radians = math.radians(angle)
                return math.cos(radians), math.sin(radians)

            # Convert both angles to vectors
            x1, y1 = degrees_to_vector(ps[0][0])
            x2, y2 = degrees_to_vector(ps[1][0])
            
            # Average the x and y components
            avg_x = (x1 + x2) / 2
            avg_y = (y1 + y2) / 2
            return math.degrees(math.atan2(avg_y, avg_x)) % 360
        
        return ps[0][0]
    
    def closestPointTo(self, othershape: Shape) -> pointLike:
        if isinstance(othershape, Point):
            ps = [i.closestPointTo(othershape) for i in self.toLines()]
            ps.sort(key=lambda x: abs(x[0]-othershape[0])**2+abs(x[1]-othershape[1])**2)
            return ps[0]
        elif isinstance(othershape, Line):
            colls = self.whereCollides(othershape)
            if colls != []:
                return colls[0]
            def calculate(ln, oln, recalculate):
                p2 = oln.closestPointTo(ln)
                p = ln.closestPointTo(Point(*p2))
                if recalculate:
                    p3 = oln.closestPointTo(Point(*p))
                    p2 = p
                    p = p3
                return p2, abs(p[0]-p2[0])**2+abs(p[1]-p2[1])**2
            tries = [
                calculate(othershape, p, False) for p in self.toLines()
            ] + [
                calculate(ln, othershape, True) for ln in self.toLines()
            ]
            tries.sort(key=lambda x: x[1])
            return tries[0][0]
        elif isinstance(othershape, Circle):
            return self.closestPointTo(Point(othershape.x, othershape.y))
        else:
            colls = self.whereCollides(othershape)
            if colls != []:
                return colls[0]
            def calculate(ln, point, recalculate):
                p2 = ln.closestPointTo(Point(*point))
                olineP = point
                if recalculate:
                    olineP = p2
                    p2 = self.closestPointTo(Point(*p2))
                return p2, abs(p2[0]-olineP[0])**2+abs(p2[1]-olineP[1])**2
            tries = []
            olns = othershape.toLines()
            slns = self.toLines()
            for ln in slns:
                tries.extend([calculate(ln, oln.p1, False) for oln in olns])
                tries.extend([calculate(ln, oln.p2, False) for oln in olns])
            for oln in olns:
                tries.extend([calculate(oln, ln.p1, True) for ln in slns])
                tries.extend([calculate(oln, ln.p2, True) for ln in slns])
            tries.sort(key=lambda x: x[1])
            return tries[0][0]
    
    def toLines(self):
        return []
    
    def toPoints(self) -> Iterable[pointLike]:
        return []
    
    def __getitem__(self, item: Number) -> pointLike:
        return self.toPoints()[item]

    def __str__(self):
        return '<Closed Shape>'

class Rect(ClosedShape):
    def __init__(self, x: Number, y: Number, w: Number, h: Number):
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def rect(self) -> Iterable[Number]:
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
        return othershape._collides(self)
    
    def toLines(self) -> Iterable[Line]:
        return [
            Line((self.x, self.y), (self.x + self.w, self.y)),
            Line((self.x + self.w, self.y), (self.x + self.w, self.y + self.h)),
            Line((self.x + self.w, self.y + self.h), (self.x, self.y + self.h)),
            Line((self.x, self.y + self.h), (self.x, self.y))
        ]
    
    def toPoints(self) -> Iterable[pointLike]:
        return [
            (self.x, self.y),
            (self.x + self.w, self.y),
            (self.x + self.w, self.y + self.h),
            (self.x, self.y + self.h)
        ]
    
    def copy(self) -> 'Rect':
        return Rect(self.x, self.y, self.w, self.h)
    
    def __setitem__(self, item: Number, new: pointLike) -> None:
        if item == 0:
            self.x, self.y = new[0], new[1]
        elif item == 1:
            self.x, self.y = new[0]-self.w, new[1]
        elif item == 2:
            self.x, self.y = new[0]-self.w, new[1]-self.h
        elif item == 3:
            self.x, self.y = new[0], new[1]-self.h
        else:
            raise IndexError(
                'List index out of range! Must be 0-3, found: '+str(item)
            )
    
    def __str__(self):
        return f'<Rect @ ({self.x}, {self.y}) with dimensions {self.w}x{self.h}>'

class RotatedRect(ClosedShape):
    def __init__(self, x: Number, y: Number, w: Number, h: Number, rotation: Number):
        self.x, self.y, self.w, self.h, self.rot = x, y, w, h, rotation
        self.cachedPoints = []
        self.cacheRequirements = []
    
    def getCache(self) -> Iterable[pointLike]:
        check = [self.w, self.h, self.rot]
        if check != self.cacheRequirements:
            self.cacheRequirements = check
            angle = math.radians(self.rot)
            cos = math.cos(angle)
            sin = math.sin(angle)
            def rot(x, y):
                return cos * x - sin * y, sin * x + cos * y
            self.cache = [
                (0, 0),
                rot(self.w, 0),
                rot(self.w, self.h),
                rot(0, self.h)
            ]
        return [[i[0]+self.x, i[1]+self.y] for i in self.cache]
    
    def rect(self) -> Iterable[Number]:
        ps = self.toPoints()
        return min([i[0] for i in ps]), min([i[1] for i in ps]), max([i[0] for i in ps]), max([i[1] for i in ps])
    
    def _collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            ps = self.toPoints()
            c = False
            j = len(ps) - 1
            for i in range(len(ps)):
                if ((ps[i][1] > othershape.y) != (ps[j][1] > othershape.y)) and \
                (othershape.x < (ps[j][0] - ps[i][0]) * (othershape.y - ps[i][1]) / (ps[j][1] - ps[i][1]) + ps[i][0]):
                    c = not c
                j = i
            return c
        if isinstance(othershape, Line):
            for li in self.toLines():
                if li.collides(othershape):
                    return True
            if self._collides(Point(*othershape.p1)) or self._collides(Point(*othershape.p2)):
                return True
            return False
        if isinstance(othershape, Circle):
            if self._collides(Point(othershape.x, othershape.y)):
                return True
            for li in self.toLines():
                if li.collides(othershape):
                    return True
            return False
        if isinstance(othershape, Rect) or isinstance(othershape, RotatedRect):
            for li in self.toLines():
                if li.collides(othershape):
                    return True
            return othershape.collides(Point(self.x, self.y)) or self.collides(Point(othershape.x, othershape.y))
        return othershape._collides(self)
    
    def toPoints(self) -> Iterable[pointLike]:
        return self.getCache()

    def toLines(self) -> Iterable[Line]:
        ps = self.getCache()
        return [
            Line(ps[i], ps[i+1])
            for i in range(len(ps)-1)
        ] + [Line(ps[len(ps)-1], ps[0])]
    
    def copy(self) -> 'RotatedRect':
        return RotatedRect(self.x, self.y, self.w, self.h, self.rot)
    
    def __setitem__(self, item: Number, new: pointLike) -> None:
        def rot(x, y):
            return rotate([self.x, self.y], [x, y], self.rot)
        if item == 0:
            self.x, self.y = rot(new[0], new[1])
        elif item == 1:
            self.x, self.y = rot(new[0], new[1])
            self.x -= self.w
        elif item == 2:
            self.x, self.y = rot(new[0], new[1])
            self.x -= self.w
            self.y -= self.h
        elif item == 3:
            self.x, self.y = rot(new[0], new[1])
            self.y -= self.h
        else:
            raise IndexError(
                'List index out of range! Must be 0-3, found: '+str(item)
            )
    
    def __str__(self):
        return f'<RotatedRect @ ({self.x}, {self.y}), with dimensions {self.w}x{self.h}, rotated {self.rot}° to have points {self.toPoints()}>'

class Polygon(ClosedShape):
    def __init__(self, *points: pointLike):
        if len(points) < 3:
            raise ValueError(
                f'Cannot have a Polygon with less than 3 points! Found: {len(points)} points!'
            )
        self.points = list(points)
    
    def rect(self) -> Iterable[Number]:
        return min([i[0] for i in self.points]), min([i[1] for i in self.points]), max([i[0] for i in self.points]), max([i[1] for i in self.points])
    
    def _collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            ps = self.points
            c = False
            j = len(ps) - 1
            for i in range(len(ps)):
                if ((ps[i][1] > othershape.y) != (ps[j][1] > othershape.y)) and \
                (othershape.x < (ps[j][0] - ps[i][0]) * (othershape.y - ps[i][1]) / (ps[j][1] - ps[i][1]) + ps[i][0]):
                    c = not c
                j = i
            return c
        if isinstance(othershape, Line):
            for li in self.toLines():
                if li.collides(othershape):
                    return True
            if self._collides(Point(*othershape.p1)) or self._collides(Point(*othershape.p2)):
                return True
            return False
        if isinstance(othershape, Circle):
            if self._collides(Point(othershape.x, othershape.y)):
                return True
            for li in self.toLines():
                if li.collides(othershape):
                    return True
            return False
        if isinstance(othershape, Rect) or isinstance(othershape, RotatedRect):
            for li in self.toLines():
                if li.collides(othershape):
                    return True
            return othershape.collides(Point(self.points[0][0], self.points[0][1])) or self.collides(Point(othershape.x, othershape.y))
        if isinstance(othershape, Polygon):
            for li in self.toLines():
                if li.collides(othershape):
                    return True
            return othershape.collides(Point(self.points[0][0], self.points[0][1])) or self.collides(Point(othershape.points[0][0], othershape.points[0][1]))
        return othershape._collides(self)

    def toLines(self) -> Iterable[Line]:
        return [
            Line(self.points[i], self.points[i+1])
            for i in range(len(self.points)-1)
        ] + [Line(self.points[len(self.points)-1], self.points[0])]
    
    def toPoints(self) -> Iterable[pointLike]:
        return self.points
    
    def copy(self) -> 'Polygon':
        return Polygon(*self.points)
    
    def __setitem__(self, item: Number, new: pointLike) -> None:
        self.points[item] = new
    
    def __str__(self):
        return f'<Polygon with points {self.points}>'

# TODO: Ovals, ovaloids and arcs (Ellipse & capsule)
# TODO: Can also input pointlike, linelike (2 points) and polygon-like iterables into all functions to reduce conversion
# TODO: Bounciness factor for each object
# TODO: Remove constant turning things into Point objects and have the functions able to use tuples instead
# OR EVEN BETTER Have the tuples have a __getitem__ for getting [0] and [1]!!! <--- Genius
# TODO: normals for lines change based off which direction they are coming from
