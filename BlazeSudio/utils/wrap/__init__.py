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
        quality: float = 1.0, 
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
        quality (float, optional): The quality of the output, in terms of percentage of calculated total size as a decimal. Defaults to 1.0 (regular sized).
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
    """

    pg = world.get_pygame(lvl, transparent_bg=True)
    for i in world.get_level(lvl).layers:
        i.tileset = None  # So it has to render blocks instead >:)
    pg2 = world.get_pygame(lvl, transparent_bg=True)
    return wrapSurface(pg, top, bottom, quality, startRot, constraints, pg2)

def wrapSurface(pg: pygame.Surface, 
                top: int|float = 1,
                bottom: int|float = 0, 
                quality: float = 1.0, 
                startRot: int|float = 0, 
                constraints: list[Segment] = [], 
                pg2: bool|pygame.Surface=True
    ) -> tuple[pygame.Surface]|pygame.Surface:
    """
    Wrap a pygame surface and optionally it's alpha separately.

    Args:
        pg (pygame.Surface): The pygame surface to wrap.
        top (int|float, optional): The position of the top of the wrapped image. See below 'positioning'. Defaults to 1.
        bottom (int|float, optional): The position of the bottom of the wrapped image. See below 'positioning'. Defaults to 0.
        quality (float, optional): The quality of the output, in terms of percentage of calculated total size as a decimal. Defaults to 1.0 (regular sized).
        startRot (int|float, optional): The starting rotation. Defaults to 0.
        constraints (list[Segment], optional): A list of constraints to apply to the image. Defaults to [].
        pg2 (bool|pygame.Surface, optional): A pygame surface for the alpha wrapping, or a bool as to whether to return it in the first place. Defaults to True.
            - `pygame.Surface` -> use that for the alpha only wrap
            - `True` -> use `pg` for the alpha wrap
            - `False` -> don't return or calculate an alpha wrap

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
    """
    width, height = pg.get_size()
    if isinstance(pg2, pygame.Surface):
       if pg.get_size() != pg2.get_size():
           raise ValueError(
               'The 2 input surfaces are of different sizes!!!'
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
    large, main, small = shape.generateBounds(height)
    collsegs = shape.collSegments
    largePs = large.toPoints()
    sze = (math.ceil(max(i[0] for i in largePs)), math.ceil(max(i[1] for i in largePs)))
    cir = pygame.Surface(sze, pygame.SRCALPHA)

    angs = [collisions.direction(i.p1, i.p2) for i in collsegs]

    # print('initialising lines...')

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
    
    # print('finding delaunay triangles...')

    lns = collisions.Shapes(*lns)

    # edges = shapely.delaunay_triangles(shapely.MultiPoint([shapely.Point(p) for p in lns.whereCollides(lns)]), only_edges=True)

    # shapelyOuter = collisions.collToShapely(large)

    # hitsLns = [collisions.shapelyToColl(i) for i in edges.geoms if not shapelyOuter.intersects(i)]

    # hitsLns = collisions.shapelyToColl([edges])
    print('0 %')
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

    # def sort_points(points, centre = None): # *slightly* modified from https://stackoverflow.com/questions/69100978/how-to-sort-a-list-of-points-in-clockwise-anti-clockwise-in-python
    #     if centre:
    #         centre_x, centre_y = centre
    #     else:
    #         centre_x, centre_y = sum([x for x,_ in points])/len(points), sum([y for _,y in points])/len(points)
    #     angles = [(math.atan2(y - centre_y, x - centre_x)-(math.pi/4))%360 for x,y in points]
    #     idxs = sorted(range(len(points)), key=lambda i: angles[i])
    #     points = [points[i] for i in idxs]
    #     return points
    
    # if not pg.get_flags() & pygame.SRCALPHA:
    #     pg = pg.convert_alpha()

    for idx, seg in enumerate(collsegs):
        d = shape.jointDists[idx]

        # TODO: Trace the large poly along bcos it may have multiple segments
        poly = [
            closestTo(lns[idx-1].whereCollides(hitsLge), seg.p1),
            closestTo(lns[idx].whereCollides(hitsLge), seg.p2),
            closestTo(lns[idx].whereCollides(lns), seg.p2),
            closestTo(lns[idx-1].whereCollides(lns), seg.p1),
        ]

        draw_quad(cir, poly, pg.subsurface(((totd/total)*width, 0, math.ceil((d/total)*width), pg.get_height())))

        # collpoly = collisions.Polygon(*poly)

        # mins = (min(i[0] for i in poly), min(i[1] for i in poly))
        # zeroPoly = [(i[0]-mins[0], i[1]-mins[1]) for i in poly]

        # sur = pygame.Surface((max(i[0] for i in zeroPoly), max(i[1] for i in zeroPoly)), pygame.SRCALPHA)
        # pygame.gfxdraw.textured_polygon(sur, zeroPoly, pg.subsurface(((totd/total)*width, 0, math.ceil((d/total)*height), height)), 0, 0)
        # pygame.gfxdraw.textured_polygon(cir, poly, pg.subsurface(((totd/total)*width, 0, math.ceil((d/total)*height), height)), 0, 0)
        # ns = pygame.transform.scale(pg.subsurface(((totd/total)*width, 0, max((d/total)*width, 1), height)), (d/total*width, height))
        # pygame.gfxdraw.textured_polygon(cir, poly, pygame.transform.rotate(ns, math.degrees(angs[idx])), 0, 0)
        # pygame.gfxdraw.textured_polygon(cir, poly, pygame.transform.rotate(pg, math.degrees(angs[idx])), (totd/total)*width, 0)

        #poly[-1][0] -= 0.1
        #poly[-1][1] -= 0.1

        #cir.blit(*warp(pg.subsurface(((totd/total)*width, 0, max((d/total)*height, 1), height)), poly, False))

        # pygame.draw.polygon(cir, ((totd/total)*255, 125, 125, 255), poly)
        # r = collpoly.rect()
        # for y in range(math.floor(r[1]), math.ceil(r[3])):
        #     for x in range(math.floor(r[0]), math.ceil(r[2])):
        #         if collpoly.collides(collisions.Point(x, y)):
        #             cir.set_at((x, y), (c, 125, 125))
        #             alphaArray[x, y] = 255

        totd += d
        print((totd/total)*100, '%')

    # for idx, poly in enumerate(polys):
    #     d2 = shape.jointDists[idx]**2

    #     ang1 = (math.cos(angs[idx]), math.sin(angs[idx]))
    #     avgs = []
    #     for a in (angs[idx-1], angs[idx+1]):
    #         ang2 = (math.cos(a), math.sin(a))
    #         avgs.append(collisions.direction((0, 0), ((ang1[0]+ang2[0])/2, (ang1[1]+ang2[1])/2)))
        
    #     ps1 = []

    #     thisPoly = collisions.Polygon()

    #     totd2 += d2
    #     print((idx+1)/totL, '%')
    
    # TODO: if pg2 is True: # just mask the output
    return cir.copy()
    # return cirs

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
