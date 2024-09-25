import os
import pygame
import math

# Thanks to https://stackoverflow.com/questions/38745020/wrap-image-around-a-circle !!

def wrapWorld(world):
    imgs = [[], []]
    szes = []
    for outlining in (False, True):
        for lvl in range(len(world.ldtk.levels)):
            Ro = 50.0
            Ri = 1.0
            size = 128
            settingsExists = False
            for e in world.ldtk.levels[lvl].entities:
                if e.identifier == 'Settings':
                    settingsExists = True
                    for i in e.fieldInstances:
                        if i['__identifier'] == 'Ro':
                            Ro = i['__value'] or Ro
                        if i['__identifier'] == 'Ri':
                            Ri = i['__value'] or Ri
                        if i['__identifier'] == 'size':
                            size = i['__value'] or size
            if not settingsExists:
                continue
            szes.append(size)

            cir = [[(0, 0, 0, 0) for x in range(int(Ro * 2))] for y in range(int(Ro * 2))]

            if outlining:
                for i in world.get_level(lvl).layers:
                    i.tileset = None  # So it has to render blocks instead >:)
            pg = world.get_pygame(lvl, transparent_bg=True)
            width, height = pg.get_size()
            pixels = pygame.surfarray.pixels3d(pg)
            alpha = pygame.surfarray.pixels_alpha(pg)

            for i in range(int(Ro)):
                outer_radius = math.sqrt(Ro * Ro - i * i)
                for j in range(-int(outer_radius), int(outer_radius)):
                    if i < Ri:
                        inner_radius = math.sqrt(Ri * Ri - i * i)
                    else:
                        inner_radius = -1
                    if j < -inner_radius or j > inner_radius:
                        x = Ro + j
                        y = Ro - i
                        angle = math.atan2(y - Ro, x - Ro) / 2
                        distance = math.sqrt((y - Ro) * (y - Ro) + (x - Ro) * (x - Ro))
                        distance = math.floor((distance - Ri + 1) * (height - 1) / (Ro - Ri))
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
                        y = Ro + i
                        angle = math.atan2(y - Ro, x - Ro) / 2
                        distance = math.sqrt((y - Ro) * (y - Ro) + (x - Ro) * (x - Ro))
                        distance = math.floor((distance - Ri + 1) * (height - 1) / (Ro - Ri))
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
            imgs[outlining].append(cir)
    return imgs, szes

def save(imgs, fname, szes):
    out = pygame.Surface((max(szes), sum(szes)/2), pygame.SRCALPHA)
    prevh = 0
    for img, sze in zip(imgs, szes):
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
