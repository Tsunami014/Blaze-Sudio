import os, sys
if 'demogames/planetWrapping' in sys.path[0]:
    sys.path.append(os.path.abspath(os.path.join(__file__, '../../../'))) # Make sure you can still access BS
from BlazeSudio.ldtk import sync
if not sync.is_synced():
    print(sync.explanation())
    print("For this file, it's best to use it with the 'after save', so it will automatically update the file.")
    print(sync.generate_sync_code('wrap.py', 'demogames/planetWrapping'))
    exit()

# TODO: Clean up and don't use PIL and stuff
# Thanks to https://stackoverflow.com/questions/38745020/wrap-image-around-a-circle !
import math as m
from PIL import Image
import pygame
from BlazeSudio.Game import world
thispth = __file__[:__file__.rindex('/')]

lvl = 0
world = world.World(thispth+"/planets.ldtk")

Ro = 100.0
Ri = 50.0
size = 128
for e in world.ldtk.levels[lvl].entities:
    if e._identifier == 'Settings':
        for i in e.fieldInstances:
            if i['__identifier'] == 'Ro':
                Ro = i['__value'] or Ro
            if i['__identifier'] == 'Ri':
                Ri = i['__value'] or Ri
            if i['__identifier'] == 'size':
                size = i['__value'] or size

# img = [[1 for x in range(int(width))] for y in range(int(height))]
cir = [[0 for x in range(int(Ro * 2))] for y in range(int(Ro * 2))]

# image = Image.open('0vWEI.png')
# image = Image.open('this-is-a-test.png')
# data = image.convert('RGB')
pg = world.get_pygame(lvl, transparent_bg=True)
pil_string_image = pygame.image.tostring(pg,"RGBA",False)
image = Image.frombytes("RGBA", pg.get_size(), pil_string_image)
pixels = image.load()
width, height = image.size

def shom_im(img):  # for showing data as image
    list_image = [item for sublist in img for item in sublist]
    new_image = Image.new("RGBA", (len(img[0]), len(img)))
    new_image.putdata(list_image)
    new_image = new_image.resize((size, size), Image.Resampling.NEAREST)
    new_image.save(os.path.dirname(__file__)+"/out.png","PNG")
    #new_image.show()


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
            # solid:
            # cir[int(Ro-i)][int(Ro+j)] = (255,255,255)
            # cir[int(Ro+i)][int(Ro+j)] = (255,255,255)
            # textured:

            x = Ro+j
            y = Ro-i
            # calculate source
            angle = m.atan2(y-Ro,x-Ro)/2
            distance = m.sqrt((y-Ro)*(y-Ro) + (x-Ro)*(x-Ro))
            distance = m.floor((distance-Ri+1)*(height-1)/(Ro-Ri))
        #   if distance >= height:
        #       distance = height-1
            cir[int(y)][int(x)] = pixels[int(width*angle/m.pi) % width, height-distance-1]
            y = Ro+i
            # calculate source
            angle = m.atan2(y-Ro,x-Ro)/2
            distance = m.sqrt((y-Ro)*(y-Ro) + (x-Ro)*(x-Ro))
            distance = m.floor((distance-Ri+1)*(height-1)/(Ro-Ri))
        #   if distance >= height:
        #       distance = height-1
            cir[int(y)][int(x)] = pixels[int(width*angle/m.pi) % width, height-distance-1]

shom_im(cir)