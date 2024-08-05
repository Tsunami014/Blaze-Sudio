from typing import Union
Number = Union[int, float]

class Shape:
    def handle_collisions(self, shapegroup: 'Shapes', movement: list[Number]) -> None:
        for s in shapegroup:
            self.handle_collision(s, movement)
    
    def __repr__(self): return str(self)
    
    # Replace these
    def collides(self, othershape: 'Shape') -> bool:
        return False
    
    def copy(self) -> 'Shape':
        return Shape()
    
    def handle_collision(self, othershape: 'Shape', movement: list[Number]) -> None:
        pass
    
    def __str__(self):
        return '<Shape>'

class Shapes:
    def __init__(self, *shapes: list[Shape]):
        self.shapes = shapes
    
    def add_shape(self, shape: Shape) -> None:
        self.shapes.append(shape)
    
    def add_shapes(self, *shapes: list[Shape]) -> None:
        self.shapes.extend(shapes)
    
    def collides(self, shape: Shape) -> bool:
        for shape in self.shapes:
            if shape.collides(shape):
                return True
        return False

    def collides_multiple(self, *shapes: list[Shape]) -> bool:
        for s in shapes:
            if self.collides(s):
                return True
        return False
    
    def handle_collisions(self, shape: Shape, movement: list[Number]) -> None:
        for s in self.shapes:
            shape.handle_collision(s, movement)
    
    def copy_all(self) -> 'Shapes':
        return Shapes([s.copy() for s in self.shapes])
    
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
    
    def collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return self.x == othershape.x and self.y == othershape.y
        return othershape.collides(self)

    def copy(self) -> 'Point':
        return Point(self.x, self.y)

    def __getitem__(self, item: int) -> int|None:
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
    
    # Some code yoinked off of https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/ modified for this use case
    
    @staticmethod
    def _onSegment(p, q, r):
        """
        Given three collinear points p, q, r, the function checks if point q lies on line segment 'pr'
        """
        if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False
    
    @staticmethod
    def _orientation(p, q, r): 
        """
        Finds the orientation of an ordered triplet (p,q,r).
        The function returns the following values:
        0 : Collinear points
        1 : Clockwise points
        2 : Counterclockwise
        
        See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/ for details of below formula.
        """
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1])) 
        if (val > 0): # Clockwise orientation
            return 1
        elif (val < 0): # Counterclockwise orientation
            return 2
        else: # Collinear orientation
            return 0
    
    def collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return self._onSegment(self.p1, [othershape.x, othershape.y], self.p2)
        if isinstance(othershape, Line):
            # Find the 4 orientations required for  
            # the general and special cases 
            o1 = self._orientation(self.p1, othershape.p1, self.p2) 
            o2 = self._orientation(self.p1, othershape.p1, othershape.p2) 
            o3 = self._orientation(self.p2, othershape.p2, self.p1) 
            o4 = self._orientation(self.p2, othershape.p2, othershape.p1) 
            
            # General case 
            if ((o1 != o2) and (o3 != o4)): 
                return True

            # Special Cases 
            # p1 , q1 and p2 are collinear and p2 lies on segment p1q1 
            if ((o1 == 0) and self.onSegment(self.p1, self.p2, othershape.p1)): 
                return True
            # p1 , q1 and q2 are collinear and q2 lies on segment p1q1 
            if ((o2 == 0) and self.onSegment(self.p1, othershape.p2, othershape.p1)): 
                return True
            # p2 , q2 and p1 are collinear and p1 lies on segment p2q2 
            if ((o3 == 0) and self.onSegment(self.p2, self.p1, othershape.p2)): 
                return True
            # p2 , q2 and q1 are collinear and q1 lies on segment p2q2 
            if ((o4 == 0) and self.onSegment(self.p2, othershape.p1, othershape.p2)): 
                return True

            # If none of the cases 
            return False
        return othershape.collides(self)
    
    def copy(self) -> 'Line':
        return Line(self.p1, self.p2)
    
    def __str__(self):
        return f'<Line from {self.p1} to {self.p2}>'

class Circle(Shape):
    def __init__(self, x: Number, y: Number, r: Number):
        self.x, self.y, self.r = x, y, r
    
    def collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return (self.x - othershape.x)**2 + (self.y - othershape.y)**2 < self.r**2
        if isinstance(othershape, Line):
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
        return othershape.collides(self)
    
    def copy(self) -> 'Circle':
        return Circle(self.x, self.y, self.r)

    def __str__(self):
        return f'<Circle @ ({self.x}, {self.y}) with radius {self.r}>'

class Box(Shape):
    def __init__(self, x: Number, y: Number, w: Number, h: Number, offset: pointLike = [0,0]):
        self.offset = offset
        self.x, self.y, self.w, self.h = x+self.offset[0], y+self.offset[1], w, h
    
    @property
    def realPos(self) -> tuple[Number]:
        return self.x - self.offset[0], self.y - self.offset[1]
    
    def collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return self.x < othershape.x and self.x + self.w > othershape.x and self.y < othershape.y and self.y + self.h > othershape.y
        if isinstance(othershape, Line):
            return False # TODO
        if isinstance(othershape, Circle):
            return (self.x - othershape.r < othershape.x and self.x + self.w + othershape.r > othershape.x and self.y < othershape.y and self.y + self.h > othershape.y) or \
                   (self.x < othershape.x and self.x + self.w > othershape.x and self.y - othershape.r < othershape.y and self.y + self.h + othershape.r > othershape.y) or \
                   ((self.x - othershape.x)**2 + (self.y - othershape.y)**2 < othershape.r**2) or \
                   (((self.x + self.w) - othershape.x)**2 + (self.y - othershape.y)**2 < othershape.r**2) or \
                   ((self.x - othershape.x)**2 + ((self.y + self.h) - othershape.y)**2 < othershape.r**2) or \
                   (((self.x + self.w) - othershape.x)**2 + ((self.y + self.h) - othershape.y)**2 < othershape.r**2)
            
        if isinstance(othershape, Box):
            return self.x < othershape.x + othershape.w and self.x + self.w > othershape.x and self.y < othershape.y + othershape.h and self.y + self.h > othershape.y
    
    def handle_collision(self, othershape: Shape, movement: list[Number]) -> None:
        if isinstance(othershape, Box):
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
    
    def copy(self) -> 'Box':
        return Box(self.x, self.y, self.w, self.h, self.offset)
    
    def __str__(self):
        if self.offset != [0,0]:
            offtxt = 'without an offset'
        else:
            offtxt = f'on an offset of {self.offset}, realpos: {self.realPos}'
        return f'<Box @ ({self.x}, {self.y}) with dimensions {self.w}x{self.h} {offtxt}>'

# TODO: Box that isn't straight (Polygons)
# TODO: Ovals and ovaloids (Ellipse)
