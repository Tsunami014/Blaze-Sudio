class Shape:
    def handle_collisions(self, shapegroup, movement):
        for s in shapegroup:
            self.handle_collision(s, movement)
    
    def __repr__(self): return str(self)
    
    # Replace these
    def collides(self, othershape):
        return False
    
    def handle_collision(self, othershape, movement):
        pass
    
    def __str__(self):
        return '<Shape>'

class Shapes:
    def __init__(self, *shapes: list[Shape]):
        self.shapes = shapes
    
    def add_shape(self, shape: Shape):
        self.shapes.append(shape)
    
    def add_shapes(self, *shapes: list[Shape]):
        self.shapes.extend(shapes)
    
    def collides(self, shape: Shape):
        for shape in self.shapes:
            if shape.collides(shape):
                return True
        return False

    def collides_multiple(self, *shapes: list[Shape]):
        for s in shapes:
            if self.collides(s):
                return True
        return False
    
    def handle_collisions(self, shape: Shape, movement: list[int]):
        for s in self.shapes:
            shape.handle_collision(s, movement)
    
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
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def collides(self, othershape):
        if isinstance(othershape, Point):
            return self.x == othershape.x and self.y == othershape.y
        return othershape.collides(self)
    
    def __str__(self):
        return f'<Point @ ({self.x}, {self.y})>'

class Line(Shape):
    def __init__(self, p1, p2):
        self.p1, self.p2 = p1, p2
    
    def collides(self, othershape):
        if isinstance(othershape, Point):
            return False # TODO
        if isinstance(othershape, Line):
            return False # TODO
        return othershape.collides(self)
    
    def __str__(self):
        return f'<Line from {self.p1} to {self.p2}>'

class Circle(Shape):
    def __init__(self, x, y, r):
        self.x, self.y, self.r = x, y, r
    
    def collides(self, othershape):
        if isinstance(othershape, Point):
            return (self.x - othershape.x)**2 + (self.y - othershape.y)**2 < self.r**2
        if isinstance(othershape, Line):
            return False # TODO
        if isinstance(othershape, Circle):
            return (self.x - othershape.x)**2 + (self.y - othershape.y)**2 < (self.r + othershape.r)**2
        return othershape.collides(self)

    def __str__(self):
        return f'<Circle @ ({self.x}, {self.y}) with radius {self.r}>'

class Box(Shape):
    def __init__(self, x, y, w, h, offset=[0,0]):
        self.offset = offset
        self.x, self.y, self.w, self.h = x+self.offset[0], y+self.offset[1], w, h
    
    @property
    def realPos(self):
        return self.x - self.offset[0], self.y - self.offset[1]
    
    def collides(self, othershape):
        if isinstance(othershape, Point):
            return self.x < othershape.x and self.x + self.w > othershape.x and self.y < othershape.y and self.y + self.h > othershape.y
        if isinstance(othershape, Line):
            return False # TODO
        if isinstance(othershape, Circle):
            return False # TODO
        if isinstance(othershape, Box):
            return self.x < othershape.x + othershape.w and self.x + self.w > othershape.x and self.y < othershape.y + othershape.h and self.y + self.h > othershape.y
    
    def handle_collision(self, othershape, movement):
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
    
    def __str__(self):
        if self.offset != [0,0]:
            offtxt = 'without an offset'
        else:
            offtxt = f'on an offset of {self.offset}, realpos: {self.realPos}'
        return f'<Box @ ({self.x}, {self.y}) with dimensions {self.w}x{self.h} {offtxt}>'

# TODO: Box that isn't straight
# TODO: Cross collisions (box-circle)
# TODO: .copy method
