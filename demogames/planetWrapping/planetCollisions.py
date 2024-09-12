from shapely import concave_hull
from shapely.geometry import MultiPoint
from BlazeSudio.collisions import Polygon

def approximate_polygon(surface, tolerance=3, ratio=0.1):
    """
    Returns a concave polygon that approximates the non-transparent area of the surface.
    :param tolerance: Controls how closely the algorithm will match the shape (lower is more detailed).
    :param ratio: A number in the range [0, 1]. Higher means fewer verticies
    """
    non_transparent_points = []
    width, height = surface.get_size()
    
    # Scan the surface to find non-transparent points
    for x in range(0, width, tolerance):
        for y in range(0, height, tolerance):
            color = surface.get_at((x, y))
            if color.a == 255:
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

    hull = concave_hull(MultiPoint(polygon_points), ratio=ratio)

    return Polygon(*list(zip(*[list(i) for i in hull.exterior.coords.xy])))
