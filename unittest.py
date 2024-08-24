# Contrary to the fact that this is unittest.py, we will not use the unittest library.
# This is intended for development, not practical use.

def testCollisions():
    from BlazeSudio.utils import collisions
    def roundTuple(t):
        return tuple(round(x) for x in t)
    outpos, outaccel = collisions.handleCollisions([2, 0], [0, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4)))
    assert roundTuple(outpos) == (2, 0) # It rebounded perfectly and now is exactly where it started
    assert roundTuple(outaccel) == (0, -2) # It is now going the opposite direction
    # . = current pos, N = new pos
    #  .
    #+--+
    #| N|
    #|  |
    #+--+
    outpos, outaccel = collisions.handleCollisions([0, 2], [2, 0], collisions.Shapes(collisions.Rect(1, 0, 4, 4)))
    assert roundTuple(outpos) == (0, 2) # It rebounded perfectly and now is exactly where it started
    assert roundTuple(outaccel) == (-2, 0) # It is now going the opposite direction
    # . = current pos, N = new pos
    # +--+
    # |  |
    #.|N |
    # +--+
    print('IT ALL WORKS YAY')

if __name__ == "__main__":
    testCollisions()
