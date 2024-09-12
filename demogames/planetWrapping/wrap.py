import os, sys
if 'demogames/planetWrapping' in sys.path[0]:
    sys.path.append(os.path.abspath(os.path.join(__file__, '../../../'))) # Make sure you can still access BS
from BlazeSudio.ldtk import sync
# if not sync.is_synced():
#     print(sync.explanation())
#     print("For this file, it's best to use it with the 'after save', so it will automatically update the file.")
#     print(sync.generate_sync_code('wrap.py', 'demogames/planetWrapping'))
#     exit()

# TODO: Clean up and don't use PIL and stuff
# Thanks to https://stackoverflow.com/questions/38745020/wrap-image-around-a-circle !
import math as m
from PIL import Image
import pygame
from BlazeSudio.Game import world
thispth = __file__[:__file__.rindex('/')]
world = world.World(thispth+"/planets.ldtk")

imgs = [[], []]
for outlining in (False, True):
    for lvl in range(len(world.ldtk.levels)):
        Ro = 100.0
        Ri = 50.0
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

        # img = [[1 for x in range(int(width))] for y in range(int(height))]
        cir = [[0 for x in range(int(Ro * 2))] for y in range(int(Ro * 2))]

        if outlining:
            for i in world.get_level(lvl).layers:
                i.tileset = None # So it has to render blocks instead >:)
        pg = world.get_pygame(lvl, transparent_bg=True)
        imageStr = pygame.image.tostring(pg,"RGBA",False)
        image = Image.frombytes("RGBA", pg.get_size(), imageStr)
        pixels = image.load()
        #pixels = [list(imageStr[i*4:(i+1)*4]) for i in range(len(imageStr)//4)]
        width, height = pg.get_size()

        for i in range(int(Ro)):
            # outer_radius = Ro*m.cos(m.asin(i/Ro))
            outer_radius = m.sqrt(Ro*Ro - i*i)
            for j in range(-int(outer_radius),int(outer_radius)):
                if i < Ri:
                    # inner_radius = Ri*m.cos(m.asin(i/Ri))
                    inner_radius = m.sqrt(Ri*Ri - i*i)
                else:
                    inner_radius = -1
                if j < -inner_radius or j > inner_radius:
                    # this is the destination
                    x = Ro+j
                    y = Ro-i
                    # calculate source
                    angle = m.atan2(y-Ro,x-Ro)/2
                    distance = m.sqrt((y-Ro)*(y-Ro) + (x-Ro)*(x-Ro))
                    distance = m.floor((distance-Ri+1)*(height-1)/(Ro-Ri))
                    if distance >= height:
                        distance = height-1
                    col = pixels[int(width*angle/m.pi) % width, height-distance-1]
                    if outlining:
                        if col[3] == 3:
                            col = (0, 0, 0, 3)
                        else:
                            col = (255, 255, 255)
                    cir[int(y)][int(x)] = col
                    y = Ro+i
                    # calculate source
                    angle = m.atan2(y-Ro,x-Ro)/2
                    distance = m.sqrt((y-Ro)*(y-Ro) + (x-Ro)*(x-Ro))
                    distance = m.floor((distance-Ri+1)*(height-1)/(Ro-Ri))
                    if distance >= height:
                        distance = height-1
                    col = pixels[int(width*angle/m.pi) % width, height-distance-1]
                    if outlining:
                        if col[3] == 3:
                            col = (0, 0, 0, 3)
                        else:
                            col = (255, 255, 255)
                    cir[int(y)][int(x)] = col
        imgs[outlining].append(cir)

def render(imgs, fname):
    list_image = [item for sublist1 in imgs for sublist2 in sublist1 for item in sublist2]
    new_image = Image.new("RGBA", (len(imgs[0][0]), len(imgs[0])*len(imgs)))
    new_image.putdata(list_image)
    new_image = new_image.resize((size, size*len(imgs)), Image.Resampling.NEAREST)
    new_image.save(os.path.dirname(__file__)+"/"+fname, "PNG")
    #new_image.show()

render(imgs[0], "out.png")
render(imgs[1], "colls.png")
