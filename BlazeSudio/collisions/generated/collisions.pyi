from _typeshed import Incomplete
from enum import Enum
from typing import Any, Iterable

__all__ = ['rotate', 'rotateBy0', 'direction', 'pointOnUnitCircle', 'pointsToShape', 'ShpGroups', 'checkShpType', 'Shape', 'NoShape', 'Shapes', 'Point', 'Line', 'Circle', 'Arc', 'ClosedShape', 'Rect', 'RotatedRect', 'Polygon', 'ShapeCombiner']

Number = int | float
verboseOutput = Iterable[Any] | None
pointLike = Iterable[Number]

def rotate(origin: pointLike, point: pointLike, angle: Number) -> pointLike:
    """
    Rotate a point clockwise by a given angle around a given origin.
    The angle should be given in degrees.

    Args:
        origin (pointLike): The point to rotate around
        point (pointLike): The point to rotate
        angle (Number): The angle to rotate around in degrees

    Returns:
        pointLike: The rotated point
    """
def rotateBy0(point: pointLike, angle: Number) -> pointLike:
    """
    Rotate a point clockwise by a given angle around the origin.
    The angle should be given in degrees.

    Args:
        point (pointLike): The point to rotate
        angle (Number): The angle to rotate around in degrees

    Returns:
        pointLike: The rotated point
    """
def direction(fromPoint: pointLike, toPoint: pointLike) -> Number:
    """
    Finds the direction of `toPoint` from the origin of `fromPoint`

    Args:
        fromPoint (pointLike): The origin point
        toPoint (pointLike): The point to find the direction to

    Returns:
        Number: The direction in radians OF `toPoint` FROM `fromPoint`
    """
def pointOnUnitCircle(angle: Number, strength: Number = 1) -> pointLike:
    """
    Finds the point on the unit circle at a given angle with a given strength

    Args:
        angle (Number): The angle in radians
        strength (Number): The distance from the origin. Defaults to 1.

    Returns:
        pointLike: The point on the unit circle at angle `angle` * strength
    """
def pointsToShape(*points: Iterable[pointLike], bounciness: float = ...) -> Shape:
    """
    Converts a list of points to a shape object.
    If there is only one point, it will return a Point object, if there are two it will return a Line object, and if there are more it will return a Polygon object.

    Args:
        points (pointLike): The points to convert to a shape.
        bounciness (float, optional): The bounciness of the shape. Defaults to 0.7.

    Returns:
        Shape: The shape object made from the points
    """

class ShpGroups(Enum):
    """
    An enum representing the different groups you can put shapes in.
    """
    CLOSED = 0
    LINES = 1
    GROUP = 2

def checkShpType(shape: Shape | Shapes, typs: type | ShpGroups | Iterable[type | ShpGroups]) -> bool:
    """
    Checks to see if a shape is of a certain type or group.

    Args:
        shape (Shape or Shapes]): The input shape or shapes to check the type of.
        typs (ShpTypes, ShpGroups, or an Iterable[ShpTypes or ShpGroups]): The shape type(s) &/or group(s) to check for.

    Returns:
        bool: Whether the shape is of the specified type(s) or group(s).
    """

class Shape:
    GROUPS: Incomplete
    x: Number
    y: Number
    bounciness: Incomplete
    def __init__(self, bounciness: float = ...) -> None:
        """
        The base Shape class. This defaults to always collide.
        This class always collides; so *can* be used as an infinite plane, but why?

        Args:
            bounciness (float, optional): How bouncy this object is. 1 = rebounds perfectly, <1 = eventually will stop, >1 = will bounce more each time. Defaults to 0.7.
        """
    def collides(self, othershape: Shape | Shapes | Iterable['Shape']) -> bool:
        """
        Whether this shape collides with another shape(s)

        Args:
            othershape (Shape / Shapes / Iterable[Shape]): The shape(s) to check for collision with

        Returns:
            bool: whether or not this shape collides with any of the input shape(s)
        """
    def whereCollides(self, othershape: Shape | Shapes | Iterable['Shape']) -> Iterable[pointLike]:
        """
        Finds where this shape collides with another shape(s)

        Args:
            othershape (Shape / Shapes / Iterable[Shape]): The shape(s) to check for collision with

        Returns:
            Iterable[pointLike]: Points that lie both on this shape and the input shape(s)
        """
    def check_rects(self, othershape: Shape) -> bool:
        """
        Check whether this shape's bounding box collides with the other shape's.
        This can be used for a very fast way to know if shapes *aren't* colliding, but to find if they **are** then use `collides`.
        In fact, the `collides` method already uses this in it, so there isn't much need for you to use it.

        Args:
            othershape (Shape): _description_

        Returns:
            bool: Whether the bounding boxes of this object an the othershape collide
        """
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike | Iterable[pointLike]:
        """
        Finds the closest point ON THIS OBJECT **TO** the other object

        Args:
            othershape (Shape): The other shape to find the closest point to
            returnAll (bool, optional): Whether to return *all* the potential closest points sorted in order of closeness or just **the** closest. Defaults to False (only the closest).

        Returns:
            pointLike|Iterable[pointLike]: The closest point(s) on this object to the other object. Whether this is an iterable or not depends on the `returnAll` parameter.
        """
    def isCorner(self, point: pointLike, precision: Number = ...) -> bool:
        """
        Finds whether a point is on a corner of this shape.

        Args:
            point (pointLike): The point to find if it's a corner
            precision (Number, optional): The decimal places to round to to check. Defaults to 5.

        Returns:
            bool: Whether the point is on a corner of this shape
        """
    def tangent(self, point: pointLike, vel: pointLike) -> Number:
        """
        Finds the tangent on this surface to a point with a given velocity

        Args:
            point (pointLike): The point to find the tangent of this surface from
            vel (pointLike): Which direction the point is moving (useful for example with lines for finding which side of the line the tangent should be of)

        Returns:
            Number: The tangent of this object at the point. You can -90 to get the normal.
        """
    def toLines(self) -> Iterable['Line']:
        """
        Returns:
            Iterable[Line]: Get a list of all the Lines that make up this object. For anything under a ClosedShape, this will most likely be empty.
        """
    def toPoints(self) -> Iterable[pointLike]:
        """
        Returns:
            Iterable[pointLike]: Get a list of all the Points that make up this object. For Circles, Arcs and Shape's, this will be empty.
        """
    def rect(self) -> Iterable[Number]:
        """
        Returns the rectangle bounding box surrounding this object.

        Returns:
            Iterable[Number]: (min x, min y, max x, max y)
        """
    def handleCollisionsPos(self, oldP: Shape, newP: Shape, objs: Shapes | Iterable['Shape'], vel: pointLike = [0, 0], verbose: bool = False) -> tuple['Shape', pointLike, verboseOutput]:
        """
        This is called to modify objects' positions to bounce off objects.
        """
    def handleCollisionsVel(self, vel: pointLike, objs: Shapes | Iterable['Shape'], verbose: bool = False) -> tuple['Shape', pointLike, verboseOutput]:
        """
        This is a wrapper for `handleCollisionsPos` to handle velocity instead of position.
        """
    def copy(self) -> Shape:
        """
        Copy this shape to return another with the same properties
        """
    def __getitem__(self) -> None: ...
    def __setitem__(self) -> None: ...

class NoShape(Shape):
    def __init__(self) -> None:
        """
        A class to represent no shape. This is useful for when you want to have a shape that doesn't collide with anything.
        """
    def copy(self) -> NoShape:
        """Make a copy of this non-existant shape"""

class Shapes:
    GROUPS: Incomplete
    shapes: Incomplete
    def __init__(self, *shapes: Shape) -> None:
        """
        A class which holds multiple shapes and can be used to do things with all of them at once.

        Args:
            *shapes (Shape): The shapes to start off with in this object.
        
        Example:
        `Shapes(Shape1, Shape2)` OR `Shapes(*[Shape1, Shape2])`
        """
    def add_shape(self, shape: Shape) -> None:
        """
        Adds a shape to this Shapes object.

        Args:
            shape (Shape): The desired shape to add.
        """
    def add_shapes(self, *shapes: Shape) -> None:
        """
        Adds multiple shapes to this object.

        Args:
            *shapes (Shape): The shapes to add to this object.
        
        Example:
        `shapes.add_shapes(Shape1, Shape2)` OR `shapes.add_shapes(*[Shape1, Shape2])`
        """
    def remove_shape(self, shape: Shape) -> None:
        """
        Removes a specific shape from this object.

        Args:
            shape (Shape): The shape to remove.
        """
    def remove_shapes(self, *shapes: Shape) -> None:
        """
        Removes multiple shapes from this object.

        Args:
            *shapes (Shape): The shapes to remove.
        
        Example:
        `shapes.remove_shapes(Shape1, Shape2)` OR `shapes.remove_shapes(*[Shape1, Shape2])`
        """
    def collides(self, shapes: Shape | Shapes | Iterable['Shape']) -> bool:
        """
        Checks for collisions between all the shapes in this object and the input shape(s).

        Args:
            shapes (Shape / Shapes / Iterable[Shape]]): The shape(s) to check for collisions against

        Returns:
            bool: True if *any* of the shapes in this object collide with *any* of the input shapes
        """
    def whereCollides(self, shapes: Shape | Shapes | Iterable['Shape']) -> Iterable[pointLike]:
        """
        Find the points where this object collides with the input shape(s).

        Args:
            shapes (Shape / Shapes / Iterable[Shape]]): _description_

        Returns:
            Iterable[pointLike]: _description_
        """
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> Iterable[pointLike]:
        """
        Finds the closest point ON all of these objects TO the input shape.
        PLEASE NOTE that this won't have the list in order of closest to furthest, you have to do that yourself.

        Args:
            othershape (Shape): The shape to find the cosest points towards
            returnAll (bool, optional): Whether to return EVERY possible option, sorted from closest to furthest. Defaults to False.

        Returns:
            Iterable[pointLike]: All the closest point(s) ON each of these objects
        """
    def isCorner(self, point: pointLike, precision: Number = ...) -> dict[Shape | Shapes, bool]:
        """
        Takes each object and finds whether the input point is on the corner of that object.

        Args:
            point (pointLike): The point to find if it's on the corner or not
            precision (Number, optional): The decimal places to round to to check. Defaults to 5.

        Returns:
            dict[Shape / Shapes: bool]: A dictionary of each object in this and whether the point is a corner on it or not.
        """
    def tangent(self, point: pointLike, vel: pointLike) -> Iterable[Number]:
        """
        Finds the tangent on each of these objects for the specified point. -90 = normal.

        Args:
            point (pointLike): The point to find the tangent from
            vel (pointLike): Which direction the point is moving (useful for example with lines for finding which side of the line the tangent should be of)

        Returns:
            Iterable[Number]: A list of all the tangents to the specified point.
        """
    def rect(self) -> Iterable[Number]:
        """
        Returns the rectangle bounding box surrounding every one of these objects.

        Returns:
            Iterable[Number]: (min x, min y, max x, max y)
        """
    def copy(self) -> Shapes:
        """
        Make a copy of this class with a copy of each shape in it.
        """
    def copy_leave_shapes(self) -> Shapes:
        """
        Makes a copy of this class but keeps the same shapes.
        """
    def __iter__(self): ...
    def __getitem__(self, index: Number) -> Shape | Shapes: ...
    def __setitem__(self, index: Number, new: Shape | Shapes) -> None: ...

class Point(Shape):
    def __init__(self, x: Number, y: Number, bounciness: float = ...) -> None:
        """
        An infintesimally small point in space.

        Args:
            x (Number): The x ordinate of this object.
            y (Number): The y ordinate of this object.
            bounciness (float, optional): How bouncy this object is. 1 = rebounds perfectly, <1 = eventually will stop, >1 = will bounce more each time. Defaults to 0.7.
        """
    def rect(self) -> Iterable[Number]:
        """
        Returns the rectangle bounding box surrounding this point.

        Returns:
            Iterable[Number]: (min x, min y, max x, max y)
        """
    def toPoints(self) -> Iterable[pointLike]:
        """
        Returns:
            Iterable[pointLike]: Get a list of all the Points that make up this object; i.e. just this one point.
        """
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike | Iterable[pointLike]:
        """
        Finds the closest point ON this object TO the other shape

        Args:
            othershape (Shape): The other shape to find the closest point towards
            returnAll (bool, optional): Whether to return ALL the possible options in order of closeness (True) or just the closest (False). Defaults to False.

        Returns:
            pointLike / Iterable[pointLike]: The closest points ON this object TO the other object
        """
    def getTuple(self) -> tuple[Number]:
        """
        Gets this object in a tuple format: (x, y).
        Do you get the point?
        """
    def handleCollisionsPos(self, oldPoint: Point | pointLike, newPoint: Point | pointLike, objs: Shapes | Iterable[Shape], vel: pointLike = [0, 0], replaceSelf: bool = True, precision: Number = ..., verbose: bool = False) -> tuple[pointLike, pointLike, verboseOutput]:
        """
        Handles movement of this point and it bouncing off of other objects.
        It is recommended you use `.handleCollisionsVel` instead of this, as it handles velocity instead of raw movement and is easier to use.

        But if you are to use this, remember to still provide the vel param. It will sometimes provide weird results if you don't.
        It could even just be the difference in positions, it just needs to be something realistic.

        Args:
            oldPoint (Point / pointLike): The old position of this object.
            newPoint (Point / pointLike): The new position of this object.
            objs (Shapes / Iterable[Shape]): The objects this will bounce off.
            vel (pointLike, optional): The velocity that this object is going. Defaults to [0, 0].
            replaceSelf (bool, optional): Whether to replace self.x and self.y with the new position of the object after bouncing or not. Defaults to True.
            precision (Number, optional): The decimal places to round to to check (for things like corner checking). Defaults to 5.
            verbose (bool, optional): Whether to give verbose output or not. Defaults to False.

        Returns:
            tuple[pointLike, pointLike, veboseOutput?]: The new position and vel of this object respectively, and if verbose then the verboseOutput.
        
        VerboseOutput:
            DidReflect (bool): Whether the line reflected off of something
        """
    def handleCollisionsVel(self, vel: pointLike, objs: Shapes | Iterable[Shape], replaceSelf: bool = True, precision: Number = ..., verbose: bool = False) -> tuple[pointLike, pointLike, verboseOutput]:
        """
        Handles movement of this point via velocity and it bouncing off of other objects.

        Args:
            vel (pointLike): The velocity of this point
            objs (Shapes / Iterable[Shape]): The objects to bounce off of
            replaceSelf (bool, optional): Whether or not to replace self.x and self.y with the new position. Defaults to True.
            precision (Number, optional): The decimal places to round to to check (for things like corner checking). Defaults to 5.
            verbose (bool, optional): Whether to give verbose output or not. Defaults to False.

        Returns:
            tuple[pointLike, pointLike, veboseOutput?]: The new position and vel of this object respectively, and if verbose then the verboseOutput.
        
        VerboseOutput:
            DidReflect (bool): Whether the line reflected off of something
        """
    def copy(self) -> Point:
        """
        Make a brand new Point with the same values!
        """
    def __getitem__(self, item: Number) -> Number: ...
    x: Incomplete
    y: Incomplete
    def __setitem__(self, item: Number, new: Number) -> None: ...
    def __iter__(self): ...

class Line(Shape):
    GROUPS: Incomplete
    def __init__(self, p1: pointLike, p2: pointLike, bounciness: float = ...) -> None:
        """
        A line segment object.

        Args:
            p1 (pointLike): The start point of this line
            p2 (pointLike): The end point of this line
            bounciness (float, optional): How bouncy this object is. 1 = rebounds perfectly, <1 = eventually will stop, >1 = will bounce more each time. Defaults to 0.7.
        """
    @property
    def x(self):
        """One of the line's points' x value. Changing this will move the other point by the difference!"""
    p1: Incomplete
    p2: Incomplete
    @x.setter
    def x(self, value) -> None: ...
    @property
    def y(self):
        """One of the line's points' y value. Changing this will move the other point by the difference!"""
    @y.setter
    def y(self, value) -> None: ...
    def rect(self) -> Iterable[Number]:
        """
        Returns the rectangle bounding box surrounding this line.

        Returns:
            Iterable[Number]: (min x, min y, max x, max y)
        """
    def toLines(self) -> Iterable['Line']:
        """
        Returns:
            Iterable[Line]: Get a list of all the Lines that make up this object; i.e. just this one line.
        """
    def toPoints(self) -> Iterable[pointLike]:
        """
        Returns:
            Iterable[pointLike]: Get a list of all the Points that make up this object.
        """
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike | Iterable[pointLike]:
        """
        Find the closest point ON this object TO another object.

        Args:
            othershape (Shape): The other shape to find the closest point towards.
            returnAll (bool, optional): Whether to return ALL the possible options in order of closeness (True) or just the closest (False). Defaults to False.

        Returns:
            pointLike / Iterable[pointLike]: The closest points ON this object TO the other object
        """
    def isCorner(self, point: pointLike, precision: Number = ...) -> bool:
        """
        Finds whether a point is on a corner of this shape.

        Args:
            point (pointLike): The point to find if it's a corner
            precision (Number, optional): The decimal places to round to to check. Defaults to 5.

        Returns:
            bool: Whether the point is on a corner of this shape
        """
    def tangent(self, point: pointLike, vel: pointLike) -> Number:
        """
        Finds the tangent on this surface to a point with a given velocity.

        Args:
            point (pointLike): The point to find the tangent of this surface from.
            vel (pointLike): Which direction the point is moving. In this case (for lines) it is actually very important, so please don't forget it.

        Returns:
            Number: The tangent of the line at the point. You can -90 to get the normal.
        """
    def handleCollisionsPos(self, oldLine: Line, newLine: Line, objs: Shapes | Iterable[Shape], vel: pointLike = [0, 0], replaceSelf: bool = True, precision: Number = ..., verbose: bool = False) -> tuple['Line', pointLike, verboseOutput]:
        """
        Handles movement of this line and it bouncing off of other objects.
        It is recommended you use `.handleCollisionsVel` instead of this, as it handles velocity instead of raw movement and is easier to use.

        But if you are to use this, remember to still provide the vel param. It will provide VERY weird results if you don't.
        It could even just be the difference in positions, it just needs to be something realistic.

        Args:
            oldLine (Line): The old Line object.
            newLine (Line): The new Line object. Should be the exact same as the old one except with the 2 points offset by the same amount.
            objs (Shapes / Iterable[Shape]): The objects this will bounce off.
            vel (pointLike, optional): The velocity that this object is going. Defaults to [0, 0].
            replaceSelf (bool, optional): Whether to move this Line to the new position after bouncing or not. Defaults to True.
            precision (Number, optional): The decimal places to round to to check (for things like corner checking). Defaults to 5.
            verbose (bool, optional): Whether to give verbose output or not. Defaults to False.

        Returns:
            tuple[Line, pointLike, veboseOutput?]: The new Line object and vel of this object respectively, and if verbose then the verboseOutput.
        
        VerboseOutput:
            CollisionType (list[int, ...] / None): The type of collision that occured for each sub-collision (if it ever collided, that is)
            DidReflect (bool): Whether the line reflected off of something
        """
    def handleCollisionsVel(self, vel: pointLike, objs: Shapes | Iterable[Shape], replaceSelf: bool = True, precision: Number = ..., verbose: bool = False) -> tuple['Line', pointLike, verboseOutput]:
        """
        Handles movement of this line via velocity and it bouncing off of other objects.

        Args:
            vel (pointLike): The velocity of this line.
            objs (Shapes / Iterable[Shape]): The objects to bounce off of.
            replaceSelf (bool, optional): Whether to move this Line to the new position after bouncing or not. Defaults to True.
            precision (Number, optional): The decimal places to round to to check (for things like corner checking). Defaults to 5.
            verbose (bool, optional): Whether to give verbose output or not. Defaults to False.

        Returns:
            tuple[Line, pointLike, veboseOutput?]: The new position and vel of this object respectively, and if verbose then the verboseOutput.
        
        VerboseOutput:
            CollisionType (list[int, ...] / None): The type of collision that occured for each sub-collision (if it ever collided, that is)
            DidReflect (bool): Whether the line reflected off of something
        """
    def copy(self) -> Line:
        """
        Make a copy of the Line with the same values!
        """
    def __getitem__(self, item: Number) -> pointLike: ...
    def __setitem__(self, item: Number, new: pointLike) -> None: ...

class Circle(Shape):
    GROUPS: Incomplete
    def __init__(self, x: Number, y: Number, r: Number, bounciness: float = ...) -> None:
        """
        A perfect circle.

        Args:
            x (Number): The x ordinate of the centre of this circle.
            y (Number): The y ordinate of the centre of this circle.
            r (Number): The radius of the circle
            bounciness (float, optional): How bouncy this object is. 1 = rebounds perfectly, <1 = eventually will stop, >1 = will bounce more each time. Defaults to 0.7.
        """
    def rect(self) -> Iterable[Number]:
        """
        Returns the rectangle bounding box surrounding this circle.

        Returns:
            Iterable[Number]: (min x, min y, max x, max y)
        """
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike | Iterable[pointLike]:
        """
        Find the closest point ON this object TO another object.

        Args:
            othershape (Shape): The other object to find the closest point to
            returnAll (bool, optional): Whether to return all the possible points in order of closeness or not. Defaults to False.

        Returns:
            pointLike / Iterable[pointLike]: The closest point(s, depending on returnAll) ON this object TO the othershape
        """
    def isCorner(self, point: pointLike, precision: Number = ...) -> bool:
        """
        Finds whether a point is on a corner of this shape.

        Args:
            point (pointLike): The point to find if it's a corner
            precision (Number, optional): The decimal places to round to to check. Defaults to 5.

        Returns:
            bool: Whether the point is on a corner of this shape
        """
    def tangent(self, point: pointLike, vel: pointLike) -> Number:
        """
        Finds the tangent on this surface to a point with a given velocity.

        Args:
            point (pointLike): The point to find the tangent of this surface from.
            vel (pointLike): Which direction the point is moving.

        Returns:
            Number: The tangent of the circle at the point. You can -90 to get the normal.
        """
    def copy(self) -> Circle:
        """
        Make a replica of this object with the same object.
        """
    def __getitem__(self, item: Number) -> Number: ...
    x: Incomplete
    y: Incomplete
    r: Incomplete
    def __setitem__(self, item: Number, new: Number) -> None: ...

class Arc(Circle):
    GROUPS: Incomplete
    precision: Incomplete
    bounciness: Incomplete
    def __init__(self, x: Number, y: Number, rad: Number, startAngle: Number, endAngle: Number, precision: Number = ..., bounciness: float = ...) -> None:
        """
        A section of a circle's circumfrance.

        Args:
            x (Number): The x position of this arc's centre.
            y (Number): The y position of this arc's centre.
            rad (Number): The radius of the circle.
            startAngle (Number): The starting angle to take the portion of the circumfrance of. Wraps around.
            endAngle (Number): The ending angle to take the portion of the circumfrance of. Wraps around.
            precision (Number, optional): The decimal places to round to to check. Defaults to 5. This is needed as almost everything requires a very precise exact check to succeed and sometimes decimal errors occur and you get an equation like `10000.000000000002 == 10000.0` which is False. This is to prevent that.
            bounciness (float, optional): How bouncy this object is. 1 = rebounds perfectly, <1 = eventually will stop, >1 = will bounce more each time. Defaults to 0.7.
        """
    def flip(self) -> None:
        """
        Flips the portion taken to make the arc; so an arc covering 90 degrees of the circle will now cover 270, and vice versa.
        """
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike | Iterable[pointLike]:
        """
        Finds the closest point ON THIS OBJECT **TO** the other object

        Args:
            othershape (Shape): The other shape to find the closest point to
            returnAll (bool, optional): Whether to return *all* the potential closest points sorted in order of closeness or just **the** closest. Defaults to False (only the closest).

        Returns:
            pointLike|Iterable[pointLike]: The closest point(s) on this object to the other object. Whether this is an iterable or not depends on the `returnAll` parameter.
        """
    def angleInRange(self, angle: Number) -> bool:
        """
        Check to see if an angle is in the range of this arc.

        Args:
            angle (Number): The angle to check if it is in range of this arc or not.

        Returns:
            bool: Whether or not the angle is in the range of this arc.
        """
    def endPoints(self) -> Iterable[pointLike]:
        """
        Gets the end points of the arc

        Returns:
            Iterable[pointLike]: The endpoints of the arc
        """
    def rect(self) -> Iterable[Number]:
        """
        Returns the rectangle bounding box surrounding this object.

        Returns:
            Iterable[Number]: (min x, min y, max x, max y)
        """
    def copy(self) -> Arc:
        """
        Because Noah's first arc broke, now you need another one.
        """
    def __getitem__(self, item: Number) -> Number | pointLike: ...
    x: Incomplete
    y: Incomplete
    r: Incomplete
    startAng: Incomplete
    endAng: Incomplete
    def __setitem__(self, item: Number, new: Number | pointLike) -> None: ...

class ClosedShape(Shape):
    GROUPS: Incomplete
    def tangent(self, point: pointLike, vel: pointLike) -> Number:
        """
        Finds the tangent on this surface to a point with a given velocity.

        Args:
            point (pointLike): The point to find the tangent of this surface from.
            vel (pointLike): Which direction the point is moving. In this case (for closed shapes, which are made of lines) it is actually very important, so please don't forget it.

        Returns:
            Number: The tangent of the line at the point. You can -90 to get the normal.
        """
    def closestPointTo(self, othershape: Shape, returnAll: bool = False) -> pointLike | Iterable[pointLike]:
        """
        Find the closest point ON this object TO another object.

        Args:
            othershape (Shape): The other object to find the closest point to
            returnAll (bool, optional): Whether to return all the possible points in order of closeness or not. Defaults to False.

        Returns:
            pointLike / Iterable[pointLike]: The closest point(s, depending on returnAll) ON this object TO the othershape
        """
    def handleCollisionsPos(self, oldShp: ClosedShape, newShp: ClosedShape, objs: Shapes | Iterable[Shape], vel: pointLike = [0, 0], replaceSelf: bool = True, precision: Number = ..., verbose: bool = False) -> tuple['ClosedShape', pointLike, verboseOutput]:
        """
        Handles movement of this closed shape and it bouncing off of other objects.
        It is recommended you use `.handleCollisionsVel` instead of this, as it handles velocity instead of raw movement and is easier to use.

        But if you are to use this, remember to still provide the vel param. It will provide VERY weird results if you don't.
        It could even just be the difference in positions, it just needs to be something realistic.

        Args:
            oldShp (ClosedShape): The old object.
            newShp (ClosedShape): The new object. Should be the exact same as the old one except with the points offset by the same amount.
            objs (Shapes / Iterable[Shape]): The objects this will bounce off.
            vel (pointLike, optional): The velocity that this object is going. Defaults to [0, 0].
            replaceSelf (bool, optional): Whether to move this object to the new position after bouncing or not. Defaults to True.
            precision (Number, optional): The decimal places to round to to check (for things like corner checking). Defaults to 5.
            verbose (bool, optional): Whether to give verbose output or not. Defaults to False.

        Returns:
            tuple[ClosedShape, pointLike, veboseOutput?]: The new object and vel respectively, and if verbose then the verboseOutput.
        
        VerboseOutput:
            CollisionType (list[int, ...] / None): The type of collision that occured for each sub-collision (if it ever collided, that is)
            DidReflect (bool): Whether the object reflected off of something
        """
    def handleCollisionsVel(self, vel: pointLike, objs: Shapes | Iterable[Shape], replaceSelf: bool = True, precision: Number = ..., verbose: bool = False) -> tuple['ClosedShape', pointLike, verboseOutput]:
        """
        Handles movement of this object via velocity and it bouncing off of other objects.

        Args:
            vel (pointLike): The velocity of this object.
            objs (Shapes / Iterable[Shape]): The objects to bounce off of.
            replaceSelf (bool, optional): Whether to move this object to the new position after bouncing or not. Defaults to True.
            precision (Number, optional): The decimal places to round to to check (for things like corner checking). Defaults to 5.
            verbose (bool, optional): Whether to give verbose output or not. Defaults to False.

        Returns:
            tuple[ClosedShape, pointLike, veboseOutput?]: The new position and vel of this object respectively, and if verbose then the verboseOutput.
        
        VerboseOutput:
            CollisionType (list[int, ...] / None): The type of collision that occured for each sub-collision (if it ever collided, that is)
            DidReflect (bool): Whether the line reflected off of something
        """
    def isCorner(self, point: pointLike, precision: Number = ...) -> bool:
        """
        Finds whether a point is on a corner of this shape.

        Args:
            point (pointLike): The point to find if it's a corner
            precision (Number, optional): The decimal places to round to to check. Defaults to 5.

        Returns:
            bool: Whether the point is on a corner of this shape
        """
    def toLines(self) -> Iterable[Line]:
        """
        Returns:
            Iterable[Line]: Get a list of all the Lines that make up this object
        """
    def toPoints(self) -> Iterable[pointLike]:
        """
        Returns:
            Iterable[pointLike]: Get a list of all the Points that make up this object
        """
    def __getitem__(self, item: Number) -> pointLike: ...

class Rect(ClosedShape):
    def __init__(self, x: Number, y: Number, w: Number, h: Number, bounciness: float = ...) -> None:
        """
        A Rectangle.

        Args:
            x (Number): The x ordinate.
            y (Number): The y ordinate.
            w (Number): The width.
            h (Number): The height.
            bounciness (float, optional): How bouncy this object is. 1 = rebounds perfectly, <1 = eventually will stop, >1 = will bounce more each time. Defaults to 0.7.
        """
    def rect(self) -> Iterable[Number]:
        """
        Returns the rectangle bounding box surrounding this rectangle, which is virtually just the rectangle itself in a different form.

        Returns:
            Iterable[Number]: (min x, min y, max x, max y)
        """
    def toLines(self) -> Iterable[Line]:
        """
        Returns:
            Iterable[Line]: Get a list of all the Lines that make up this object
        """
    def toPoints(self) -> Iterable[pointLike]:
        """
        Returns:
            Iterable[pointLike]: Get a list of all the Points that make up this object
        """
    def copy(self) -> Rect:
        """
        Clone this object using the latest cloning technology.
        """
    def __setitem__(self, item: Number, new: pointLike) -> None: ...

class RotatedRect(ClosedShape):
    cachedPoints: Incomplete
    cacheRequirements: Incomplete
    def __init__(self, x: Number, y: Number, w: Number, h: Number, rotation: Number, bounciness: float = ...) -> None:
        """
        A rectangle...... That is rotated.
        It is rotated around it's x and y coordinates.

        Args:
            x (Number): The x ordinate. Also what it rotates around.
            y (Number): The y ordinate. Also what it rotates around.
            w (Number): The width of the object.
            h (Number): The height of the object.
            rotation (Number): The rotation of the object.
            bounciness (float, optional): How bouncy this object is. 1 = rebounds perfectly, <1 = eventually will stop, >1 = will bounce more each time. Defaults to 0.7.
        """
    cache: Incomplete
    def getCache(self) -> Iterable[pointLike]:
        """
        Specifically for the rotatedRect. This is a utility function to cache the rotated points so it doesn't have to re-rotate them every time.
        Please don't use this in your code unless you know what you're doing. Instead, use `.toPoints()` or `.toLines()`.

        Returns:
            Iterable[pointLike]: All the points that make up this rectangle, all rotated BUT NOT TRANSLATED. You must add (self.x, self.y) to each one to get the pos.
        """
    def rect(self) -> Iterable[Number]:
        """
        Returns the rectangle bounding box surrounding this rectangle.

        Returns:
            Iterable[Number]: (min x, min y, max x, max y)
        """
    def toPoints(self) -> Iterable[pointLike]:
        """
        Returns:
            Iterable[pointLike]: Get a list of all the Points that make up this object
        """
    def toLines(self) -> Iterable[Line]:
        """
        Returns:
            Iterable[Line]: Get a list of all the Lines that make up this object
        """
    def copy(self) -> RotatedRect:
        """
        Spawn in a duplicate object
        """
    def __setitem__(self, item: Number, new: pointLike) -> None: ...

class Polygon(ClosedShape):
    points: Incomplete
    def __init__(self, *points: pointLike, errorOnLT3: bool = True, bounciness: float = ...) -> None: ...
    @property
    def x(self):
        """One of this object's points' x value. Changing this will move the other points by the difference!"""
    @x.setter
    def x(self, new) -> None: ...
    @property
    def y(self):
        """One of this object's points' y value. Changing this will move the other points by the difference!"""
    @y.setter
    def y(self, new) -> None: ...
    def rect(self) -> Iterable[Number]:
        """
        Returns the rectangle bounding box surrounding this polygon.

        Returns:
            Iterable[Number]: (min x, min y, max x, max y)
        """
    def toLines(self) -> Iterable[Line]:
        """
        Returns:
            Iterable[Line]: Get a list of all the Lines that make up this object.
        """
    def toPoints(self) -> Iterable[pointLike]:
        """
        Returns:
            Iterable[pointLike]: Get a list of all the Points that make up this object.
        """
    def copy(self) -> Polygon:
        """
        And then he lifted his arms and said, 'LET THERE BE ANOTHER!'
        """
    def __setitem__(self, item: Number, new: pointLike) -> None: ...

class ShapeCombiner:
    @staticmethod
    def boundingBox(*shapes: Rect) -> Shapes:
        """
        Makes a new shape which is the bounding box of all the shapes combined.

        Returns:
            Shapes: A Shapes object containing one rectangle (if there are any shapes in shapes; else nothing) which is the bounding box around every input shape.
        """
    @staticmethod
    def combineRects(*shapes: Rect) -> Shapes:
        """
        Combines adjacent rectangles.
        What this means is if you have 2 rectangles exactly touching they will combine to one
        ```
        +-+-+      +---+
        | | |  ->  |   |
        +-+-+      +---+
        ```
        This will only work if the combination would exactly encompass each shape without any room for air and would be a rectangle.
        For a more general combination, try using `.to_polygons()` instead.

        Returns:
            Shapes: A Shapes object with the rectangles from the input shapes combined
        """
    @staticmethod
    def Union(*shapes: Shape) -> Shapes:
        """
        Combine all the input shapes with a unary union. Still in progress and doesn't work too well.

        Returns:
            Shapes: The union of all the shapes.
        """