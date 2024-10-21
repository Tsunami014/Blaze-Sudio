# Contrary to the fact that this is debugunittest.py, we will not use the unittest library.
# This is intended for development, not practical use.

from BlazeSudio.debug import collisions # Use this more because it is the exact latest version
# from BlazeSudio import collisions # Use this **instead** if you want to use the compiled version
import time
print()

def Debug(names, ins, outs, expecteds, formatter, highlights=None):
    if len(ins) != len(outs) or len(outs) != len(expecteds) or len(expecteds) != len(names):
        raise ValueError('All inputs must be the same length.')
    
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
        highlight_line = ' ' * 10  # Initial spaces for alignment
        prevlns = 0
        # HACK: This won't be a problem unless you have a stupid amount of inputs
        ln = formatter([chr(i) * max_lens[i] for i in range(len(ins))])  # Call formatter to get the max length of the line
        for h in highlights:
            new = ' ' * (ln.index(chr(h))-prevlns) + '^' * max_lens[h]
            highlight_line += new
            prevlns += len(new)
        print(highlight_line)
    else:
        print()

def RoundAny(t):
    if isinstance(t, (tuple, list)):
        return type(t)(RoundAny(x) for x in t)
    return round(t, 2)

def Check(testName, names, ins, outs, expecteds, formatter):
        if len(ins) != len(outs) or len(outs) != len(expecteds) or len(expecteds) != len(names):
            raise ValueError('All inputs must be the same length.')
        
        errors = []
        errortxts = []
        for i in range(len(ins)):
            if RoundAny(outs[i]) != expecteds[i]:
                errors.append(i)
                errortxts.append(f'In {names[i]}: expected {expecteds[i]}, got {outs[i]}')
        if errors != []:
            print(f'TEST {testName} FAILED:')
            Debug(
                names,
                ins,
                outs,
                expecteds,
                formatter,
                errors
            )
            raise AssertionError(
                ' &\n'.join(errortxts)
            )

def Timeit(func, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    print(f'Time taken: {(time.time() - start)*1000} ms.')

def CompareTimes(func1, func2, *args, **kwargs):
    start = time.time()
    func1(*args, **kwargs)
    f1Time = time.time() - start
    start = time.time()
    func2(*args, **kwargs)
    f2Time = time.time() - start
    f1Time *= 1000
    f2Time *= 1000
    print(f'Time taken for func1: {f1Time} ms, time taken for func2: {f2Time} ms.')
    print(f'Difference: {abs(f1Time - f2Time)} ms.')
    if f1Time == 0 or f2Time == 0:
        return
    if f1Time > f2Time:
        print(f'Func1 is {f2Time/f1Time} times faster than func2.')
    else:
        print(f'Func2 is {f1Time/f2Time} times faster than func1.')

def testAll():
    # If these fail there is a big issue
    assert collisions.rotate([0, 0], [123, 456], 127.001) == collisions.rotateBy0([123, 456], 127.001)
    assert RoundAny(collisions.rotate([1, 0], [1, -1], 90)) == (2, 0)

    # Test points and circles
    def testPoint(testName, outs, expected1, expected2, ins):
        Check(testName, 
            ['x', 'y', 'accelx', 'accely'], 
            ins, 
            [outs[0][0], outs[0][1], outs[1][0], outs[1][1]], 
            [*expected1, *expected2], 
            lambda li: f'({li[0]}, {li[1]}), [{li[2]}, {li[3]}]'
        )
    
    testPoint('Perfect rebound',
            collisions.Point(2, 0).handleCollisionsVel([0, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1))), 
            (2, 0), # It rebounded perfectly and now is exactly where it started
            (0, -2), # It is now going the opposite direction
            (2, 0, 0, 2))
    # . = current pos, N = new pos
    #  .
    #+--+
    #| N|
    #|  |
    #+--+
    testPoint('Perfect rebound 2 - side',
            collisions.Point(0, 2).handleCollisionsVel([2, 0], collisions.Shapes(collisions.Rect(1, 0, 4, 4, 1))),
            (0, 2), # It rebounded perfectly and now is exactly where it started
            (-2, 0), # It is now going the opposite direction
            (0, 2, 2, 0))
    # . = current pos, N = new pos
    # +--+
    # |  |
    #.|N |
    # +--+
    testPoint('v shape',
            collisions.Point(0, 0).handleCollisionsVel([2, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1))),
            (2, 0), # It rebounded like a v shape
            (2, -2),
            (0, 0, 2, 2))
    # . = current pos, N = new pos
    #.
    #+--+
    #| N|
    #|  |
    #+--+
    
    testPoint('Rebound top',
            collisions.Circle(2, 0, 1).handleCollisionsVel([0, 2], collisions.Shapes(collisions.Rect(0, 2, 4, 4, 1))), 
            (2, 0),
            (0, -2), # It is now going the opposite direction
            (2, 0, 0, 2))
    # . = current pos, N = new pos
    #  .
    #+--+
    #| N|
    #|  |
    #+--+
    # TODO: More tests
    # testPoint('Perfect rebound 2 - side',
    #         collisions.Circle(0, 2).handleCollisionsVel([2, 0], collisions.Shapes(collisions.Rect(1, 0, 4, 4, 1))),
    #         (0, 2), # It rebounded perfectly and now is exactly where it started
    #         (-2, 0), # It is now going the opposite direction
    #         (0, 2, 2, 0))
    # . = current pos, N = new pos
    # +--+
    # |  |
    #.|N |
    # +--+
    # testPoint('v shape',
    #         collisions.Circle(0, 0).handleCollisionsVel([2, 2], collisions.Shapes(collisions.Rect(0, 1, 4, 4, 1))),
    #         (2, 0), # It rebounded like a v shape
    #         (2, -2),
    #         (0, 0, 2, 2))
    # . = current pos, N = new pos
    #.
    #+--+
    #| N|
    #|  |
    #+--+

    # Test lines
    def testLine(testName, line, accel, shapes, expectedp1, expectedp2, expectedaccel, expectedtype):
        outLine, outaccel, v = collisions.Line(*line).handleCollisionsVel(accel, collisions.Shapes(*shapes), verbose=True)
        Check(testName, 
              ['p1x', 'p1y', 'p2x', 'p2y', 'accelx', 'accely', 'type'], 
              [*line[0], *line[1], *accel, 'N/A'], 
              [*outLine[0], *outLine[1], *outaccel, v[0]], 
              [*expectedp1, *expectedp2, *expectedaccel, expectedtype], 
              lambda li: f'({li[0]}, {li[1]}), ({li[2]}, {li[3]}), ({li[4]}, {li[5]}), {li[6]}'
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

    # TIMING
    shp1 = collisions.RotatedRect(0, 0, 1, 1, 45)
    shp2 = collisions.Polygon((0.5, 0), (1, 0.5), (0.5, 1), (0, 0.5))
    CompareTimes(shp1.handleCollisionsVel, shp2.handleCollisionsVel, [1, 1], collisions.Shapes(collisions.Rect(-99, 0, 10, 19)))

if __name__ == "__main__":
    testAll()
    print('\nIT ALL WORKS YAY')
