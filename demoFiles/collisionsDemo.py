from BlazeSudio import collisions
from BlazeSudio.graphics.options import CRAINBOWCOLOURS, FREGULAR
import pygame
import math
pygame.init()
win = pygame.display.set_mode()
run = True
header_opts = ['point', 'line', 'arc', 'circle', 'rect', 'rotated rect', 'polygon', 'eraser', 'combiner', 'help']
types = [collisions.Point, collisions.Line, collisions.Arc, collisions.Circle, collisions.Rect, collisions.RotatedRect, collisions.Polygon, collisions.NoShape]
font = pygame.font.Font(None, 36)
header_sze = 50
typ = 0
curObj: collisions.Shape = collisions.Point(0, 0)
objs = collisions.Shapes()
dir = [0, 0, 0]
combineTyp = 0
pos = [0, 0]
vel = [0, 0]
combineFs = {
    'CollsUnion': collisions.ShapeCombiner.union,
    'ShapelyUnion': collisions.ShapeCombiner.shapelyUnion,
    'BoundingBox': collisions.ShapeCombiner.boundingBox,
    'CombineRects': collisions.ShapeCombiner.combineRects,
    'PointsToShape': collisions.ShapeCombiner.pointsToShape,
    'PointsToPoly': collisions.ShapeCombiner.pointsToPoly
}
highlightTyps = [
    (collisions.Line, collisions.ClosedShape),
    (collisions.Shape),
    (collisions.Shape),
    (collisions.Rect),
    (collisions.Point),
    (collisions.Point)
]
combineCache = [None, None]

def findCombinedOutput():
    global combineCache
    toCombineObjs = [o for o in objs if isinstance(o, highlightTyps[combineTyp]) and o.collides(curObj)]
    cacheCheck = (toCombineObjs, combineTyp)
    if combineCache[0] == cacheCheck:
        return combineCache[1]
    else:
        combined = combineFs[list(combineFs.keys())[combineTyp]](*toCombineObjs)
        ret = (combined, toCombineObjs)
        combineCache = [cacheCheck, ret]
        return ret

def drawObj(obj, t, col):
    if t == 8: # As well as drawing the point, outline the shapes to be combined
        combined, objsToCombine = findCombinedOutput()
        if isinstance(combined, collisions.Shape):
            combined = [combined]
        for o in objsToCombine:
            drawObj(o, types.index(type(o)), (255, 110, 60))
        for o in combined:
            drawObj(o, types.index(type(o)), (244, 194, 194, 200))
    if t == 7:
        col = (255, 255, 255)
        # Outline shapes to be deleted
        for o in objs:
            if curObj.collides(o):
                drawObj(o, types.index(type(o)), (255, 110, 60))
    collisions.drawShape(win, obj, col, 8)

def moveCurObj(curObj):
    if typ == 1:
        curObj.p1 = pos
        curObj.p2 = (curObj.p1[0]+dir[0], curObj.p1[1]+dir[1])
    elif typ == 6:
        moveAll = pygame.key.get_pressed()[pygame.K_PERIOD] or playMode
        if isinstance(curObj, collisions.Point):
            curObj.x, curObj.y = pos
        elif isinstance(curObj, collisions.Line):
            if moveAll:
                curObj.p1 = [curObj.p1[0]-curObj.p2[0]+pos[0], curObj.p1[1]-curObj.p2[1]+pos[1]]
            curObj.p2 = pos
        else:
            if moveAll:
                diff = (curObj.points[-1][0]-pos[0], curObj.points[-1][1]-pos[1])
                curObj.points = [(p[0]-diff[0], p[1]-diff[1]) for p in curObj.points[:-1]] + [pos]
            else:
                curObj.points[-1] = pos
    else:
        curObj.x, curObj.y = pos
        if typ in (2, 3):
            curObj.r = dir[1]
        elif typ in (4, 5, 7, 8):
            curObj.w, curObj.h = dir[0], dir[1]
            if typ == 5:
                curObj.rot = dir[2]
        if typ == 2:
            dir[0], dir[2] = dir[0] % 360, dir[2] % 360
            curObj.startAng, curObj.endAng = dir[0], dir[2]
    return curObj

def offsetColour(obj, col):
    r, g, b = col
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    mx, mn = max(r, g, b), min(r, g, b)
    df = mx - mn

    # Calculate hsv
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g - b) / df) + 360) % 360
    elif mx == g:
        h = (60 * ((b - r) / df) + 120) % 360
    elif mx == b:
        h = (60 * ((r - g) / df) + 240) % 360
    s = 0 if mx == 0 else df / mx
    v = mx

    # modify h
    h = (h + obj.bounciness * 40) % 360

    # Convert HSV back to RGB
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x

    r, g, b = (r + m) * 255, (g + m) * 255, (b + m) * 255
    return int(r), int(g), int(b)

clock = pygame.time.Clock()
while run:
    playMode = pygame.key.get_mods() & pygame.KMOD_ALT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                break
            elif event.key == pygame.K_SPACE:
                if typ == 7:
                    for i in objs.copy_leave_shapes():
                        if i.collides(curObj):
                            objs.remove_shape(i)
                elif typ == 8:
                    new, toRemove = findCombinedOutput()
                    objs.remove_shapes(*toRemove)
                    objs.add_shapes(*new)
                else:
                    objs.add_shape(curObj)
                    if typ == 6:
                        curObj = curObj = collisions.Point(*pygame.mouse.get_pos())
                    else:
                        curObj = curObj.copy()
            elif event.key == pygame.K_COMMA and typ == 6:
                if isinstance(curObj, collisions.Point):
                    curObj = collisions.Line(curObj.getTuple(), pygame.mouse.get_pos())
                elif isinstance(curObj, collisions.Line):
                    curObj = collisions.Polygon(curObj.p1, curObj.p2, pygame.mouse.get_pos())
                else:
                    curObj.points += [pygame.mouse.get_pos()]
            elif event.key == pygame.K_COMMA and typ == 8:
                combineTyp = (combineTyp + 1) % len(combineFs)
            elif event.key == pygame.K_PERIOD and typ == 8:
                combineTyp = (combineTyp - 1) % len(combineFs)
            elif event.key == pygame.K_MINUS:
                curObj.bounciness = max(0.1, round(curObj.bounciness-0.05, 3))
            elif event.key == pygame.K_EQUALS:
                curObj.bounciness = min(1.5, round(curObj.bounciness+0.05, 3))
            elif event.key == pygame.K_r:
                objs = collisions.Shapes()
            elif not playMode:
                if event.key == pygame.K_w:
                    dir[1] -= 5
                elif event.key == pygame.K_s:
                    dir[1] += 5
                elif event.key == pygame.K_a:
                    dir[0] -= 5
                elif event.key == pygame.K_d:
                    dir[0] += 5
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the header_opts that got clicked, if any
            if event.pos[1] < header_sze:
                oldtyp = typ
                typ = event.pos[0]//(win.get_width()//len(header_opts))
                if typ == 0:
                    curObj = collisions.Point(*event.pos)
                elif typ == 1:
                    curObj = collisions.Line((0, 0), (10, 10))
                    dir = [50, 100, 0]
                elif typ == 2:
                    curObj = collisions.Arc(*event.pos, 100, -135, -45)
                    dir = [-135, 100, -45]
                elif typ == 3:
                    curObj = collisions.Circle(*event.pos, 100)
                    dir = [0, 100, 0]
                elif typ == 4:
                    curObj = collisions.Rect(*event.pos, 100, 100)
                    dir = [100, 100, 0]
                elif typ == 5:
                    curObj = collisions.RotatedRect(*event.pos, 100, 100, 45)
                    dir = [100, 100, 45]
                elif typ == 6:
                    curObj = collisions.Point(*event.pos)
                elif typ == 7:
                    curObj = collisions.Rect(*event.pos, 0, 0)
                    dir = [0, 0, 0]
                elif typ == 8:
                    curObj = collisions.Rect(*event.pos, 0, 0)
                    dir = [0, 0, 0]
                else: # Last item in list - help menu
                    ratio = 5
                    pygame.draw.rect(win, (155, 155, 155), (win.get_width()//ratio, win.get_height()//ratio, win.get_width()//ratio*(ratio-2), win.get_height()//ratio*(ratio-2)), border_radius=8)
                    win.blit(FREGULAR.render("""How to use:
Click on one of the options at the top to change your tool. Pressing space adds it to the board (or applies some function to existing objects).\
The up, down, left and right arrow keys as well as comma and full stop do stuff with some of them too. When not holding alt to be in play mode, wsad does the same as the arrow keys but is more precise.
Holding '[' and ']' changes the bounciness of the object, and '-' and '=' are to fine-tune.
Holding shift in this mode shows the normals, and holding control shows the closest points to the object!
And holding alt allows you to test the movement physics. Holding shift and alt makes the movement physics have gravity, and holding ctrl reverses that gravity! Holding 'L' makes you have no friction. \
And holding '/' while holding shift will... well... I'll let you find that out for yourself.
And pressing 'r' will reset everything without warning.

Press any key/mouse to close this window""",0,allowed_width=win.get_width()//ratio*(ratio-2)-4), (win.get_width()//ratio+2, win.get_height()//ratio+2))
                    run2 = True
                    pygame.display.update()
                    while run2:
                        for ev in pygame.event.get():
                            if ev.type == pygame.QUIT or ev.type == pygame.MOUSEBUTTONDOWN or ev.type == pygame.KEYDOWN:
                                run2 = False
                        clock.tick(60)
                    typ = oldtyp
    
    btns = pygame.key.get_pressed()
    if btns[pygame.K_UP]:
        dir[1] -= 5
    if btns[pygame.K_DOWN]:
        dir[1] += 5
    if btns[pygame.K_LEFT]:
        dir[0] -= 5
    if btns[pygame.K_RIGHT]:
        dir[0] += 5
    if btns[pygame.K_COMMA]:
        dir[2] -= 5
    if btns[pygame.K_PERIOD]:
        dir[2] += 5
    
    if btns[pygame.K_w]:
        vel[1] -= 1
    if btns[pygame.K_s]:
        vel[1] += 1
    if btns[pygame.K_a]:
        vel[0] -= 1
    if btns[pygame.K_d]:
        vel[0] += 1
    
    if btns[pygame.K_LEFTBRACKET]:
        curObj.bounciness = max(0.1, round(curObj.bounciness-0.05, 3))
    if btns[pygame.K_RIGHTBRACKET]:
        curObj.bounciness = min(1.5, round(curObj.bounciness+0.05, 3))
        
    if playMode:
        win.fill(0)
    elif objs.collides(curObj):
        if curObj.isContaining(objs):
            win.fill((50, 100, 255))
        else:
            win.fill((250, 50, 50))
    else:
        win.fill(0)
    pygame.draw.rect(win, (255, 255, 255), (0, 0, win.get_width(), header_sze))
    # Split it up into equal segments and put the text header_opts[i] in the middle of each segment
    for i in range(len(header_opts)):
        pygame.draw.line(win, (0, 0, 0), (i*win.get_width()//len(header_opts), 0), (i*win.get_width()//len(header_opts), header_sze))
        text = font.render(header_opts[i], True, (0, 0, 0))
        win.blit(text, (i*win.get_width()//len(header_opts)+10, 10))
    
    if playMode:
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            if pygame.key.get_pressed()[pygame.K_SLASH]:
                cpoints = objs.closestPointTo(curObj) # [(i, i.closestPointTo(curObj)) for i in objs]
                if cpoints:
                    # Find the point on the unit circle * 0.2 that is closest to the object
                    angle = math.atan2(curObj.y-cpoints[1], curObj.x-cpoints[0])
                    gravity = [-0.2*math.cos(angle), -0.2*math.sin(angle)]
                else:
                    gravity = [0, 0]
            elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                gravity = [0, -0.2]
            else:
                gravity = [0, 0.2]
        else:
            gravity = [0, 0]
        vel = [vel[0] + gravity[0], vel[1] + gravity[1]]
        vellLimits = [10, 10]
        vel = [min(max(vel[0], -vellLimits[0]), vellLimits[0]), min(max(vel[1], -vellLimits[1]), vellLimits[1])]
        if not btns[pygame.K_l]:
            friction = [0.02, 0.02]
        else:
            friction = [0, 0]
        def fric_eff(x, fric):
            if x < -fric:
                return x + fric
            if x > fric:
                return x - fric
            return 0
        vel = [fric_eff(vel[0], friction[0]), fric_eff(vel[1], friction[1])]
        _, vel = curObj.handleCollisionsVel(vel, objs)

    else:
        pos = pygame.mouse.get_pos()
        vel = [0, 0]
        curObj = moveCurObj(curObj)
    
    for i in objs:
        drawObj(i, types.index(type(i)), offsetColour(i, (10, 255, 50)))
    drawObj(curObj, typ, offsetColour(curObj, CRAINBOWCOLOURS[typ%len(CRAINBOWCOLOURS)]))

    if not playMode:
        for i in objs.whereCollides(curObj):
            pygame.draw.circle(win, (175, 155, 155), tuple(i), 8)
        
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            mpos = pygame.mouse.get_pos()
            for o in objs:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    cs = [o.closestPointTo(curObj)]
                else:
                    cs = o.whereCollides(curObj)
                for i in cs:
                    pygame.draw.line(win, (55, 70, 100), i, collisions.rotate(i, [i[0], i[1]-50], o.tangent(i, [i[0]-mpos[0], i[1]-mpos[1]])-90), 8) # tangent -90 = normal
        if pygame.key.get_mods() & pygame.KMOD_CTRL:
            for o in objs:
                p = o.closestPointTo(curObj)
                pygame.draw.circle(win, ((230, 50, 250) if o.isCorner(p) else (230, 250, 50)), (p[0], p[1]), 8)
        sur = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        for p in curObj.toLines():
            pygame.draw.line(sur, (10, 50, 50, 100), (p[0][0], p[0][1]), (p[1][0], p[1][1]), 6)
        for p in curObj.toPoints():
            pygame.draw.circle(sur, (255, 255, 255, 100), (p[0], p[1]), 4)
        win.blit(sur, (0, 0))
        if typ < 7:
            win.blit(font.render(f'Bounciness: {curObj.bounciness}', 1, (255, 255, 255)), (0, header_sze+2))
    if typ == 8:
        win.blit(font.render(list(combineFs.keys())[combineTyp], 1, (255, 255, 255)), (0, header_sze+2))
    pygame.display.update()
    clock.tick(60)