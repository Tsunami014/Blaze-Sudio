from typing import Union
Number = Union[int, float]

class Shape:
    # This class always collides; so *can* be used as an infinite plane, but why?
    def handle_collisions(self, shapegroup: 'Shapes', movement: list[Number]) -> None:
        for s in shapegroup:
            self.handle_collision(s, movement)
    
    def check_rects(self, othershape: 'Shape'):
        thisr, otherr = self.rect(), othershape.rect()
        return thisr[0] < otherr[2] and thisr[2] > otherr[0] and thisr[1] < otherr[3] and thisr[3] > otherr[1]
    
    def __repr__(self): return str(self)
    
    # Replace these
    def collides(self, othershape: 'Shape') -> bool:
        return True
    
    def rect(self) -> list[Number]:
        return -float('inf'), -float('inf'), float('inf'), float('inf')
    
    def copy(self) -> 'Shape':
        return Shape()
    
    def handle_collision(self, othershape: 'Shape', movement: list[Number]) -> None:
        pass
    
    def __str__(self):
        return '<Shape>'

class Shapes:
    def __init__(self, *shapes: list[Shape]):
        self.shapes = list(shapes)
    
    def add_shape(self, shape: Shape) -> None:
        self.shapes.append(shape)
    
    def add_shapes(self, *shapes: list[Shape]) -> None:
        self.shapes.extend(list(shapes))
    
    def collides(self, shape: Shape) -> bool:
        for s in self.shapes:
            if s.collides(shape):
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
    
    def collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return self.check_rects(othershape) and self._onSegment([othershape.x, othershape.y], self.p1, self.p2)
        if isinstance(othershape, Line):
            if not self.check_rects(othershape):
                return False
            # TODO: Remove the need for so many extra variables
            x1, y1, x2, y2, x3, y3, x4, y4 = self.p1[0], self.p1[1], self.p2[0], self.p2[1], othershape.p1[0], othershape.p1[1], othershape.p2[0], othershape.p2[1]
            # Calculate the direction of the lines
            def direction(xi, yi, xj, yj, xk, yk):
                return (xk - xi) * (yj - yi) - (yk - yi) * (xj - xi)
            
            d1 = direction(x3, y3, x4, y4, x1, y1)
            d2 = direction(x3, y3, x4, y4, x2, y2)
            d3 = direction(x1, y1, x2, y2, x3, y3)
            d4 = direction(x1, y1, x2, y2, x4, y4)
            
            # Check if the line segments straddle each other
            if d1 * d2 < 0 and d3 * d4 < 0:
                return True
            
            # Check if the points are collinear and on the segments
            return (d1 == 0 and self._onSegment((x1, y1), (x3, y3), (x4, y4))) or \
                   (d2 == 0 and self._onSegment((x2, y2), (x3, y3), (x4, y4))) or \
                   (d3 == 0 and self._onSegment((x3, y3), (x1, y1), (x2, y2))) or \
                   (d4 == 0 and self._onSegment((x4, y4), (x1, y1), (x2, y2)))
        
        return othershape.collides(self)
    
    def copy(self) -> 'Line':
        return Line(self.p1, self.p2)
    
    def __str__(self):
        return f'<Line from {self.p1} to {self.p2}>'

class Circle(Shape):
    def __init__(self, x: Number, y: Number, r: Number):
        self.x, self.y, self.r = x, y, r
    
    def rect(self) -> list[Number]:
        return self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r
    
    def collides(self, othershape: Shape) -> bool:
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
        return othershape.collides(self)
    
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
    
    def collides(self, othershape: Shape) -> bool:
        if isinstance(othershape, Point):
            return self.x < othershape.x and self.x + self.w > othershape.x and self.y < othershape.y and self.y + self.h > othershape.y
        if isinstance(othershape, Line):
            return self.check_rects(othershape) and (
                   (self.x < othershape.p1[0] and self.x + self.w > othershape.p1[0] and self.y < othershape.p1[1] and self.y + self.h > othershape.p1[1]) or \
                   (self.x < othershape.p2[0] and self.x + self.w > othershape.p2[0] and self.y < othershape.p2[1] and self.y + self.h > othershape.p2[1]) or \
                   (Line((self.x, self.y), (self.x + self.w, self.y)).collides(othershape)) or \
                   (Line((self.x + self.w, self.y), (self.x + self.w, self.y + self.h)).collides(othershape)) or \
                   (Line((self.x + self.w, self.y + self.h), (self.x, self.y + self.h)).collides(othershape)) or \
                   (Line((self.x, self.y + self.h), (self.x, self.y)).collides(othershape))
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
            return self.x < othershape.x + othershape.w and self.x + self.w > othershape.x and self.y < othershape.y + othershape.h and self.y + self.h > othershape.y
    
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

# TODO: Box that isn't straight (Polygons)
# TODO: Ovals and ovaloids (Ellipse)
