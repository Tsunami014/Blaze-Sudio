# Thanks to https://www.reddit.com/r/pygame/comments/z571pa/this_is_how_you_can_texture_a_polygon/ !!!!
import pygame


def lerp( p1, p2, f ):
    return p1 + f * (p2 - p1)

def lerp2d( p1, p2, f ):
    return tuple( lerp( p1[i], p2[i], f ) for i in range(2) )

def draw_quad( surface, quad, img ):

    points = dict()

    for i in range( img.get_size()[1]+1 ):
        b = lerp2d( quad[1], quad[2], i/img.get_size()[1] )
        c = lerp2d( quad[0], quad[3], i/img.get_size()[1] )
        for u in range( img.get_size()[0]+1 ):
            a = lerp2d( c, b, u/img.get_size()[0] )
            points[ (u,i) ] = a

    for x in range( img.get_size()[0] ):
        for y in range( img.get_size()[1] ):
            pygame.draw.polygon(
                surface,
                img.get_at((x,y)),
                [ points[ (a,b) ] for a, b in [ (x,y), (x,y+1), (x+1,y+1), (x+1,y) ] ] 
            )
