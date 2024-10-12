from shapely import concave_hull
from shapely.geometry import MultiPoint, LineString
import BlazeSudio.collisions as colls

def approximate_polygon(surface, tolerance=3, ratio=0.1):
    """
    Returns a concave polygon that approximates the non-transparent area of a Pygame surface.
    :param tolerance: Controls how closely the algorithm will match the shape (lower is more detailed).
    :param ratio: A number in the range [0, 1]. Higher means fewer verticies.
    """
    non_transparent_points = []
    width, height = surface.get_size()
    
    # Scan the surface to find non-transparent points
    for x in range(0, width, tolerance):
        for y in range(0, height, tolerance):
            color = surface.get_at((x, y))
            if color.a == 255 and (color.r != 0 and color.g != 0 and color.b != 0):
                non_transparent_points.append((x, y))
    
    polygon_points = []
    for point in non_transparent_points:
        def check(x, y):
            return (x, y) not in non_transparent_points
        if (
            check(point[0] + tolerance, point[1]) or
            check(point[0], point[1] + tolerance) or
            check(point[0] - tolerance, point[1]) or
            check(point[0], point[1] - tolerance)
        ):
            polygon_points.append(point)
    
    return colls.
