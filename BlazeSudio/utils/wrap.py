import os
import pygame
import math

# Thanks to https://stackoverflow.com/questions/38745020/wrap-image-around-a-circle !!

def wrapLevel(world, lvl, Ro=50.0, Ri=1.0, quality=1.0):
    imgs = []
    for outlining in (False, True):
        cir = [[(0, 0, 0, 0) for x in range(int(Ro * 2 * quality))] for y in range(int(Ro * 2 * quality))]

        if outlining:
            for i in world.get_level(lvl).layers:
                i.tileset = None  # So it has to render blocks instead >:)
        pg = world.get_pygame(lvl, transparent_bg=True)
        width, height = pg.get_size()
        pixels = pygame.surfarray.pixels3d(pg)
        alpha = pygame.surfarray.pixels_alpha(pg)

        for i in range(int(Ro * quality)):
            outer_radius = math.sqrt(Ro * Ro - (i / quality) * (i / quality))
            for j in range(-int(outer_radius * quality), int(outer_radius * quality)):
                if i < Ri * quality:
                    inner_radius = math.sqrt(Ri * Ri - (i / quality) * (i / quality))
                else:
                    inner_radius = -1
                if j < -inner_radius * quality or j > inner_radius * quality:
                    x = Ro * quality + j
                    y = Ro * quality - i
                    angle = math.atan2(y - Ro * quality, x - Ro * quality) / 2
                    distance = math.sqrt((y - Ro * quality) * (y - Ro * quality) + (x - Ro * quality) * (x - Ro * quality))
                    distance = math.floor((distance / quality - Ri + 1) * (height - 1) / (Ro - Ri))
                    if distance >= height:
                        distance = height - 1
                    col = pixels[int(width * angle / math.pi) % width, height - distance - 1]
                    a = alpha[int(width * angle / math.pi) % width, height - distance - 1]
                    if outlining:
                        if a == 255:
                            col = (255, 255, 255)
                            a = 255
                        else:
                            col = (0, 0, 0)
                            a = 0
                    cir[int(y)][int(x)] = (*col, a)
                    y = Ro * quality + i
                    angle = math.atan2(y - Ro * quality, x - Ro * quality) / 2
                    distance = math.sqrt((y - Ro * quality) * (y - Ro * quality) + (x - Ro * quality) * (x - Ro * quality))
                    distance = math.floor((distance / quality - Ri + 1) * (height - 1) / (Ro - Ri))
                    if distance >= height:
                        distance = height - 1
                    col = pixels[int(width * angle / math.pi) % width, height - distance - 1]
                    a = alpha[int(width * angle / math.pi) % width, height - distance - 1]
                    if outlining:
                        if a == 255:
                            col = (255, 255, 255)
                            a = 255
                        else:
                            col = (0, 0, 0)
                            a = 0
                    cir[int(y)][int(x)] = (*col, a)
        imgs.append(cir)
    return imgs

def save(imgs, fname, szes):
    ms = max(szes)
    ss = sum(szes)
    out = pygame.Surface((ms, ss+ss%ms), pygame.SRCALPHA)
    prevh = 0
    for img, sze in zip(imgs, szes):
        if isinstance(img, pygame.Surface):
            newImg = pygame.transform.scale(img, (sze, sze)).convert_alpha()
            out.blit(newImg, (0, prevh))
            prevh += newImg.get_height()
            continue
        new_image = pygame.Surface((len(img[0]), len(img)), pygame.SRCALPHA)
        for y, row in enumerate(img):
            for x, pixel in enumerate(row):
                new_image.set_at((x, y), pixel)
        newImg = pygame.transform.scale(new_image, (sze, sze))
        out.blit(newImg, (0, prevh))
        prevh += newImg.get_height()

    if not os.path.exists(os.path.dirname(fname)):
        os.makedirs(os.path.dirname(fname))
    pygame.image.save(out, fname)
