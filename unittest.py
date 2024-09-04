# Contrary to the fact that this is unittest.py, we will not use the unittest library.
# This is intended for development, not practical use.

def testCollisions():
    from BlazeSudio.utils import collisions
    def roundTuple(t):
        return tuple(round(x, 2) for x in t)
    outpos, outaccel = collisions.Point(2, 0).handleCollisionsAccel([0, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4)))
    assert roundTuple(outpos) == (2, 0) # It rebounded perfectly and now is exactly where it started
    assert roundTuple(outaccel) == (0, -2) # It is now going the opposite direction
    # . = current pos, N = new pos
    #  .
    #+--+
    #| N|
    #|  |
    #+--+
    outpos, outaccel = collisions.Point(0, 2).handleCollisionsAccel([2, 0], collisions.Shapes(collisions.Rect(1, 0, 4, 4)))
    assert roundTuple(outpos) == (0, 2) # It rebounded perfectly and now is exactly where it started
    assert roundTuple(outaccel) == (-2, 0) # It is now going the opposite direction
    # . = current pos, N = new pos
    # +--+
    # |  |
    #.|N |
    # +--+
    outpos, outaccel = collisions.Point(0, 0).handleCollisionsAccel([2, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4)))
    assert roundTuple(outpos) == (2, 0) # It rebounded like a v shape
    assert roundTuple(outaccel) == (2, -2)
    # . = current pos, N = new pos
    #.
    #+--+
    #| N|
    #|  |
    #+--+

    outLine, outaccel = collisions.Line((1, 0), (2, -1)).handleCollisionsAccel([0, 3], collisions.Shapes(collisions.Rect(0, 1, 4, 4)))
    assert roundTuple(outLine.p1) == (1, -1)
    assert roundTuple(outLine.p2) == (2, -2)
    assert roundTuple(outaccel) == (0, -3)
    # /
    #+--+
    #|  |
    #|  |
    #+--+

    outLine, outaccel = collisions.Line((2, -1), (1, 0)).handleCollisionsAccel([0, 3], collisions.Shapes(collisions.Rect(0, 1, 4, 4)))
    assert roundTuple(outLine.p1) == (1, -1)
    assert roundTuple(outLine.p2) == (2, -2)
    assert roundTuple(outaccel) == (0, -3)
    # /
    #+--+
    #|  |
    #|  |
    #+--+

    outLine, outaccel = collisions.Line((0, 0), (2, -2)).handleCollisionsAccel([0, 3], collisions.Shapes(collisions.Rect(0, 1, 4, 4)))
    assert roundTuple(outLine.p1) == (1, -1)
    assert roundTuple(outLine.p2) == (2, -2)
    assert roundTuple(outaccel) == (0, -3)
    # /
    #/
    # +--+
    # |  |
    # |  |
    # +--+

    print('IT ALL WORKS YAY')

if __name__ == "__main__":
    testCollisions()
