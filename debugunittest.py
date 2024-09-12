# Contrary to the fact that this is unittest.py, we will not use the unittest library.
# This is intended for development, not practical use.

# This is the debug statement. If you wanted to use the compiled class, run `import BlazeSudio.collisions` instead.
from BlazeSudio.collisions.lib import collisions

def debug(names, ins, outs, expecteds, formatter, offsets, highlights=None):
    sins = [str(i) for i in ins]
    souts = [str(i) for i in outs]
    sxpecteds = [str(i) for i in expecteds]

    def adjust(t, ln):
        return t + ' ' * (ln - len(t))
        # return ' ' * ((ln - len(t)) // 2) + t + ' ' * ((ln - len(t) + 1) // 2)
    
    ls = [names, sins, souts, sxpecteds]
    max_lens = [max(len(j[i]) for j in ls) for i in range(len(sins))]
    names, ins, outs, expecteds = ([adjust(i[j],max_lens[j]) for j in range(len(i))] for i in ls)
    
    print('          '+formatter(names))
    print('In:       '+formatter(ins))
    print('Out:      '+formatter(outs))
    print('Expected: '+formatter(expecteds))
    
    if highlights is not None:
        # Calculate the position of the highlight
        highlight_positions = [sum(max_lens[:i]) + 2 * i + 1 for i in range(len(ins))]
        highlight_line = ' ' * 11  # Initial spaces for alignment
        prevlns = 0
        for h in highlights:
            new = ' ' * (highlight_positions[h]+offsets[h]-prevlns) + '^' * max_lens[h]
            highlight_line += new
            prevlns += len(new)
        print(highlight_line)
    else:
        print()

def roundTuple(t):
    return tuple(round(x, 2) for x in t)

def testCollisions():
    assert collisions.rotate([0, 0], [123, 456], 127.001) == collisions.rotateBy0([123, 456], 127.001)
    assert roundTuple(collisions.rotate([1, 0], [1, -1], 90)) == (2, 0)
    
    outpos, outaccel = collisions.Point(2, 0).handleCollisionsAccel([0, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1)))
    assert roundTuple(outpos) == (2, 0) # It rebounded perfectly and now is exactly where it started
    assert roundTuple(outaccel) == (0, -2) # It is now going the opposite direction
    # . = current pos, N = new pos
    #  .
    #+--+
    #| N|
    #|  |
    #+--+
    outpos, outaccel = collisions.Point(0, 2).handleCollisionsAccel([2, 0], collisions.Shapes(collisions.Rect(1, 0, 4, 4, 1)))
    assert roundTuple(outpos) == (0, 2) # It rebounded perfectly and now is exactly where it started
    assert roundTuple(outaccel) == (-2, 0) # It is now going the opposite direction
    # . = current pos, N = new pos
    # +--+
    # |  |
    #.|N |
    # +--+
    outpos, outaccel = collisions.Point(0, 0).handleCollisionsAccel([2, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1)))
    assert roundTuple(outpos) == (2, 0) # It rebounded like a v shape
    assert roundTuple(outaccel) == (2, -2)
    # . = current pos, N = new pos
    #.
    #+--+
    #| N|
    #|  |
    #+--+

    def testLine(testName, line, accel, shapes, expectedp1, expectedp2, expectedaccel, expectedtype):
        outLine, outaccel, v = collisions.Line(*line).handleCollisionsAccel(accel, collisions.Shapes(*shapes), verbose=True)
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
        if v[0] != expectedtype:
            errors.append(6)
            errortxts.append(f'In type: Expected a collision type of {expectedtype}, got {v[0]}')
        if errors != []:
            print(f'TEST {testName} FAILED:')
            debug(
                ['p1x', 'p1y', 'p2x', 'p2y', 'accelx', 'accely', 'type'],
                [*line[0], *line[1], *accel, 'N/A'],
                [*outLine[0], *outLine[1], *outaccel, v[0]],
                [*expectedp1, *expectedp2, *expectedaccel, expectedtype],
                lambda li: f'[({li[0]}, {li[1]}), ({li[2]}, {li[3]})], ({li[4]}, {li[5]}), {li[6]}',
                [0, 0, 2, 2, 5, 5, 6],
                errors
            )
            raise AssertionError(
                ' &\n'.join(errortxts)
            )
    
    # Types of collisions:
    # 0: Point off point collision
    # 1: Point off line collision
    # 2: Line off point collision
    # 3: Line off line collision
    
    testLine('Basic point off line',
             ((1, 0), (2, -1)), [0, 3], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1)),
             (1, -1), (2, -2), (0, -3), 1)
    # /
    #+--+
    #|  |
    #|  |
    #+--+

    testLine('Basic point off line 2: points reversed',
             ((2, -1), (1, 0)), [0, 3], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1)),
             (1, -1), (2, -2), (0, -3), 1)
    # /
    #+--+
    #|  |
    #|  |
    #+--+

    testLine('Basic point off line 3: closer to rect',
             ((1, 0.9), (2, 0)), [0, 0.3], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1)),
             (1, 0.8), (2, -0.1), (0, -0.3), 1)
    # /
    #+--+
    #|  |
    #|  |
    #+--+

    testLine('Basic point off line 4: further from rect',
             ((2, -3), (4, -4)), [0, 6], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1)),
             (2, -1), (4, -2), (0, -6), 1)
    # /
    #+--+
    #|  |
    #|  |
    #+--+

    testLine('V shape bounce point off line',
             ((0, 0), (1, -1)), [2, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1)),
             (2, 0), (3, -1), (2, -2), 1)
    #/v/
    #+--+
    #|  |
    #|  |
    #+--+

    testLine('Non-basic copied from a (hopefully previously) incorrect scenario in demos.py',
             ((620.52, 584), (670.52, 684)), [-3.52, 0], collisions.Shapes(collisions.Rect(520, 547, 100, 100, 1)),
             (623, 584), (673, 684), (3.52, 0), 1)
    #+--+
    #|  |
    #|  |/
    #+--+

    testLine('Line bounce off another paralell line',
             ((0, 1), (1, 0)), [0, 2], collisions.Shapes(collisions.Line((0, 2), (1, 1), 1)),
             (-1, 2), (0, 1), (-2, 0), 3)
    #/
    #/

    testLine('Line bounce off rect corner',
             ((0, 1), (1, 0)), [1, 1], collisions.Shapes(collisions.Rect(1, 1, 4, 4, 1)),
             (0, 1), (1, 0), (-1, -1), 2)
    #/+--+
    # |  |
    # |  |
    # +--+

def testCombine():
    def testCombine(testName, shapes, expected):
        out = collisions.combine(*shapes)
        if out != expected:
            debug( # TODO: Make better
                ['Shape 1', 'Shape 2'],
                [str(shapes[0]), str(shapes[1])],
                [str(out), str(expected)],
                [str(expected), str(expected)],
                lambda li: li,
                [0, 0],
                [0, 1]
            )
            raise AssertionError(f'Test {testName} failed: Expected {expected}, got {out}')
    
    # This is stupidly hard to wrap my head around for making test cases. 
    #testCombine('2 squares', 
    #            [collisions.Rect(0, 0, 1, 1), collisions.Rect(0.5, 0.5, 1, 1)]\
    #            [collisions.Polygon([(0, 0), (1, 0), (1, 0.5), (1.5, 0.5), (1.5, 1.5), (0.5, 1.5),])]
    #)

if __name__ == "__main__":
    testCollisions()
    print('IT ALL WORKS YAY')
