from .core import (
    Number,
    Shape, Shapes,
    NoShape, Point,
    checkShpType, ShpTyps, ShpGroups
)
from .Combine import pointsToShape
from typing import Union

import shapely as _shp
import shapely.geometry as shapelyGeom
import shapely.ops as shapelyOps
# TODO: Not use shapely ever


def shapelyToColl(shapelyShape: shapelyGeom.base.BaseGeometry) -> Union[Shape, Shapes]:
    """
    Converts a shapely shape to a BlazeSudio Shape.

    Args:
        shapelyShape (shapely.geometry.base.BaseGeometry): The shapely shape to convert.

    Returns:
        Shape | Shapes: The converted shape.
    """
    if _shp.is_empty(shapelyShape):
        return NoShape()
    if isinstance(shapelyShape, shapelyGeom.Point):
        return Point(shapelyShape.x, shapelyShape.y)
    if isinstance(shapelyShape, shapelyGeom.LineString):
        return pointsToShape(*list(zip(*[list(i) for i in shapelyShape.coords.xy])))
    if isinstance(shapelyShape, shapelyGeom.Polygon):
        return pointsToShape(*list(zip(*[list(i) for i in shapelyShape.exterior.coords.xy])))
    if isinstance(shapelyShape, (shapelyGeom.MultiPoint, shapelyGeom.MultiLineString, shapelyGeom.MultiPolygon, shapelyGeom.GeometryCollection)):
        return Shapes(*[shapelyToColl(i) for i in shapelyShape.geoms])
    return NoShape()
    raise ValueError(f'Cannot convert shapely shape of type {type(shapelyShape)} to BlazeSudio Shape')

def collToShapely(collShape: Shape) -> shapelyGeom.base.BaseGeometry:
    """
    Converts a BlazeSudio Shape to a shapely shape.

    Args:
        collShape (Shape): The BlazeSudio shape to convert.

    Returns:
        shapely.geometry.base.BaseGeometry: The converted shape.
    """
    if checkShpType(collShape, ShpTyps.Point):
        return shapelyGeom.Point(collShape.x, collShape.y)
    if checkShpType(collShape, ShpTyps.Line):
        return shapelyGeom.LineString([(collShape.p1[0], collShape.p1[1]), (collShape.p2[0], collShape.p2[1])])
    if checkShpType(collShape, ShpTyps.Circle):
        return shapelyGeom.Point(collShape.x, collShape.y).buffer(collShape.r)
    if checkShpType(collShape, ShpGroups.CLOSED):
        return shapelyGeom.Polygon([(i[0], i[1]) for i in collShape.toPoints()])
    if checkShpType(collShape, ShpGroups.GROUP):
        return shapelyGeom.GeometryCollection([collToShapely(i) for i in collShape.shapes])
    return shapelyGeom.GeometryCollection()
    raise ValueError(f'Cannot convert BlazeSudio shape of type {type(collShape)} to shapely shape')

def pointsToPoly(*points: list[Point], ratio: Number = 0.1) -> Union[Shape, Shapes]:
    """
    Converts a list of points to a polygon.
    This differs from `ShapeCombiner.pointsToShape` in that **this** will create a polygon encapsulating all the points, \
*instead* of connecting them all with lines.

    Uses Shapely.

    Args:
        points (list[Point]): The points to convert to a polygon.
        ratio (Number): A number in the range [0, 1]. Higher means fewer verticies/less detail.

    Returns:
        Shape | Shapes: A Shapes object containing one polygon with the points from the input.
    """
    return shapelyToColl(_shp.concave_hull(shapelyGeom.MultiPoint([tuple(i) for i in points]), ratio=ratio))

def shapelyUnion(*shapes: Shape) -> Shape:
    """
    Combine all the input shapes with shapely to be a union.
    If the shapes are not all touching, they will *still* be combined into one shape.
    If you need to combine shapes but don't like the result of this, try the `ShapeCombiner.Union` method.

    Uses Shapely.

    Args:
        shapes (list[Shape]): The shapes to combine.

    Returns:
        Shape: A Shape which is the union of all the input shapes.
    """
    return shapelyToColl(shapelyOps.unary_union(collToShapely(Shapes(*shapes))))
