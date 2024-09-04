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

    def testLine(line, accel, shapes, expectedp1, expectedp2, expectedaccel):
        outLine, outaccel = collisions.Line(*line).handleCollisionsAccel(accel, collisions.Shapes(*shapes))
        def debug():
            ins = [str(accel[0]), str(accel[1])]
            outs = [str(i) for i in [outLine.p1[0], outLine.p1[1], outaccel[0], outaccel[1]]]
            expecteds = [str(i) for i in [expectedp1[0], expectedp1[1], expectedaccel[0], expectedaccel[1]]]
            print(f'In:       {str(line):<{sum(len(i) for i in outs)+2}} ({ins[0]:<{max(len(outs[2]), len(expecteds[2]), len(ins[0]))}}, {ins[1]:<{max(len(outs[3]), len(expecteds[3]), len(ins[1]))}})')
            print(f'Out:      ({outs[0]:<{max(len(outs[0]), len(expecteds[0]))}}, {outs[1]:<{max(len(outs[1]), len(expecteds[1]))}}) ({outs[2]:<{max(len(outs[2]), len(expecteds[2]), len(ins[0]))}}, {outs[3]:<{max(len(outs[3]), len(expecteds[3]), len(ins[1]))}})')
            print(f'Expected: ({expecteds[0]:<{max(len(outs[0]), len(expecteds[0]))}}, {expecteds[1]:<{max(len(outs[1]), len(expecteds[1]))}}) ({expecteds[2]:<{max(len(outs[2]), len(expecteds[2]), len(ins[0]))}}, {expecteds[3]:<{max(len(outs[3]), len(expecteds[3]), len(ins[1]))}})')
        # debug()
        assert roundTuple(outLine.p1) == expectedp1
        assert roundTuple(outLine.p2) == expectedp2
        assert roundTuple(outaccel) == expectedaccel
    
    testLine(((1, 0), (2, -1)), [0, 3], collisions.Shapes(collisions.Rect(0, 1, 4, 4)),
             (1, -1), (2, -2), (0, -3))
    # /
    #+--+
    #|  |
    #|  |
    #+--+

    testLine(((2, -1), (1, 0)), [0, 3], collisions.Shapes(collisions.Rect(0, 1, 4, 4)),
             (1, -1), (2, -2), (0, -3))
    # /
    #+--+
    #|  |
    #|  |
    #+--+

    testLine(((0, 0), (1, -1)), [2, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4)),
             (2, 0), (3, -1), (2, -2))
    #/v/
    #+--+
    #|  |
    #|  |
    #+--+

    testLine(((0, 1), (1, 0)), [1, 1], collisions.Shapes(collisions.Rect(0.5, 0.5, 4, 4)),
             (0, 1), (1, 0), (-1, -1))
    #/+--+
    # |  |
    # |  |
    # +--+

    print('IT ALL WORKS YAY')

if __name__ == "__main__":
    testCollisions()
