# Contrary to the fact that this is unittest.py, we will not use the unittest library.
# This is intended for development, not practical use.

def testCollisions():
    from BlazeSudio.utils import collisions
    print(collisions.handleCollisions([2, 0], [0, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4))))
    # . = current pos, N = new pos
    #  .
    #+--+
    #| N|
    #|  |
    #+--+

if __name__ == "__main__":
    testCollisions()
