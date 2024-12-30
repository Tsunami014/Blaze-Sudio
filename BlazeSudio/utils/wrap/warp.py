# Improved from https://www.reddit.com/r/pygame/comments/z571pa/this_is_how_you_can_texture_a_polygon/
import pygame

def lerp2d(p1, p2, f):
    return (
        p1[0] + (p2[0] - p1[0]) * f,
        p1[1] + (p2[1] - p1[1]) * f
    )

def draw_quad(surface, quad, img):
    pixel_array = pygame.surfarray.pixels3d(img)
    wid, hei = img.get_size()
    for y in range(hei):
        b1 = lerp2d(quad[1], quad[2], y/hei)
        b2 = lerp2d(quad[1], quad[2], (y+1)/hei)
        c1 = lerp2d(quad[0], quad[3], y/hei)
        c2 = lerp2d(quad[0], quad[3], (y+1)/hei)
        for x in range(wid):
            color = pixel_array[x, y]
            poly = [
                lerp2d(c1, b1, x/wid),
                lerp2d(c1, b1, (x+1)/wid),
                lerp2d(c2, b2, (x+1)/wid),
                lerp2d(c2, b2, x/wid),
            ]
            pygame.draw.polygon(surface, color, poly)
