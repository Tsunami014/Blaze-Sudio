import os
if 'debug' in os.environ:
    from BlazeSudio.collisions.lib import collisions
else:
    from BlazeSudio import collisions
from BlazeSudio.graphics.options import CRAINBOWCOLOURS, FFONT
import pygame
import math
pygame.init()
win = pygame.display.set_mode()
run = True
header_opts = ['point', 'line', 'circle', 'rect', 'rotated rect', 'polygon', 'eraser', 'combiner', 'help']
types = [collisions.Point, collisions.Line, collisions.Circle, collisions.Rect, collisions.RotatedRect, collisions.Polygon]
highlightTyps = {
            0: (collisions.Point, collisions.Line, collisions.ClosedShape),
            1: (collisions.Rect),
            2: (collisions.Shape)
        }
typ = 0
curObj = collisions.Point(0, 0)
objs = collisions.Shapes()
dir = [0, 0, 0]
combineTyp = 0
pos = [0, 0]
accel = [0, 0]
maxcombinetyps = 3
combineCache = [None, None]

def findCombinedOutput():
    global combineCache
    toCombineObjs = [o for o in objs if isinstance(o, highlightTyps[combineTyp]) and o.collides(curObj)]
    cacheCheck = (toCombineObjs, combineTyp)
    if combineCache[0] == cacheCheck:
        return combineCache[1]
    else:
        if combineTyp == 1:
            combined = collisions.ShapeCombiner.to_rects(*toCombineObjs)
        elif combineTyp == 2:
            combined = collisions.ShapeCombiner.bounding_box(*toCombineObjs)
        else:
            combined = collisions.ShapeCombiner.to_polygons(*toCombineObjs)
        ret = (combined, toCombineObjs)
        combineCache = [cacheCheck, ret]
        return ret

def drawRect(obj, col):
    if obj.w == 0 and obj.h == 0:
        pygame.draw.circle(win, col, (obj.x, obj.y), 4)
    elif obj.w == 0:
        pygame.draw.line(win, col, (obj.x, obj.y), (obj.x, obj.y+obj.h), 3)
    elif obj.h == 0:
        pygame.draw.line(win, col, (obj.x, obj.y), (obj.x+obj.w, obj.y), 3)
    minx = min(obj.x, obj.x+obj.w)
    miny = min(obj.y, obj.y+obj.h)
    pygame.draw.rect(win, col, (minx, miny, abs(obj.w), abs(obj.h)), 8)

def drawLine(obj, col):
    if obj.p1 == obj.p2:
        pygame.draw.circle(win, col, obj.p1, 8)
    pygame.draw.line(win, col, obj.p1, obj.p2, 8)

def drawObj(obj, t, col): # TODO: Work off of type(obj), not t.
    if t == 7: # As well as drawing the point, outline the shapes to be combined
        combined, objsToCombine = findCombinedOutput()
        for o in objsToCombine:
            drawObj(o, types.index(type(o)), (255, 110, 60))
        for o in combined:
            drawObj(o, types.index(type(o)), (244, 194, 194, 0.8))
    
    if t in (0, 6):
        pygame.draw.circle(win, ((255, 255, 255) if t == 6 else col), (obj.x, obj.y), 8)
    elif t == 1:
        drawLine(obj, col)
    elif t == 2:
        pygame.draw.circle(win, col, (obj.x, obj.y), obj.r, 8)
    elif t in (3, 7):
        drawRect(obj, col)
    elif t == 4:
        for line in obj.toLines():
            pygame.draw.line(win, col, line.p1, line.p2, 8)
    elif t == 5:
        if isinstance(obj, collisions.Point):
            pygame.draw.circle(win, col, (obj.x, obj.y), 8)
        elif isinstance(obj, collisions.Line):
            pygame.draw.line(win, col, obj.p1, obj.p2, 8)
        else:
            for line in obj.toLines():
                pygame.draw.line(win, col, line.p1, line.p2, 8)

def moveCurObj(curObj):
    if typ == 1:
        curObj.p1 = pos
        curObj.p2 = (curObj.p1[0]+dir[0], curObj.p1[1]+dir[1])
    elif typ == 5:
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
        if typ == 2:
            curObj.r = dir[1]
        elif typ in (4, 3, 7):
            curObj.w, curObj.h = dir[0], dir[1]
            if typ == 4:
                curObj.rot = dir[2]
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
                if typ == 6:
                    for i in objs.copy_leave_shapes():
                        if i.collides(curObj):
                            objs.remove_shape(i)
                elif typ == 7:
                    new, toRemove = findCombinedOutput()
                    objs.remove_shapes(*toRemove)
                    objs.add_shapes(*new)
                else:
                    objs.add_shape(curObj)
                    if typ == 5:
                        curObj = curObj = collisions.Point(*pygame.mouse.get_pos())
                    else:
                        curObj = curObj.copy()
            elif event.key == pygame.K_COMMA and typ == 5:
                if isinstance(curObj, collisions.Point):
                    curObj = collisions.Line(curObj.getTuple(), pygame.mouse.get_pos())
                elif isinstance(curObj, collisions.Line):
                    curObj = collisions.Polygon(curObj.p1, curObj.p2, pygame.mouse.get_pos())
                else:
                    curObj.points += [pygame.mouse.get_pos()]
            elif event.key == pygame.K_COMMA and typ == 7:
                combineTyp = (combineTyp + 1) % maxcombinetyps
            elif event.key == pygame.K_PERIOD and typ == 7:
                combineTyp = (combineTyp - 1) % maxcombinetyps
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
            if event.pos[1] < 50:
                oldtyp = typ
                typ = event.pos[0]//(win.get_width()//len(header_opts))
                if typ == 0:
                    curObj = collisions.Point(*event.pos)
                elif typ == 1:
                    curObj = collisions.Line((0, 0), (10, 10))
                    dir = [50, 100, 0]
                elif typ == 2:
                    curObj = collisions.Circle(*event.pos, 100)
                    dir = [0, 100, 0]
                elif typ == 3:
                    curObj = collisions.Rect(*event.pos, 100, 100)
                    dir = [100, 100, 0]
                elif typ == 4:
                    curObj = collisions.RotatedRect(*event.pos, 100, 100, 45)
                    dir = [100, 100, 45]
                elif typ == 5:
                    curObj = collisions.Point(*event.pos)
                elif typ == 6:
                    curObj = collisions.Point(*event.pos)
                elif typ == 7:
                    curObj = collisions.Rect(*event.pos, 0, 0)
                    dir = [0, 0, 0]
                else: # Last item in list - help menu
                    ratio = 5
                    pygame.draw.rect(win, (155, 155, 155), (win.get_width()//ratio, win.get_height()//ratio, win.get_width()//ratio*(ratio-2), win.get_height()//ratio*(ratio-2)), border_radius=8)
                    win.blit(FFONT.render("""How to use:
Click on one of the options at the top to change your tool. Pressing space adds it to the board (or applies some function to existing objects). The up, down, left and right arrow keys as well as comma and full stop do stuff with some of them too. When not holding alt to be in play mode, wsad does the same as the arrow keys but is more precise.
Holding '[' and ']' changes the bounciness of the object.
Holding shift in this mode shows the normals, and holding control shows the closest points to the object!
And holding alt allows you to test the movement physics. Holding shift and alt makes the movement physics have gravity, and holding ctrl reverses that gravity! And holding '/' while holding shift will... well... I'll let you find that out for yourself.
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
        accel[1] -= 1
    if btns[pygame.K_s]:
        accel[1] += 1
    if btns[pygame.K_a]:
        accel[0] -= 1
    if btns[pygame.K_d]:
        accel[0] += 1
    
    if btns[pygame.K_LEFTBRACKET]:
        curObj.bounciness = max(0.1, curObj.bounciness-0.05)
    if btns[pygame.K_RIGHTBRACKET]:
        curObj.bounciness = min(1.5, curObj.bounciness+0.05)
        
    win.fill((0, 0, 0) if (not objs.collides(curObj)) or playMode else (250, 50, 50))
    pygame.draw.rect(win, (255, 255, 255), (0, 0, win.get_width(), 50))
    # Split it up into equal segments and put the text header_opts[i] in the middle of each segment
    for i in range(len(header_opts)):
        pygame.draw.line(win, (0, 0, 0), (i*win.get_width()//len(header_opts), 0), (i*win.get_width()//len(header_opts), 50))
        font = pygame.font.Font(None, 36)
        text = font.render(header_opts[i], True, (0, 0, 0))
        win.blit(text, (i*win.get_width()//len(header_opts)+10, 10))
    
    if playMode:
        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
            if pygame.key.get_pressed()[pygame.K_SLASH]:
                cpoints = objs.closestPointTo(curObj) # [(i, i.closestPointTo(curObj)) for i in objs]
                if cpoints:
                    cpoints.sort(key=lambda x: (curObj.x-x[0])**2+(curObj.y-x[1])**2)
                    # Find the point on the unit circle * 0.2 that is closest to the object
                    closest = cpoints[0]
                    angle = math.atan2(curObj.y-closest[1], curObj.x-closest[0])
                    gravity = [-0.2*math.cos(angle), -0.2*math.sin(angle)]
                else:
                    gravity = [0, 0]
            elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                gravity = [0, -0.2]
            else:
                gravity = [0, 0.2]
        else:
            gravity = [0, 0]
        accel = [accel[0] + gravity[0], accel[1] + gravity[1]]
        accellLimits = [10, 10]
        accel = [min(max(accel[0], -accellLimits[0]), accellLimits[0]), min(max(accel[1], -accellLimits[1]), accellLimits[1])]
        friction = [0.02, 0.02]
        def fric_eff(x, fric):
            if x < -fric:
                return x + fric
            if x > fric:
                return x - fric
            return 0
        accel = [fric_eff(accel[0], friction[0]), fric_eff(accel[1], friction[1])]
        _, accel = curObj.handleCollisionsVel(accel, objs)

    else:
        pos = pygame.mouse.get_pos()
        accel = [0, 0]
        curObj = moveCurObj(curObj)
    
    for i in objs:
        drawObj(i, types.index(type(i)), offsetColour(i, (10, 255, 50)))
    drawObj(curObj, typ, offsetColour(curObj, CRAINBOWCOLOURS[typ]))

    if not playMode:
        for i in objs.whereCollides(curObj):
            pygame.draw.circle(win, (175, 155, 155), i, 8)
        
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
    pygame.display.update()
    clock.tick(60)