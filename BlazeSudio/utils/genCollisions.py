import BlazeSudio.collisions as colls

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
