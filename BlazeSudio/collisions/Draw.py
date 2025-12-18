from .core import checkShpType, ShpTyps, ShpGroups, Shape
import pygame
import math

def drawShape(surface, shape: Shape, colour: tuple[int, int, int], width: int = 0):
    """
    Draws a BlazeSudio shape to a Pygame surface.

    Args:
        surface (pygame.Surface): The surface to draw the shape on.
        shape (Shape): The shape to draw.
        colour (tuple[int, int, int]): The colour to draw the shape in.
        width (int, optional): The width of the lines to draw. Defaults to 0.
    """
    if checkShpType(shape, ShpTyps.Point):
        pygame.draw.circle(surface, colour, (int(shape.x), int(shape.y)), width)
    elif checkShpType(shape, ShpTyps.Line):
        if tuple(shape.p1) == tuple(shape.p2):
            pygame.draw.circle(surface, colour, (int(shape.p1[0]), int(shape.p1[1])), int(width/2))
        pygame.draw.line(surface, colour, (int(shape.p1[0]), int(shape.p1[1])), 
                                           (int(shape.p2[0]), int(shape.p2[1])), width)
    elif checkShpType(shape, ShpTyps.Arc):
        pygame.draw.arc(surface, colour, 
                         (int(shape.x-shape.r + width/2), int(shape.y-shape.r - width/2), int(shape.r*2 - width), int(shape.r*2 - width)), 
                         math.radians(-shape.endAng - width/2), math.radians(-shape.startAng + width/2), width)
    elif checkShpType(shape, ShpTyps.Circle):
        pygame.draw.circle(surface, colour, (int(shape.x), int(shape.y)), int(shape.r), width)
    elif checkShpType(shape, ShpGroups.CLOSED):
        ps = shape.toPoints()
        psset = {tuple(i) for i in ps}
        if len(psset) == 0:
            return
        elif len(psset) == 1:
            fst = psset.pop()
            pygame.draw.circle(surface, colour, (int(fst[0]), int(fst[1])), int(width/2))
        elif len(psset) == 2:
            fst = psset.pop()
            snd = psset.pop()
            pygame.draw.line(surface, colour, 
                              (int(fst[0]), int(fst[1])), 
                              (int(snd[0]), int(snd[1])), int(width/4*3))
        pygame.draw.polygon(surface, colour, ps, width)
    elif checkShpType(shape, ShpGroups.GROUP):
        for i in shape.shapes:
            drawShape(surface, i, colour, width)
    elif checkShpType(shape, ShpTyps.NoShape):
        pass
    else:
        raise ValueError(f'Cannot draw BlazeSudio shape of type {type(shape)}')
