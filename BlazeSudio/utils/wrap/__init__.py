from BlazeSudio import collisions
from BlazeSudio.utils.wrap.makeShape import MakeShape
from BlazeSudio.utils.wrap.warp import draw_quad
import os
import pygame
import math

__all__ = [
    'wrapLevel',
    'wrapSurface',
    'Segment'
]

class Segment:
    def __init__(self, startx, endx, angle=None):
        """
        A segment of an image with optional angle constraints!

        Args:
            startx (int): The starting x position of the segment
            endx (int): The ending x position of the segment
            angle (int, optional): The angle to constrain this segment to, or None for nothing. Defaults to None.
        """
        self.pos = [startx, endx]
        self.angle = angle
    
    def __str__(self):
        if self.angle is None:
            return f'<Segment {self.pos[0]}-{self.pos[1]}>'
        return f'<Segment {self.pos[0]}-{self.pos[1]} @{self.angle}°>'
    def __repr__(self): return str(self)

def wrapLevel(
        world, 
        lvl: int, 
        top: int|float = 1,
        bottom: int|float = 0, 
        limit: bool = True, 
        startRot: int|float = 0, 
        constraints: list[Segment] = [],
    ) -> tuple[pygame.Surface]:
    """
    Wrap a level and get it's wrapped surface and also it's collision surface.

    Args:
        world (_type_): The world to get the level from.
        lvl (int): The level number.
        top (int|float, optional): The position of the top of the wrapped image. See below 'positioning'. Defaults to 1.
        bottom (int|float, optional): The position of the bottom of the wrapped image. See below 'positioning'. Defaults to 0.
        limit (bool, optional): Whether to limit the warp so it MUST be a height of `pg.get_height()`. Making this False may give some very warped results. Constrains the bottom of the image. Defaults to True.
        startRot (int|float, optional): The starting rotation. Defaults to 0.
        constraints (list[Segment], optional): A list of constraints to apply to the image. Defaults to [].

    Returns:
        tuple[pygame.Surface, pygame.Surface]: The output surface or surfaces which are the wrapped image(s)

    Positioning:
        - When the image is being wrapped, it wraps the width of the image.
        - The top and bottom parameters are the positions of the top and bottom of the image respectively.
        ```
        1 = the width (wrapped) plus a buffer of the image height
        0 = the image width (wrapped)
        -1 = the centroid (or centroid line(s)) of the polygon made by the wrapped image width
        ```
        - Top **must** be >= 0 and bottom **must** be <= 0 and >= -1.
    """

    pg = world.get_pygame(lvl, transparent_bg=True)
    for i in world.get_level(lvl).layers:
        i.tileset = None  # So it has to render blocks instead >:)
    pg2 = world.get_pygame(lvl, transparent_bg=True)
    return wrapSurface(pg, top, bottom, limit, startRot, constraints, pg2)

def wrapSurface(pg: pygame.Surface, 
                top: int|float = 1,
                bottom: int|float = 0, 
                limit: bool = True,
                startRot: int|float = 0, 
                constraints: list[Segment] = [], 
                pg2: bool|pygame.Surface = True,
                isIter: bool = False
    ) -> tuple[pygame.Surface]|pygame.Surface:
    """
    Wrap a pygame surface and optionally it's alpha separately.

    Args:
        pg (pygame.Surface): The pygame surface to wrap.
        top (int|float, optional): The position of the top of the wrapped image. See below 'positioning'. Defaults to 1.
        bottom (int|float, optional): The position of the bottom of the wrapped image. See below 'positioning'. Defaults to 0.
        limit (bool, optional): Whether to limit the warp so it MUST be a height of `pg.get_height()`. Making this False may give some very warped results. Constrains the bottom of the image. Defaults to True.
        startRot (int|float, optional): The starting rotation. Defaults to 0.
        constraints (list[Segment], optional): A list of constraints to apply to the image. Defaults to [].
        pg2 (bool|pygame.Surface, optional): A pygame surface for the alpha wrapping, or a bool as to whether to return it in the first place. Defaults to True.
            - `pygame.Surface` -> use that for the alpha only wrap
            - `True` -> use `pg` for the alpha wrap
            - `False` -> don't return or calculate an alpha wrap
        isIter (bool, optional): Whether to return a generator or just run the func itself. Defaults to False (just run the func). The generator is in a format aplicable to `graphics.loading.Progress`.

    Returns:
        tuple[pygame.Surface, pygame.Surface]: The output surface or surfaces which are the wrapped image(s)
    
    Positioning:
        - When the image is being wrapped, it wraps the width of the image.
        - The top and bottom parameters are the positions of the top and bottom of the image respectively.
        ```
        1 = the width (wrapped) plus a buffer of the image height
        0 = the image width (wrapped)
        -1 = the centroid (or centroid line(s)) of the polygon made by the wrapped image width
        ```
        - Top **must** be >= 0 and bottom **must** be <= 0 and >= -1.
    """
    def wrap():
        yield 'Initialising wrap', {'amount': 3}
        width, height = pg.get_size()
        if isinstance(pg2, pygame.Surface):
            if pg.get_size() != pg2.get_size():
                raise ValueError(
                    'The 2 input surfaces are of different sizes!!!'
                )
        if top < 0 or bottom > 0 or bottom < -1:
            raise ValueError(
                'Top must be >= 0 and bottom must be <= 0 and >= -1'
            )
        shape = MakeShape(width)
        def checkX1(x):
            for con in constraints:
                if x > con.pos[0] and x < con.pos[1]:
                    return False
            return True
        segs = [x for x in range(width) if checkX1(x)]
        def checkX2(x):
            for con in constraints:
                if x == con.pos[0]:
                    return con.angle
            return None
        segrots = [checkX2(x) for x in segs]
        shape.joints = [(i, 0) for i in segs]
        shape.setAngs = segrots
        # shape.joints = [(0, 100), (100, 200), (200, 200), (300, 100), (200, 0), (100, 0), (0, 100)]
        shape.recalculate_dists()
        large, main, small = shape.generateBounds(height, True, False, False) # main and small set to None
        largePs = large.toPoints()
        mins = (min(i[0] for i in largePs), min(i[1] for i in largePs))
        for i in range(len(shape.joints)):
            shape.joints[i] = (shape.joints[i][0]-mins[0], shape.joints[i][1]-mins[1])
        large, main, small = shape.generateBounds(height, True, False, True)
        collsegs = shape.collSegments
        largePs = large.toPoints()
        sze = (math.ceil(max(i[0] for i in largePs)), math.ceil(max(i[1] for i in largePs)))
        cir = pygame.Surface(sze, pygame.SRCALPHA)

        angs = [collisions.direction(i.p1, i.p2) for i in collsegs]

        yield 'Initialising lines'

        lns = []
        angs2 = []

        r = (shape.lastRadius + height)*2

        for idx, seg in enumerate(collsegs):
            #d2 = shape.jointDists[idx]**2

            sin_sum = math.sin(angs[idx]) + math.sin(angs[idx-1])
            cos_sum = math.cos(angs[idx]) + math.cos(angs[idx-1])

            # Calculate the circular mean using arctan2
            mean_rad = math.atan2(sin_sum, cos_sum)
            avg = math.degrees(mean_rad)
            angs2.append(avg)
        
            lns.append(collisions.Line(collisions.rotate(seg.p1, (seg.p1[0], seg.p1[1]-r), avg), 
                                        collisions.rotate(seg.p1, (seg.p1[0], seg.p1[1]+r), avg)))
            
            # pygame.draw.line(cirs[0], (255, 50, 255), seg[0], seg[1], 2)

        lns = collisions.Shapes(*lns)

        hitsLge = collisions.Shapes(*large.toLines())

        def closestTo(li, p):
            d = None
            clo = None
            for p2 in li:
                d2 = (p2[0]-p[0])**2+(p2[1]-p[1])**2
                if d is None or d2 < d:
                    d = d2
                    clo = p2
            return clo
        
        # for ln in lns:
        #     pygame.draw.line(cir, (125, 125, 125), ln[0], ln[1])
        
        # for p in lns.whereCollides(lns):
        #     pygame.draw.circle(cir, (0, 0, 0), p, 2)

        totd = 0
        total = sum(shape.jointDists)

        lastP1 = None
        lnsLen = len(lns.shapes)

        yield 'Calculating segments', {'amount': len(collsegs), 'done': 0}

        for idx, seg in enumerate(collsegs):
            d = shape.jointDists[idx]

            # TODO: Trace the large poly along bcos it may have multiple segments
            
            if top != 0:
                out1 = closestTo(lns[idx].whereCollides(hitsLge), seg.p1)
                out2 = closestTo(lns[(idx+1)%lnsLen].whereCollides(hitsLge), seg.p2)
                if top == 1:
                    outerp1 = out1
                    outerp2 = out2
                else:
                    inner1 = seg.p1
                    outerp1 = (
                        (inner1[0]-out1[0])*top+out1[0],
                        (inner1[1]-out1[1])*top+out1[1]
                    )
                    inner2 = seg.p2
                    outerp2 = (
                        (inner2[0]-out2[0])*top+out2[0],
                        (inner2[1]-out2[1])*top+out2[1]
                    )
            else:
                outerp1 = seg.p1
                outerp2 = seg.p2
            
            if bottom != 0:
                if lastP1 is None:
                    p1Closests = small.closestPointTo(collisions.Point(*seg.p1))
                    p1Closest = closestTo(p1Closests, seg.p1)
                else:
                    p1Closest = lastP1
                p2Closests = small.closestPointTo(collisions.Point(*seg.p2))
                p2Closest = closestTo(p2Closests, seg.p2)
                lastP1 = p2Closest

                if bottom == -1:
                    innerP1 = p1Closest
                    innerP2 = p2Closest
                else:
                    innerP1 = (
                        (p1Closest[0]-seg.p1[0])*abs(bottom)+seg.p1[0],
                        (p1Closest[1]-seg.p1[1])*abs(bottom)+seg.p1[1]
                    )
                    innerP2 = (
                        (p2Closest[0]-seg.p2[0])*abs(bottom)+seg.p2[0],
                        (p2Closest[1]-seg.p2[1])*abs(bottom)+seg.p2[1]
                    )
            else:
                innerP1 = seg.p1
                innerP2 = seg.p2
            
            if limit:
                phi1 = collisions.direction(outerp1, innerP1)
                innerP1 = collisions.rotate(outerp1, (outerp1[0], outerp1[1]-height), math.degrees(phi1)+90)
                phi2 = collisions.direction(outerp2, innerP2)
                innerP2 = collisions.rotate(outerp2, (outerp2[0], outerp2[1]-height), math.degrees(phi2)+90)

            poly = [
                outerp1,
                outerp2,
                innerP2,
                innerP1,
            ]

            draw_quad(cir, poly, pg.subsurface(((totd/total)*width, 0, math.ceil((d/total)*width), pg.get_height())))

            totd += d
            yield 'Calculating segments'
        
        # TODO: if pg2 is True: # just mask the output
        return cir.copy()
        # return cirs
    if isIter:
        return wrap()
    else:
        w = wrap()
        for msg in w:
            pass
        try:
            next(w)
        except StopIteration as e:
            return e.value

def save(imgs, fname, szes, spacing=None): # TODO: Think about removing
    ms = max(szes)
    ss = sum(szes)
    sp = (spacing or ms)
    out = pygame.Surface((ms, ss+sp-ss%sp), pygame.SRCALPHA)
    prevh = 0
    for img, sze in zip(imgs, szes):
        if isinstance(img, pygame.Surface):
            newImg = pygame.transform.scale(img, (sze, sze)).convert_alpha()
            out.blit(newImg, (0, prevh))
            if spacing is None:
                prevh += newImg.get_height()
            else:
                prevh += spacing
            continue
        new_image = pygame.Surface((len(img[0]), len(img)), pygame.SRCALPHA)
        for y, row in enumerate(img):
            for x, pixel in enumerate(row):
                new_image.set_at((x, y), pixel)
        newImg = pygame.transform.scale(new_image, (sze, sze))
        out.blit(newImg, (0, prevh))
        if spacing is None:
            prevh += newImg.get_height()
        else:
            prevh += spacing

    if not os.path.exists(os.path.dirname(fname)):
        os.makedirs(os.path.dirname(fname))
    pygame.image.save(out, fname)
