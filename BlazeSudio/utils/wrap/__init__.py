from BlazeSudio import collisions
from BlazeSudio.utils.wrap.makeShape import MakeShape
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
    cirs = [pygame.Surface(sze, pygame.SRCALPHA) for _ in range(2 if pg2 is not False and pg2 is not True else 1)]
    pixels = pygame.surfarray.array3d(pg)
    alpha = pygame.surfarray.array_alpha(pg)
    if pg2 is True or pg2 is False:
        alpha2 = None
    else:
        alpha2 = pygame.surfarray.array_alpha(pg2)

    print(0, '%')

    height2 = height**2
    width2 = width**2
    distsSqrd = [i**2 for i in shape.jointDists]

    for y in range(sze[1]):
        closests = {}
        line = collisions.Line((0, y), (sze[0], y))
        for idx, seg in enumerate(collsegs):
            if seg.collides(line):
                closests[idx] = seg
        for x in range(sze[0]):
            collP = collisions.Point(x, y)
            closest_point = None
            min_dist = float('inf')
            
            for idx, i in closests.items():
                p = i.closestPointTo(collP)
                dist = (p[0] - x) ** 2 + (p[1] - y) ** 2
                if dist < min_dist:
                    min_dist = dist
                    closest_point = p
                    closestIdx = idx

            hei = min_dist/height2
            if hei > 1 or hei < 0:
                continue

            d = sum(distsSqrd[:closestIdx])
            d += (closest_point[0]-collsegs[closestIdx].p1[0])**2 + (closest_point[1]-collsegs[closestIdx].p1[1])**2
            if hei >= 1 or hei < 0: # Not in the shape
                continue
            d = d / width2 # Percentage of the way through the shape
            realx, realy = (int(width*d), int(height*hei)) # test
            col = pixels[realx, realy]
            a = alpha[realx, realy]
            cirs[0].set_at((int(x), int(y)), (*col, a))
            if alpha2 is not None:
                if alpha2[realx, realy] == 255:
                    ocol = (255, 255, 255)
                    oa = 255
                else:
                    ocol = (0, 0, 0)
                    oa = 0
                cirs[1].set_at((int(x), int(y)), (*ocol, oa))
        print(((y+1)*sze[0])/(sze[1]*sze[0]), '%')
    # TODO: if pg2 is True: # just mask the output
    if len(cirs) == 1:
        return cirs[0]
    return cirs

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
