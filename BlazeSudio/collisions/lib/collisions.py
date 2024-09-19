import math
from typing import Union, Iterable, Any
Number = Union[int, float]
verboseOutput = Union[Iterable[Any], None]
pointLike = Iterable[Number]
AVERYSMALLNUMBER: Number = 1e-6
BASEPRECISION: Number = 5
BASEBOUNCINESS: Number = 0.7 # The lower the less bouncy, 1 = reflects perfectly (but there will always be rounding imperfections, so it won't be *perfect* perfect)

def rotate(origin: pointLike, point: pointLike, angle: Number) -> pointLike:
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

def rotateBy0(point: pointLike, angle: Number) -> pointLike:
    """
    Rotate a point clockwise by a given angle around the origin.
    The angle should be given in degrees.
    """
    angle = math.radians(angle)
    cos = math.cos(angle)
    sin = math.sin(angle)
    qx = cos * point[0] - sin * point[1]
    qy = sin * point[0] + cos * point[1]
    return qx, qy

def direction(fromPoint: pointLike, toPoint: pointLike) -> Number:
    """
    Finds the direction of `toPoint` from the origin of `fromPoint`
    """
    return math.atan2(toPoint[1]-fromPoint[1], toPoint[0]-fromPoint[0])

def pointOnUnitCircle(angle: Number, strength: Number) -> pointLike:
    return math.cos(angle)*strength, math.sin(angle)*strength

class Shape:
    # This class always collides; so *can* be used as an infinite plane, but why?
    x: Number = 0
    y: Number = 0
    def __init__(self, bounciness: float = BASEBOUNCINESS):
        self.bounciness: Number = bounciness
    
    def collides(self, othershape: Union['Shape','Shapes',Iterable['Shape']]) -> bool:
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
    
    def _where(self, othershape: 'Shape') -> Iterable[pointLike]:
        return []
    
    def closestPointTo(self, othershape: 'Shape', returnAll: bool = False) -> pointLike|Iterable[pointLike]:
        return [0, 0]
    
    def isCorner(self, point: pointLike, precision: Number = BASEPRECISION) -> bool:
        return True
    
    def tangent(self, point: pointLike, accel: pointLike) -> Number:
        return math.degrees(math.atan2(accel[1], accel[0])) % 360
    
    def rect(self) -> Iterable[Number]:
        return -float('inf'), -float('inf'), float('inf'), float('inf')
    
    def handleCollisionsPos(self, oldP: 'Shape', newP: 'Shape', objs: Union['Shapes',Iterable['Shape']], accel: pointLike = [0,0]) -> tuple['Shape', pointLike]:
        return newP, accel
    
    def handleCollisionsAccel(self, accel: pointLike, objs: Union['Shapes',Iterable['Shape']]) -> tuple['Shape', pointLike]:
        return self, accel
    
    def copy(self) -> 'Shape':
        return Shape(self.bounciness)
    
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
    
    def add_shapes(self, *shapes: Union[Shape,'Shapes']) -> None:
        self.shapes.extend(list(shapes))
    
    def remove_shape(self, shape: Shape) -> None:
        self.shapes.remove(shape)
    
    def remove_shapes(self, *shapes: Union[Shape,'Shapes']) -> None:
        for s in shapes:
            self.shapes.remove(s)
    
    def collides(self, shapes: Union[Shape,'Shapes']) -> bool:
        for s in self.shapes:
            if s.collides(shapes):
                return True
        return False

    def whereCollides(self, shapes: Union[Shape,'Shapes']) -> Iterable[pointLike]:
        points = []
        for s in self.shapes:
            points.extend(s.whereCollides(shapes))
        return points
    
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> Iterable[pointLike]:
        points = []
        for s in self.shapes:
            if returnAll:
                points.extend(s.closestPointTo(othershape, True))
            else:
                points.append(s.closestPointTo(othershape, False))
        return points
    
    def isCorner(self, point: pointLike, precision: Number = BASEPRECISION) -> dict[Union[Shape,'Shapes']: bool]:
        cs = {}
        for s in self.shapes:
            cs[s] = s.isCorner(point, precision)
        return cs
    
    def tangent(self, point: pointLike, accel: pointLike) -> pointLike:
        points = []
        for s in self.shapes:
            points.append(s.tangent(point, accel))
        return points
    
    # TODO: handleCollisions

    def rect(self) -> Iterable[Number]:
        rs = [s.rect() for s in self.shapes]
        return min(i[0] for i in rs), min(i[1] for i in rs), max(i[2] for i in rs), max(i[3] for i in rs)
    
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
    def __init__(self, x: Number, y: Number, bounciness: float = BASEBOUNCINESS):
        super().__init__(bounciness)
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
    
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike|Iterable[pointLike]:
        if returnAll:
            return [(self.x, self.y)]
        return (self.x, self.y)
    
    def getTuple(self) -> tuple[Number]:
        return (self.x, self.y)
    
    def handleCollisionsPos(self, oldPoint: Union['Point',pointLike], newPoint: Union['Point',pointLike], objs: Union[Shapes,Iterable[Shape]], accel: pointLike = [0,0], replaceSelf: bool = True, precision: Number = BASEPRECISION) -> tuple['Point', pointLike]:
        # TODO: Check if the objects collide before finding closest point
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
        dist_left = math.sqrt(abs(newPoint[0]-closestP[0])**2+abs(newPoint[1]-closestP[1])**2) * closestObj.bounciness
        x, y = newPoint[0] - closestP[0], newPoint[1] - closestP[1]
        phi = math.degrees(math.atan2(y, x))-90
        diff = (phi-normal) % 360
        if diff > 180:
            diff = diff - 360
        pos = rotate(closestP, [closestP[0], closestP[1]+dist_left], phi-180-diff*2)
        accel = list(rotateBy0(accel, 180-diff*2))
        accel = [accel[0]*closestObj.bounciness, accel[1]*closestObj.bounciness]
        # HACK
        smallness = rotateBy0([0,AVERYSMALLNUMBER], phi-180-diff*2)
        out, outaccel = self.handleCollisionsPos((closestP[0]+smallness[0], closestP[1]+smallness[1]), pos, objs, accel, False, precision)
        if replaceSelf:
            self.x, self.y = out[0], out[1]
        return out, outaccel

    def handleCollisionsAccel(self, accel: pointLike, objs: Union[Shapes,Iterable[Shape]], replaceSelf: bool = True, precision: Number = BASEPRECISION) -> tuple['Point', pointLike]:
        out, outaccel = self.handleCollisionsPos(self, (self.x+accel[0], self.y+accel[1]), objs, accel, False, precision)
        if replaceSelf:
            self.x, self.y = out[0], out[1]
        return out, outaccel

    def copy(self) -> 'Point':
        return Point(self.x, self.y, self.bounciness)

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
    def __init__(self, p1: pointLike, p2: pointLike, bounciness: float = BASEBOUNCINESS):
        super().__init__(bounciness)
        self.p1, self.p2 = p1, p2
    
    @property
    def x(self):
        return self.p1[0]
    @x.setter
    def x(self, value):
        diff = value - self.p1[0]
        self.p1 = [value, self.p1[1]]
        self.p2 = [self.p2[0]+diff, self.p2[1]]
    @property
    def y(self):
        return self.p1[1]
    @y.setter
    def y(self, value):
        diff = value - self.p1[1]
        self.p1 = [self.p1[0], value]
        self.p2 = [self.p2[0], self.p2[1]+diff]
    
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
    
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike|Iterable[pointLike]:
        if isinstance(othershape, Point):
            dx, dy = self.p2[0] - self.p1[0], self.p2[1] - self.p1[1]
            det = dx * dx + dy * dy
            if det == 0:
                return self.p1
            a = (dy * (othershape[1] - self.p1[1]) + dx * (othershape[0] - self.p1[0])) / det
            a = min(1, max(0, a))
            p = (self.p1[0] + a * dx, self.p1[1] + a * dy)
            if returnAll:
                return [p]
            return p
        elif isinstance(othershape, Line):
            colls = self.whereCollides(othershape)
            if colls != []:
                if returnAll:
                    return colls
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
            if returnAll:
                return [i[0] for i in tries]
            return tries[0][0]
        elif isinstance(othershape, Circle):
            return self.closestPointTo(Point(othershape.x, othershape.y), returnAll)
        else: # Rects, Rotated rects and polygons
            colls = self.whereCollides(othershape)
            if colls != []:
                if returnAll:
                    return colls
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
            if returnAll:
                return [i[0] for i in tries]
            return tries[0][0]
    
    def isCorner(self, point: pointLike, precision: Number = BASEPRECISION) -> bool:
        def rountTuple(x):
            return (round(x[0], precision), round(x[1], precision))
        return rountTuple(self.p1) == rountTuple(point) or rountTuple(self.p2) == rountTuple(point)
    
    def tangent(self, point: pointLike, accel: pointLike) -> Number:
        if point == self.p1:
            return math.degrees(math.atan2(self.p2[1] - self.p1[1], self.p2[0] - self.p1[0]))
        elif point == self.p2:
            return math.degrees(math.atan2(self.p1[1] - self.p2[1], self.p1[0] - self.p2[0]))
        def fixangle(angle):
            angle = angle % 360
            if angle > 180:
                angle = angle - 360
            return abs(angle) # Because we don't need to use this for anything else
        toDeg = (math.degrees(math.atan2(accel[1], accel[0]))-180) % 360
        phi = (math.degrees(math.atan2(self.p2[1] - self.p1[1], self.p2[0] - self.p1[0]))-90)
        tries = [fixangle(phi-toDeg), fixangle(phi-toDeg-180)]
        return [(phi-180)%360, phi % 360][tries.index(min(tries))]
    
    def handleCollisionsPos(self, oldLine: 'Line', newLine: 'Line', objs: Union[Shapes,Iterable[Shape]], accel: pointLike = [0,0], replaceSelf: bool = True, precision: Number = BASEPRECISION, verbose: bool = False) -> tuple['Line', pointLike, verboseOutput]:
        # This function's verbose output: [
        # CollisionType?: list[int, ...], ; This is the type of collision that happened, and it includes each type of collision for each sub-collision
        # ]
        oldLine = Line(*sorted([oldLine.p1, oldLine.p2], key=lambda x: x[0]))
        newLine = Line(*sorted([newLine.p1, newLine.p2], key=lambda x: x[0]))
        mvement = Polygon(oldLine.p1, oldLine.p2, newLine.p2, newLine.p1)
        points = []
        hit = False
        for o in objs:
            if o.collides(mvement):
                hit = True
                ps = o.whereCollides(mvement) + [i for i in o.closestPointTo(oldLine, True) if mvement.collides(Point(*i))]
                for p in ps:
                    # The rotation is making sure the line crosses the oldLine
                    cPoint = oldLine.closestPointTo(Line(p, (p[0]-accel[0],p[1]-accel[1])))
                    points.append([p, o, cPoint, abs(p[0]-cPoint[0])**2+abs(p[1]-cPoint[1])**2])
                    #points.extend(list(zip(cs, [o for _ in range(len(cs))])))
        if not hit:
            if verbose:
                return newLine, accel, []
            return newLine, accel
        # Don't let you move when you're in a wall
        if points == []:
            if verbose:
                return oldLine, [0, 0], []
            return oldLine, [0, 0]
        points.sort(key=lambda x: x[3])
        closestP = points[0][0] # Closest point on the OTHER object
        cPoint = points[0][2] # closestP projected onto the oldLine
        closestObj = points[0][1]
        newPoint = newLine.closestPointTo(Line(closestP, (closestP[0]+accel[0],closestP[1]+accel[1]))) # closestP projected onto the newLine

        thisNormal = math.degrees(math.atan2(oldLine[0][1]-oldLine[1][1], oldLine[0][0]-oldLine[1][0]))
        paralell = False
        cLine = None
        thisIsOnP = oldLine.isCorner(cPoint, precision)
        if isinstance(closestObj, Line):
            cLine = closestObj
        elif isinstance(closestObj, ClosedShape):
            colllidingLns = [i for i in closestObj.toLines() if i.collides(Point(*closestP))]
            if colllidingLns != []:
                cLine = colllidingLns[0]
        elif isinstance(closestObj, Circle) and (not thisIsOnP):
            paralell = True
        if cLine is not None:
            sortedOtherLn = Line(*sorted([cLine.p1, cLine.p2], key=lambda x: x[0]))
            otherLnNormal = math.degrees(math.atan2(sortedOtherLn[0][1]-sortedOtherLn[1][1], sortedOtherLn[0][0]-sortedOtherLn[1][0]))
            paralell = abs(otherLnNormal%360 - thisNormal%360) < precision or abs((otherLnNormal-180)%360 - thisNormal%360) < precision
        accelDiff = 180
        if paralell: # Line off line
            collTyp = 3
            # Reflect off the object's normal to the point (but really could be either point; the tangents *should* be the same)
            normal = thisNormal
            phi = math.degrees(math.atan2(newPoint[1] - closestP[1], newPoint[0] - closestP[0]))-90
        else:
            otherIsOnP = closestObj.isCorner(closestP, precision)
            if thisIsOnP and otherIsOnP: # Point off point collision
                collTyp = 0
                # Reflect off the same way as you came in (as if you can land an infintesimally small point on another infintesimally small point anyway)
                normal, phi = 0, 0
            elif thisIsOnP and (not otherIsOnP): # Point off line
                collTyp = 1
                # Reflect off the other object's normal to the point
                normal = closestObj.tangent(closestP, accel)-90
                phi = math.degrees(math.atan2(newPoint[1] - closestP[1], newPoint[0] - closestP[0]))-90 # The angle of incidence
            elif (not thisIsOnP) and otherIsOnP: # Line off point
                collTyp = 2
                # Reflect off this line's normal
                normal = thisNormal-90 # The normal off the line
                phi = math.degrees(math.atan2(closestP[1] - newPoint[1], closestP[0] - newPoint[0]))-90 # The angle of incidence
                accelDiff = 0
            else:
                raise TypeError(
                    'Cannot have a line reflecting off of another line when they aren\'t paralell; something bad must have occured!'
                )
                collTyp = None
                normal, phi = 0, 0

        # the distance between the closest point on the other object and the corresponding point on the newLine
        dist_left = math.sqrt((newPoint[0]-closestP[0])**2 + (newPoint[1]-closestP[1])**2) * closestObj.bounciness
        diff = (phi-normal) % 360 # The difference between the angle of incidence and the normal
        if diff > 180: # Do we even need this?
            diff -= 360
        pos = rotate(closestP, [closestP[0], closestP[1] + dist_left], phi-180-diff*2)
        accel = list(rotateBy0(accel, accelDiff-diff*2))
        accel = [accel[0]*closestObj.bounciness, accel[1]*closestObj.bounciness]
        diff2Point = (closestP[0]-cPoint[0], closestP[1]-cPoint[1])
        odiff = (pos[0]-cPoint[0], pos[1]-cPoint[1])
        # HACK
        smallness = rotateBy0([0, AVERYSMALLNUMBER], phi-180-diff*2)
        newp1, newp2 = (oldLine.p1[0]+odiff[0], oldLine.p1[1]+odiff[1]), (oldLine.p2[0]+odiff[0], oldLine.p2[1]+odiff[1])
        o = self.handleCollisionsPos(
            Line((oldLine.p1[0]+diff2Point[0]+smallness[0], oldLine.p1[1]+diff2Point[1]+smallness[1]), 
                 (oldLine.p2[0]+diff2Point[0]+smallness[0], oldLine.p2[1]+diff2Point[1]+smallness[1])), 
            Line(newp1, newp2), objs, accel, False, precision, verbose)
        out, outaccel = o[0], o[1]
        if replaceSelf:
            self.p1, self.p2 = out.p1, out.p2
        if verbose:
            return out, outaccel, [collTyp, *o[2]]
        return out, outaccel

    def handleCollisionsAccel(self, accel: pointLike, objs: Union[Shapes,Iterable[Shape]], replaceSelf: bool = True, precision: Number = BASEPRECISION, verbose: bool = False) -> tuple['Line', pointLike, verboseOutput]:
        o = self.handleCollisionsPos(self, Line((self.p1[0]+accel[0], self.p1[1]+accel[1]), (self.p2[0]+accel[0], self.p2[1]+accel[1])), objs, accel, False, precision, verbose)
        out, outaccel = o[0], o[1]
        if replaceSelf:
            self.p1, self.p2 = out.p1, out.p2
        if verbose:
            return out, outaccel, o[2]
        return out, outaccel
    
    def copy(self) -> 'Line':
        return Line(self.p1, self.p2, self.bounciness)
    
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
    def __init__(self, x: Number, y: Number, r: Number, bounciness: float = BASEBOUNCINESS):
        super().__init__(bounciness)
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
            if not self.check_rects(othershape):
                return []
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
            if not self.check_rects(othershape):
                return []
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
    
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike|Iterable[pointLike]:
        if isinstance(othershape, Point):
            x, y = othershape.x - self.x, othershape.y - self.y
            #if abs(x)**2 + abs(y)**2 < self.r**2:
            #    return othershape
            phi = (math.degrees(math.atan2(y, x)) - 90) % 360
            angle = math.radians(phi)
            
            qx = self.x - math.sin(angle) * self.r
            qy = self.y + math.cos(angle) * self.r
            if returnAll:
                return [[qx, qy]]
            return qx, qy
        elif isinstance(othershape, Line):
            return self.closestPointTo(Point(*othershape.closestPointTo(Point(self.x, self.y))), returnAll)
        elif isinstance(othershape, Circle):
            return self.closestPointTo(Point(othershape.x, othershape.y), returnAll)
        else:
            ps = []
            for ln in othershape.toLines():
                ps.append(ln.closestPointTo(self))
            ps.sort(key=lambda x: (x[0]-self.x)**2+(x[1]-self.y)**2)
            if returnAll:
                return [self.closestPointTo(Point(*p)) for p in ps]
            return self.closestPointTo(Point(*ps[0]))
    
    def isCorner(self, point: pointLike, precision: Number = BASEPRECISION) -> bool:
        return False

    def tangent(self, point: pointLike, accel: pointLike) -> Number:
        if self.x == point[0]:
            return 90
        return math.degrees(math.atan((point[1]-self.y)/(point[0]-self.x))) + (0 if self.x>point[0] else 180)

    def copy(self) -> 'Circle':
        return Circle(self.x, self.y, self.r, self.bounciness)
    
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
        if not self.check_rects(othershape):
            return []
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
        # TODO: Make it so the line normals go in the direction facing away from the centre instead of away from the velocity vector 
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
    
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike|Iterable[pointLike]:
        if isinstance(othershape, Point):
            ps = [i.closestPointTo(othershape) for i in self.toLines()]
            ps.sort(key=lambda x: abs(x[0]-othershape[0])**2+abs(x[1]-othershape[1])**2)
            if returnAll:
                return [ps]
            return ps[0]
        elif isinstance(othershape, Line):
            colls = self.whereCollides(othershape)
            if colls != []:
                if returnAll:
                    return colls
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
            if returnAll:
                return [i[0] for i in tries]
            return tries[0][0]
        elif isinstance(othershape, Circle):
            return self.closestPointTo(Point(othershape.x, othershape.y), returnAll)
        else:
            colls = self.whereCollides(othershape)
            if colls != []:
                if returnAll:
                    return colls
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
            if returnAll:
                return [i[0] for i in tries]
            return tries[0][0]
    
    def handleCollisionsPos(self, oldShp: 'ClosedShape', newShp: 'ClosedShape', objs: Union[Shapes,Iterable[Shape]], accel: pointLike = [0,0], replaceSelf: bool = True, precision: Number = BASEPRECISION, verbose: bool = False) -> tuple['ClosedShape', pointLike, verboseOutput]:
        # This function's verbose output: [
        # CollisionType?: list[int, ...], ; This is the type of collision that happened, and it includes each type of collision for each sub-collision
        # ]
        # Don't let you move when you're in a wall, but if you are leaving a wall then GET THE HELLA OUTTA THERE
        if oldShp.collides(objs):
            if newShp.collides(objs):
                if verbose:
                    return oldShp, [0, 0], []
                return oldShp, [0, 0]
            else:
                if verbose:
                    return newShp, accel, []
                return newShp, accel
        points = []
        hit = False
        for oldLine, newLine in zip(oldShp.toLines(), newShp.toLines()):
            oldLine = Line(*sorted([oldLine.p1, oldLine.p2], key=lambda x: x[0]))
            newLine = Line(*sorted([newLine.p1, newLine.p2], key=lambda x: x[0]))
            mvement = Polygon(oldLine.p1, oldLine.p2, newLine.p2, newLine.p1)
            for o in objs:
                if o.collides(mvement):
                    hit = True
                    ps = o.whereCollides(mvement) + [i for i in o.closestPointTo(oldLine, True) if mvement.collides(Point(*i))]
                    for p in ps:
                        if oldShp.collides(Point(*p)):
                            continue
                        # The rotation is making sure the line crosses the oldLine
                        cPoint = oldLine.closestPointTo(Line(p, (p[0]-accel[0],p[1]-accel[1])))
                        pdists = (oldLine.p1[0]-p[0])**2+(oldLine.p1[1]-p[1])**2 + (oldLine.p2[0]-p[0])**2+(oldLine.p2[1]-p[1])**2
                        points.append([p, o, cPoint, round((p[0]-cPoint[0])**2+(p[1]-cPoint[1])**2, precision), round(pdists, precision), oldLine, newLine])
                        #points.extend(list(zip(cs, [o for _ in range(len(cs))])))
        if not hit:
            if verbose:
                return newShp, accel, []
            return newShp, accel
        # Don't let you move when you're in a wall
        if points == []:
            if verbose:
                return oldShp, [0, 0], []
            return oldShp, [0, 0]
        
        points.sort(key=lambda x: (x[3], x[4]))
        oldLine, newLine = points[0][5], points[0][6]
        closestP = points[0][0] # Closest point on the OTHER object
        cPoint = points[0][2] # closestP projected onto the oldLine
        closestObj = points[0][1]
        newPoint = newLine.closestPointTo(Line(closestP, (closestP[0]+accel[0],closestP[1]+accel[1]))) # closestP projected onto the newLine

        thisNormal = math.degrees(math.atan2(oldLine[0][1]-oldLine[1][1], oldLine[0][0]-oldLine[1][0]))
        paralell = False
        cLines = []
        thisIsOnP = oldLine.isCorner(cPoint, precision)
        if isinstance(closestObj, Line):
            cLines = [closestObj]
        elif isinstance(closestObj, ClosedShape):
            cLines = [i for i in closestObj.toLines() if i.collides(Point(*closestP))]
        elif isinstance(closestObj, Circle) and (not thisIsOnP):
            paralell = True
        if cLines != []:
            for cLine in cLines:
                sortedOtherLn = Line(*sorted([cLine.p1, cLine.p2], key=lambda x: x[0]))
                otherLnNormal = math.degrees(math.atan2(sortedOtherLn[0][1]-sortedOtherLn[1][1], sortedOtherLn[0][0]-sortedOtherLn[1][0]))
                paralell = abs(otherLnNormal%360 - thisNormal%360) < precision or abs((otherLnNormal-180)%360 - thisNormal%360) < precision
                if paralell:
                    break
        accelDiff = 180
        if paralell: # Line off line
            collTyp = 3
            # Reflect off the object's normal to the point (but really could be either point; the tangents *should* be the same)
            normal = thisNormal
            phi = math.degrees(math.atan2(newPoint[1] - closestP[1], newPoint[0] - closestP[0]))-90
        else:
            otherIsOnP = closestObj.isCorner(closestP, precision)
            if thisIsOnP and otherIsOnP: # Point off point collision
                collTyp = 0
                # Reflect off the same way as you came in (as if you can land an infintesimally small point on another infintesimally small point anyway)
                normal, phi = 0, 0
            elif thisIsOnP and (not otherIsOnP): # Point off line
                collTyp = 1
                # Reflect off the other object's normal to the point
                normal = closestObj.tangent(closestP, accel)-90
                phi = math.degrees(math.atan2(newPoint[1] - closestP[1], newPoint[0] - closestP[0]))-90 # The angle of incidence
            elif (not thisIsOnP) and otherIsOnP: # Line off point
                collTyp = 2
                # Reflect off this line's normal
                normal = thisNormal-90 # The normal off the line
                phi = math.degrees(math.atan2(closestP[1] - newPoint[1], closestP[0] - newPoint[0]))-90 # The angle of incidence
                accelDiff = 0
            else:
                raise TypeError(
                    'Cannot have a line reflecting off of another line when they aren\'t paralell; something bad must have occured!'
                )
                collTyp = None
                normal, phi = 0, 0

        # the distance between the closest point on the other object and the corresponding point on the newLine
        dist_left = math.sqrt((newPoint[0]-closestP[0])**2 + (newPoint[1]-closestP[1])**2) * closestObj.bounciness
        diff = (phi-normal) % 360 # The difference between the angle of incidence and the normal
        if diff > 180: # Do we even need this?
            diff -= 360
        pos = rotate(closestP, [closestP[0], closestP[1] + dist_left], phi-180-diff*2)
        accel = list(rotateBy0(accel, accelDiff-diff*2))
        accel = [accel[0]*closestObj.bounciness, accel[1]*closestObj.bounciness]
        diff2Point = (closestP[0]-cPoint[0], closestP[1]-cPoint[1])
        odiff = (pos[0]-cPoint[0], pos[1]-cPoint[1])
        # HACK
        smallness = rotateBy0([0, AVERYSMALLNUMBER], phi-180-diff*2)
        newshp = [(i[0]+odiff[0], i[1]+odiff[1]) for i in oldShp.toPoints()]
        o = self.handleCollisionsPos(
            Polygon(*[(i[0]+diff2Point[0]+smallness[0], i[1]+diff2Point[1]+smallness[1]) for i in oldShp.toPoints()]), 
            Polygon(*newshp), objs, accel, False, precision, verbose)
        out, outaccel = o[0], o[1]
        if replaceSelf:
            self.x, self.y = out.x, out.y
        if verbose:
            return out, outaccel, [collTyp, *o[2]]
        return out, outaccel

    def handleCollisionsAccel(self, accel: pointLike, objs: Union[Shapes,Iterable[Shape]], replaceSelf: bool = True, precision: Number = BASEPRECISION, verbose: bool = False) -> tuple['ClosedShape', pointLike, verboseOutput]:
        n = self.copy()
        n.x, n.y = n.x+accel[0], n.y+accel[1]
        o = self.handleCollisionsPos(self, n, objs, accel, False, precision, verbose)
        out, outaccel = o[0], o[1]
        if replaceSelf:
            self.x, self.y = out.x, out.y
        if verbose:
            return out, outaccel, o[2]
        return out, outaccel
    
    def isCorner(self, point: pointLike, precision: Number = BASEPRECISION) -> bool:
        for i in self.toPoints():
            if round(i[0], precision) == round(point[0], precision) and round(i[1], precision) == round(point[1], precision):
                return True
        return False
    
    def toLines(self):
        return []
    
    def toPoints(self) -> Iterable[pointLike]:
        return []
    
    def __getitem__(self, item: Number) -> pointLike:
        return self.toPoints()[item]

    def __str__(self):
        return '<Closed Shape>'

class Rect(ClosedShape):
    def __init__(self, x: Number, y: Number, w: Number, h: Number, bounciness: float = BASEBOUNCINESS):
        super().__init__(bounciness)
        self.x, self.y, self.w, self.h = x, y, w, h
    
    def rect(self) -> Iterable[Number]:
        return min(self.x, self.x + self.w), min(self.y, self.y + self.h), max(self.x, self.x + self.w), max(self.y, self.y + self.h)
    
    def _collides(self, othershape: Shape) -> bool:
        x, y, mx, my = self.rect()
        if isinstance(othershape, Point):
            return x <= othershape.x <= mx and y <= othershape.y and my >= othershape.y
        if isinstance(othershape, Line):
            return self.check_rects(othershape) and (
                   (x < othershape.p1[0] and mx > othershape.p1[0] and y < othershape.p1[1] and my > othershape.p1[1]) or \
                   (x < othershape.p2[0] and mx > othershape.p2[0] and y < othershape.p2[1] and my > othershape.p2[1]) or \
                   any([i.collides(othershape) for i in self.toLines()])
            )
        if isinstance(othershape, Circle):
            return self.check_rects(othershape) and (
                   (x - othershape.r < othershape.x and mx + othershape.r > othershape.x and y < othershape.y and my > othershape.y) or \
                   (x < othershape.x and mx > othershape.x and y - othershape.r < othershape.y and my + othershape.r > othershape.y) or \
                   ((x - othershape.x)**2 + (y - othershape.y)**2 < othershape.r**2) or \
                   (((mx) - othershape.x)**2 + (y - othershape.y)**2 < othershape.r**2) or \
                   ((x - othershape.x)**2 + ((my) - othershape.y)**2 < othershape.r**2) or \
                   (((mx) - othershape.x)**2 + ((my) - othershape.y)**2 < othershape.r**2)
            )
        if isinstance(othershape, Rect):
            ox, oy, omx, omy = othershape.rect()
            return x <= omx and mx >= ox and y <= omy and my >= oy
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
            [self.x, self.y],
            [self.x + self.w, self.y],
            [self.x + self.w, self.y + self.h],
            [self.x, self.y + self.h]
        ]
    
    def copy(self) -> 'Rect':
        return Rect(self.x, self.y, self.w, self.h, self.bounciness)
    
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

class RotatedRect(ClosedShape): # TODO: Fix movement physics on a rotated rect
    def __init__(self, x: Number, y: Number, w: Number, h: Number, rotation: Number, bounciness: float = BASEBOUNCINESS):
        super().__init__(bounciness)
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
        if not self.check_rects(othershape):
            return False
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
        return RotatedRect(self.x, self.y, self.w, self.h, self.rot, self.bounciness)
    
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
    def __init__(self, *points: pointLike, errorOnLT3: bool = True, bounciness: float = BASEBOUNCINESS):
        super().__init__(bounciness)
        if len(points) < 3 and errorOnLT3:
            raise ValueError(
                f'Cannot have a Polygon with less than 3 points! Found: {len(points)} points!'
            )
        self.points = list(points)
    
    @property
    def x(self):
        return min([i[0] for i in self.points])
    @x.setter
    def x(self, new):
        diff = new - self.x
        self.points = [[i[0]+diff, i[1]] for i in self.points]
    @property
    def y(self):
        return min([i[1] for i in self.points])
    @y.setter
    def y(self, new):
        diff = new - self.y
        self.points = [[i[0], i[1]+diff] for i in self.points]
    
    def rect(self) -> Iterable[Number]:
        return min([i[0] for i in self.points]), min([i[1] for i in self.points]), max([i[0] for i in self.points]), max([i[1] for i in self.points])
    
    def _collides(self, othershape: Shape) -> bool:
        if not self.check_rects(othershape):
            return False
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
        return [list(i) for i in self.points]
    
    def copy(self) -> 'Polygon':
        return Polygon(*self.points, errorOnLT3=False, bounciness=self.bounciness)
    
    def __setitem__(self, item: Number, new: pointLike) -> None:
        self.points[item] = new
    
    def __str__(self):
        return f'<Polygon with points {self.points}>'

class ShapeCombiner:
    @classmethod
    def bounding_box(cls, *shapes: Rect) -> Shapes:
        if not shapes:
            return Shapes()
        rs = [s.rect() for s in shapes]
        mins, maxs = [
            min(i[0] for i in rs),
            min(i[1] for i in rs)
        ], [
            max(i[2] for i in rs),
            max(i[3] for i in rs)
        ]
        return Shapes(Rect(
            *mins,
            maxs[0]-mins[0],
            maxs[1]-mins[1]
        ))

    @classmethod
    def to_rects(cls, *shapes: Rect) -> Shapes:
        if not shapes:
            return Shapes()
        merged = True
        while merged:
            merged = False
            # Sort shapes by x-coordinate
            shapes = sorted(shapes, key=lambda x: x.x)
            outshapes1 = []
            
            while shapes:
                rect = shapes.pop(0)
                for i in shapes:
                    if rect.y == i.y and rect.h == i.h and (rect.x + rect.w >= i.x):
                        rect.w = max(rect.x + rect.w, i.x + i.w) - rect.x
                        shapes.remove(i)
                        merged = True
                        break
                outshapes1.append(rect)
            
            # Sort shapes by y-coordinate
            outshapes1 = sorted(outshapes1, key=lambda x: x.y)
            outshapes2 = []
            
            while outshapes1:
                rect = outshapes1.pop(0)
                for i in outshapes1:
                    if rect.x == i.x and rect.w == i.w and (rect.y + rect.h >= i.y):
                        rect.h = max(rect.y + rect.h, i.y + i.h) - rect.y
                        outshapes1.remove(i)
                        merged = True
                        break
                outshapes2.append(rect)
            
            shapes = outshapes2
        
        return Shapes(*shapes)

    @classmethod
    def to_polygons(cls, *shapes: Shape) -> Shapes:
        if not shapes:
            return Shapes()
        def reformat(obj):
            if isinstance(obj, ClosedShape):
                return obj
            elif isinstance(s, Line):
                return Polygon(obj.p1, obj.p2, obj.p2, obj.p1)
            # TODO: More
        reform = [reformat(s) for s in shapes]
        shapes = [reform[i] for i in range(len(reform)) if reform[i]]
        outshps = []
        while shapes:
            s = shapes.pop(0)
            colls = [i.collides(s) for i in outshps]
            if any(colls):
                for i in range(len(colls)):
                    if colls[i]:
                        newpts = []
                        oshps = [s, outshps[i]]
                        lns = [j.toLines() for j in oshps]
                        direc = 1
                        check = 0
                        checked = []
                        # TODO: When objs are covered
                        ps = [any(k.collides(Point(*j)) for k in oshps if k != s) for j in s.toPoints()]
                        j = ps.index(False)
                        while True:
                            if (check, j) not in checked:
                                checked.append((check, j))
                                ln = lns[check][j]
                                p1 = ln.p1 if direc == 1 else ln.p2
                                p2 = ln.p2 if direc == 1 else ln.p1
                                newpts.append(p1)
                                wheres = []
                                for other in range(len(oshps)):
                                    if other != check:
                                        if ln.collides(oshps[other]):
                                            for k in range(len(lns[other])):
                                                if ln.collides(lns[other][k]):
                                                    ws = ln.whereCollides(lns[other][k])
                                                    wheres.extend(zip(ws, [(other, k) for _ in range(len(ws))]))
                                if wheres != []:
                                    wheres.sort(key=lambda x: (x[0][0]-p1[0])**2+(x[0][1]-p1[1])**2)
                                    newpts.append(wheres[0][0])
                                    # Correct direction handling
                                    if oshps[check].collides(Point(*lns[wheres[0][1][0]][wheres[0][1][1]].p2)):
                                        direc = -1
                                    else:
                                        direc = 1
                                    check = wheres[0][1][0]
                                    j = wheres[0][1][1]
                                else:
                                    newpts.append(p2)
                            else:
                                break
                            j = (j + direc) % len(lns[check])
                        outshps[i] = Polygon(*newpts)
            else:
                outshps.append(s)
        return Shapes(*outshps)

# TODO: A lot more bounding box checks everywhere
# TODO: Split functions up into smaller bits and have more sharing of functions (especially with the handleCollisions)
# TODO: colliding VELOCITY, not accel
# TODO: Ovals, ovaloids and arcs (Ellipse & capsule)
# TODO: Can also input pointlike, linelike (2 points) and polygon-like iterables into all functions to reduce conversion
# TODO: Bounciness factor for each object
# TODO: Remove constant turning things into Point objects and have the functions able to use tuples instead
# OR EVEN BETTER Have the tuples have a __getitem__ for getting [0] and [1]!!! <--- Genius
# TODO: normals for lines change based off which direction they are coming from
