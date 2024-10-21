try:
    from BlazeSudio.debug.globals import IMPORT_CONFIG as _CNFG
    debug = _CNFG['Debug']
except ImportError:
    debug = False

if debug:
    from BlazeSudio.collisions.lib.collisions import *
else:
    from BlazeSudio.collisions.generated.collisions import *

import pygame as _pygame
import shapely as _shapely
import shapely.geometry as _shapelyGeom
import shapely.ops as _shapelyOps
from math import radians as _toRadians

from typing import TYPE_CHECKING as _TYPE_CHECKING
from typing import Union
Number = Union[int, float]
if _TYPE_CHECKING:
    # from BlazeSudio.collisions.lib.collisions import (
    from BlazeSudio.collisions.generated.collisions import (
        Shape,
        Shapes,
        checkShpType,
        ShpGroups,
        Point,
        Line,
        Arc,
        Circle,
        ShapeCombiner,
        NoShape,
    )

def shapelyToColl(shapelyShape: _shapelyGeom.base.BaseGeometry) -> Union[Shape, Shapes]:
    """
    Converts a shapely shape to a BlazeSudio Shape.

    Args:
        shapelyShape (shapely.geometry.base.BaseGeometry): The shapely shape to convert.

    Returns:
        Shape | Shapes: The converted shape.
    """
    if _shapely.is_empty(shapelyShape):
        return NoShape()
    if isinstance(shapelyShape, _shapelyGeom.Point):
        return Point(shapelyShape.x, shapelyShape.y)
    if isinstance(shapelyShape, _shapelyGeom.LineString):
        return ShapeCombiner.pointsToShape(*list(zip(*[list(i) for i in shapelyShape.coords.xy])))
    if isinstance(shapelyShape, _shapelyGeom.Polygon):
        return ShapeCombiner.pointsToShape(*list(zip(*[list(i) for i in shapelyShape.exterior.coords.xy])))
    if isinstance(shapelyShape, (_shapelyGeom.MultiPoint, _shapelyGeom.MultiLineString, _shapelyGeom.MultiPolygon, _shapelyGeom.GeometryCollection)):
        return Shapes(*[shapelyToColl(i) for i in shapelyShape.geoms])
    raise ValueError(f'Cannot convert shapely shape of type {type(shapelyShape)} to BlazeSudio Shape')

def collToShapely(collShape: Shape) -> _shapelyGeom.base.BaseGeometry:
    """
    Converts a BlazeSudio Shape to a shapely shape.

    Args:
        collShape (Shape): The BlazeSudio shape to convert.

    Returns:
        shapely.geometry.base.BaseGeometry: The converted shape.
    """
    if checkShpType(collShape, Point):
        return _shapelyGeom.Point(collShape.x, collShape.y)
    if checkShpType(collShape, Line):
        return _shapelyGeom.LineString([(collShape.p1.x, collShape.p1.y), (collShape.p2.x, collShape.p2.y)])
    if checkShpType(collShape, Circle):
        return _shapelyGeom.Point(collShape.x, collShape.y).buffer(collShape.radius)
    if checkShpType(collShape, ShpGroups.CLOSED):
        return _shapelyGeom.Polygon([(i.x, i.y) for i in collShape.toPoints()])
    if checkShpType(collShape, ShpGroups.GROUP):
        return _shapelyGeom.GeometryCollection([collToShapely(i) for i in collShape.shapes])
    raise ValueError(f'Cannot convert BlazeSudio shape of type {type(collShape)} to shapely shape')

def drawShape(surface: _pygame.Surface, shape: Shape, colour: tuple[int, int, int], width: int = 0):
    """
    Draws a BlazeSudio shape to a Pygame surface.

    Args:
        surface (pygame.Surface): The surface to draw the shape on.
        shape (Shape): The shape to draw.
        colour (tuple[int, int, int]): The colour to draw the shape in.
        width (int, optional): The width of the lines to draw. Defaults to 0.
    """
    if checkShpType(shape, Point):
        _pygame.draw.circle(surface, colour, (int(shape.x), int(shape.y)), width)
    elif checkShpType(shape, Line):
        if tuple(shape.p1) == tuple(shape.p2):
            _pygame.draw.circle(surface, colour, (int(shape.p1[0]), int(shape.p1[1])), int(width/2))
        _pygame.draw.line(surface, colour, (int(shape.p1[0]), int(shape.p1[1])), 
                                           (int(shape.p2[0]), int(shape.p2[1])), width)
    elif checkShpType(shape, Arc):
        _pygame.draw.arc(surface, colour, 
                         (int(shape.x)-int(shape.r), int(shape.y)-int(shape.r), int(shape.r*2), int(shape.r*2)), 
                         _toRadians(-shape.endAng), _toRadians(-shape.startAng), width)
    elif checkShpType(shape, Circle):
        _pygame.draw.circle(surface, colour, (int(shape.x), int(shape.y)), int(shape.r), width)
    elif checkShpType(shape, ShpGroups.CLOSED):
        ps = shape.toPoints()
        psset = {tuple(i) for i in ps}
        if len(psset) == 0:
            return
        elif len(psset) == 1:
            fst = psset.pop()
            _pygame.draw.circle(surface, colour, (int(fst[0]), int(fst[1])), int(width/2))
        elif len(psset) == 2:
            fst = psset.pop()
            snd = psset.pop()
            _pygame.draw.line(surface, colour, 
                              (int(fst[0]), int(fst[1])), 
                              (int(snd[0]), int(snd[1])), int(width/4*3))
        _pygame.draw.polygon(surface, colour, ps, width)
    elif checkShpType(shape, ShpGroups.GROUP):
        for i in shape.shapes:
            drawShape(surface, i, colour, width)
    else:
        raise ValueError(f'Cannot draw BlazeSudio shape of type {type(shape)}')

class ShapeCombiner(ShapeCombiner): # Override the ShapeCombiner class to add some extra methods that use shapely (so cannot be compiled)
    @staticmethod
    def pointsToPoly(*points: list[Point], ratio: Number = 0.1) -> Union[Shape, Shapes]:
        """
        Converts a list of points to a polygon.
        This differs from `ShapeCombiner.pointsToShape` in that **this** will create a polygon encapsulating all the points, \
*instead* of connecting them all with lines.

        Args:
            points (list[Point]): The points to convert to a polygon.
            ratio (Number): A number in the range [0, 1]. Higher means fewer verticies/less detail.

        Returns:
            Shape | Shapes: A Shapes object containing one polygon with the points from the input.
        """
        return shapelyToColl(_shapely.concave_hull(_shapelyGeom.MultiPoint([tuple(i) for i in points]), ratio=ratio))
    
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
