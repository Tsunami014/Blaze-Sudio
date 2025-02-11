import BlazeSudio.collisions as colls
import numpy as np
import pygame

__all__ = [
    "bounding_box",
    "approximate_polygon"
]

def bounding_box(surface):
    """
    Simplifies a polygon into 4 points.

    Args:
        surface (pygame.Surface): The surface to simplify.
    """
    width, height = surface.get_size()
    points = []
    for x in range(width):
        for y in range(height):
            if surface.get_at((x, y)).a > 125:
                points.append((x, y))
    if not points:
        return None
    
    xs, ys = zip(*points)
    x1 = min(xs)
    x2 = max(xs)
    y1 = min(ys)
    y2 = max(ys)
    if x2 == width-1:
        x2 = width
    if y2 == height-1:
        y2 = height
    return colls.Polygon((x1, y1), (x2, y1), (x2, y2), (x1, y2))

def corners(surface: pygame.Surface):
    alphas = pygame.surfarray.array_alpha(surface)
    rows = [np.any(i) for i in alphas.T]
    cols = [np.any(i) for i in alphas]

    if not np.any(rows+cols):
        return []

    points = []
    topR = None
    for idx, r in enumerate(rows):
        if r:
            topR = idx
            break
    else:
        return []
    botR = None
    for idx, r in enumerate(rows[::-1]):
        if r:
            botR = len(rows)-idx
            break
    else:
        return []
    for r, dir, off in ((topR, 1, 0), (botR, -1, -1)):
        for dir2 in (1, -1)[::dir]:
            col = None
            li = alphas.T[r+off][::dir2]
            for idx, c in enumerate(li):
                if c:
                    if dir2 == -1:
                        col = len(li)-idx
                    else:
                        col = idx
                    break
            else:
                return []
            points.append((col, r))
    return colls.Polygon(*points)

def approximate_polygon(surface, tolerance=3, ratio=0.1): # TODO: Seriously boost performance
    """
    Returns a concave polygon that approximates the non-transparent area of a Pygame surface.
    :param tolerance: Controls how closely the algorithm will match the shape (lower is more detailed).
    :param ratio: A number in the range [0, 1]. Higher means fewer verticies.
    """
    non_transparent_points = []
    polygon_points = []
    width, height = surface.get_size()

    def check_col(col):
        return col.a > 125
    
    # Scan the surface to find non-transparent points
    for x in range(0, width, tolerance):
        for y in range(0, height, tolerance):
            if check_col(surface.get_at((x, y))):
                non_transparent_points.append((x, y))
    non_transparent_points = set(non_transparent_points)
    
    for point in non_transparent_points:
        def check(x, y):
            return (x, y) not in non_transparent_points
        if (
            check(point[0] + tolerance, point[1]) or
            check(point[0], point[1] + tolerance) or
            check(point[0] - tolerance, point[1]) or
            check(point[0], point[1] - tolerance)
        ):
            if point[0] == width-width%tolerance:
                point = (width, point[1])
            if point[1] == height-height%tolerance:
                point = (point[0], height)
            polygon_points.append(point)
    
    return colls.ShapeCombiner.pointsToPoly(*polygon_points, ratio=ratio)
