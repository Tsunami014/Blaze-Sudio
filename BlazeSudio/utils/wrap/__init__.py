from BlazeSudio.utils.wrap import constraints, makeShape
import os
import pygame
import math

__all__ = [
    'wrapLevel',
    'constraints'
]

def wrapLevel(
        world, 
        lvl: int, 
        Ri: int|float = 0, 
        quality: float = 1.0, 
        startRot: int|float = 0, 
        constraints: list[constraints.BaseConstraint] = [],
    ) -> tuple[pygame.Surface]:
    """
    Wrap a level and get it's wrapped surface and also it's collision surface.

    Args:
        world (_type_): The world to get the level from.
        lvl (int): The level number.
        Ri (float, optional): The amount or gap in the centre of the circle. Defaults to 0.
        quality (float, optional): The quality of the output, in terms of percentage of calculated total size as a decimal. Defaults to 1.0 (regular sized).
        startRot (int|float, optional): The starting rotation. Defaults to 0.
        constraints (list[constraints.BaseConstraint], optional): A list of constraints to apply to the image. Defaults to [].

    Returns:
        tuple[pygame.Surface, pygame.Surface]: The output surface or surfaces which are the wrapped image(s)
    """

    pg = world.get_pygame(lvl, transparent_bg=True)
    for i in world.get_level(lvl).layers:
        i.tileset = None  # So it has to render blocks instead >:)
    pg2 = world.get_pygame(lvl, transparent_bg=True)
    return wrapSurface(pg, Ri, quality, startRot, constraints, pg2)

def wrapSurface(pg: pygame.Surface, 
               Ri: int|float = 0, 
               quality: float = 1.0, 
               startRot: int|float = 0, 
               constraints: list[constraints.BaseConstraint] = [], 
               pg2: bool|pygame.Surface=True
    ) -> tuple[pygame.Surface]|pygame.Surface:
    """
    Wrap a pygame surface and optionally it's alpha separately.

    Args:
        pg (pygame.Surface): The pygame surface to wrap.
        Ri (float, optional): The amount or gap in the centre of the circle. Defaults to 0.
        quality (float, optional): The quality of the output, in terms of percentage of calculated total size as a decimal. Defaults to 1.0 (regular sized).
        startRot (int|float, optional): The starting rotation. Defaults to 0.
        constraints (list[constraints.BaseConstraint], optional): A list of constraints to apply to the image. Defaults to [].
        pg2 (bool|pygame.Surface, optional): A pygame surface for the alpha wrapping, or a bool as to whether to return it in the first place. Defaults to True.
            - `pygame.Surface` -> use that for the alpha only wrap
            - `True` -> use `pg` for the alpha wrap
            - `False` -> don't return or calculate an alpha wrap

    Returns:
        tuple[pygame.Surface, pygame.Surface]: The output surface or surfaces which are the wrapped image(s)
    """
    circrad = 250
    imgw, imgh = circrad*2, circrad*2
    cirs = [pygame.Surface((imgw, imgh), pygame.SRCALPHA) for _ in range(2 if pg2 is not False and pg2 is not True else 1)]
    width, height = pg.get_size()
    if isinstance(pg2, pygame.Surface):
        if pg.get_size() != pg2.get_size():
            raise ValueError(
                'The 2 input surfaces are of different sizes!!!'
            )
    pixels = pygame.surfarray.array3d(pg)
    alpha = pygame.surfarray.array_alpha(pg)
    if pg2 is True or pg2 is False:
        alpha2 = None
    else:
        alpha2 = pygame.surfarray.array_alpha(pg2)
    
    centre = (int(imgw/2), int(imgh/2))

    for y in range(imgh):
        for x in range(imgw):
            d = (x-centre[0])**2+(y-centre[1])**2
            if d < Ri**2 or d > circrad**2:
                continue
            ang = math.atan2(y-centre[1],x-centre[0])/2
            realx, realy = int(width*(ang/math.pi)) % width, int(height*(1-(math.sqrt(d)/circrad))-1)
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
