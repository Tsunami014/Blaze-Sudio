# Improved from https://www.reddit.com/r/pygame/comments/z571pa/this_is_how_you_can_texture_a_polygon/
import pygame

def lerp2d(p1, p2, f):
    return (
        p1[0] + (p2[0] - p1[0]) * f,
        p1[1] + (p2[1] - p1[1]) * f
    )

def draw_quad(surface, quad, img):
    pixel_array = pygame.surfarray.pixels3d(img)
    alpha_array = pygame.surfarray.pixels_alpha(img)
    wid, hei = img.get_size()
    inv_wid = 1 / wid
    inv_hei = 1 / hei
    for y in range(hei):
        fy = y * inv_hei
        fy1 = (y + 1) * inv_hei
        b1 = lerp2d(quad[1], quad[2], fy)
        b2 = lerp2d(quad[1], quad[2], fy1)
        c1 = lerp2d(quad[0], quad[3], fy)
        c2 = lerp2d(quad[0], quad[3], fy1)
        for x in range(wid):
            fx = x * inv_wid
            fx1 = (x + 1) * inv_wid
            color = (*pixel_array[x, y], alpha_array[x, y])
            poly = [
                lerp2d(c1, b1, fx),
                lerp2d(c1, b1, fx1),
                lerp2d(c2, b2, fx1),
                lerp2d(c2, b2, fx),
            ]
            pygame.draw.polygon(surface, color, poly)
