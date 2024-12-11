# Thanks to https://www.reddit.com/r/pygame/comments/z571pa/this_is_how_you_can_texture_a_polygon/ !!!!
import pygame

def lerp(p1, p2, f):
    return p1 + f * (p2 - p1)

def lerp2d(p1, p2, f):
    return tuple(lerp(p1[i], p2[i], f) for i in range(2))

def draw_quad(surface, quad, img):
    points = []

    wid, hei = img.get_size()

    for i in range(hei+1):
        b = lerp2d(quad[1], quad[2], i/hei)
        c = lerp2d(quad[0], quad[3], i/hei)
        row = []
        for u in range(wid+1):
            a = lerp2d(c, b, u/wid)
            row.append(a)
        points.append(row)

    for x in range(wid):
        for y in range(hei):
            pygame.draw.polygon(
                surface,
                img.get_at((x,y)),
                [points[b][a] for a, b in [(x,y), (x,y+1), (x+1,y+1), (x+1,y)]] 
            )
