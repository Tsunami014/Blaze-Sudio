# Contrary to the fact that this is unittest.py, we will not use the unittest library.
# This is intended for development, not practical use.

def testCollisions():
    from BlazeSudio.utils import collisions
    def roundTuple(t):
        return tuple(round(x, 2) for x in t)
    
    assert collisions.rotate([0, 0], [123, 456], 127.001) == collisions.rotateBy0([123, 456], 127.001)
    assert roundTuple(collisions.rotate([1, 0], [1, -1], 90)) == (2, 0)
    
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
        
        def debug(highlights=None):
            ins = [str(i) for i in [line[0][0], line[0][1], line[1][0], line[1][1], accel[0], accel[1]]]
            outs = [str(i) for i in [outLine[0][0], outLine[0][1], outLine[1][0], outLine[1][1], outaccel[0], outaccel[1]]]
            expecteds = [str(i) for i in [expectedp1[0], expectedp1[1], expectedp2[0], expectedp2[1], expectedaccel[0], expectedaccel[1]]]
            
            max_lens = [max(len(ins[i]), len(outs[i]), len(expecteds[i])) for i in range(len(ins))]
            ins, outs, expecteds = ([f'{i[j]:<{max_lens[j]}}' for j in range(len(i))] for i in [ins, outs, expecteds])
            def formatLi(li):
                return f'[({li[0]}, {li[1]}), ({li[2]}, {li[3]})], ({li[4]}, {li[5]})'
            
            print('In:       '+formatLi(ins))
            print('Out:      '+formatLi(outs))
            print('Expected: '+formatLi(expecteds))
            
            if highlights is not None:
                # Calculate the position of the highlight
                highlight_positions = [sum(max_lens[:i]) + 2 * i + 1 for i in range(len(ins))]
                offsets = [0, 0, 2, 2, 5, 5]
                highlight_line = ' ' * 11  # Initial spaces for alignment
                prevlns = 0
                for h in highlights:
                    new = ' ' * (highlight_positions[h]+offsets[h]-prevlns) + '^' * max_lens[h]
                    highlight_line += new
                    prevlns += len(new)
                print(highlight_line)
        
        # debug()
        errors = []
        errortxts = []
        if roundTuple(outLine[0]) != expectedp1:
            errors.extend([0, 1])
            errortxts.append(f'In p1: Expected {expectedp1}, got {outLine[0]}')
        if roundTuple(outLine[1]) != expectedp2:
            errors.extend([2, 3])
            errortxts.append(f'In p2: Expected {expectedp2}, got {outLine[1]}')
        if roundTuple(outaccel) != expectedaccel:
            errors.extend([4, 5])
            errortxts.append(f'In accel: Expected {expectedaccel}, got {outaccel}')
        if errors != []:
            debug(errors)
            raise AssertionError(
                ' &\n'.join(errortxts)
            )
    
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

    testLine(((1, 0.9), (2, 0)), [0, 0.3], collisions.Shapes(collisions.Rect(0, 1, 4, 4)),
             (1, 0.8), (2, -0.1), (0, -0.3))
    # /
    #+--+
    #|  |
    #|  |
    #+--+

    testLine(((2, -3), (4, -4)), [0, 6], collisions.Shapes(collisions.Rect(0, 1, 4, 4)),
             (2, -1), (4, -2), (0, -6))
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
