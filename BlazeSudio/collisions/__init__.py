from BlazeSudio.collisions.collisions import *

import shapely.geometry as _shapelyGeom
import shapely.ops as _shapelyOps

from typing import TYPE_CHECKING as _TYPE_CHECKING
from typing import Union
Number = Union[int, float]
if _TYPE_CHECKING:
    from BlazeSudio.collisions.collisions import (
        Shape,
        Shapes,
        Point,
        Line,
        Circle,
        ClosedShape,
        Polygon,
        ShapeCombiner,
    )

def shapelyToColl(shapelyShape: _shapelyGeom.base.BaseGeometry) -> Shape:
    """
    Converts a shapely shape to a BlazeSudio Shape.

    Args:
        shapelyShape (shapely.geometry.base.BaseGeometry): The shapely shape to convert.

    Returns:
        Shape: The converted shape.
    """
    if isinstance(shapelyShape, _shapelyGeom.Point):
        return Point(shapelyShape.x, shapelyShape.y)
    elif isinstance(shapelyShape, _shapelyGeom.LineString):
        return Line(*shapelyShape.coords.xy)
    elif isinstance(shapelyShape, _shapelyGeom.Polygon):
        return Polygon(*shapelyShape.exterior.coords.xy)
    elif isinstance(shapelyShape, _shapelyGeom.MultiPoint):
        return Shapes(*[Point(*i) for i in shapelyShape.coords.xy])
    elif isinstance(shapelyShape, _shapelyGeom.MultiLineString):
        return Shapes(*[Line(*i) for i in shapelyShape.coords.xy])
    elif isinstance(shapelyShape, _shapelyGeom.MultiPolygon):
        return Shapes(*[Polygon(*i.exterior.coords.xy) for i in shapelyShape])
    else:
        raise ValueError(f'Cannot convert shapely shape of type {type(shapelyShape)} to BlazeSudio Shape')

def collToShapely(collShape: Shape) -> _shapelyGeom.base.BaseGeometry:
    """
    Converts a BlazeSudio Shape to a shapely shape.

    Args:
        collShape (Shape): The BlazeSudio shape to convert.

    Returns:
        shapely.geometry.base.BaseGeometry: The converted shape.
    """
    if isinstance(collShape, Point):
        return _shapelyGeom.Point(collShape.x, collShape.y)
    elif isinstance(collShape, Line):
        return _shapelyGeom.LineString([(collShape.p1.x, collShape.p1.y), (collShape.p2.x, collShape.p2.y)])
    elif isinstance(collShape, Circle):
        return _shapelyGeom.Point(collShape.x, collShape.y).buffer(collShape.radius)
    elif isinstance(collShape, ClosedShape):
        return _shapelyGeom.Polygon([(i.x, i.y) for i in collShape.toPoints()])
    elif isinstance(collShape, Shapes):
        return _shapelyGeom.GeometryCollection([collToShapely(i) for i in collShape.shapes])
    else:
        raise ValueError(f'Cannot convert BlazeSudio shape of type {type(collShape)} to shapely shape')

class ShapeCombiner(ShapeCombiner):
    @staticmethod
    def pointsToPoly(*points: list[Point], ratio: Number) -> Union[Shape, Shapes]:
        """
        Converts a list of points to a polygon.

        Args:
            points (list[Point]): The points to convert to a polygon.
            ratio (Number): A number in the range [0, 1]. Higher means fewer verticies/less detail.

        Returns:
            Shape | Shapes: A Shapes object containing one polygon with the points from the input.
        """
        hull = _shapelyGeom.concave_hull(_shapelyGeom.MultiPoint(points), ratio=ratio)
        return shapelyToColl(hull)
    
    @staticmethod
    def ShapelyUnion(*shapes: Shape) -> Shape:
        """
        Combine all the input shapes with shapely to be a union.
        If the shapes are not all touching, they will *still* be combined into one shape.
        If you need to combine shapes but don't like the result of this, try the `ShapeCombiner.Union` method.

        Args:
            shapes (list[Shape]): The shapes to combine.

        Returns:
            Shape: A Shape which is the union of all the input shapes.
        """
        return shapelyToColl(_shapelyOps.unary_union(collToShapely(Shapes(*shapes))))
