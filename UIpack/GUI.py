import pygame
pygame.init()
WIN = pygame.display.set_mode((500, 500))

import os
if os.getcwd().endswith('UIpack'):
    app = ''
else: app = 'UIpack/'

from xml.dom.minidom import parse
def getAll(colour):
    p = parse(app+'Spritesheet/%sSheet.xml'%colour)
    sur = pygame.image.load(app+'Spritesheet/%sSheet.png'%colour).convert_alpha()
    #a = {i.attributes._attrs['name'].value: {j: int(i.attributes._attrs[j].value) for j in i.attributes._attrs.keys() if j != 'name'} for i in p.getElementsByTagName('SubTexture')}
    return {i.attributes._attrs['name'].value[len(colour)+1:-4]: 
        sur.subsurface(pygame.Rect(
        int(i.attributes._attrs['x'].value), 
        int(i.attributes._attrs['y'].value), 
        int(i.attributes._attrs['width'].value), 
        int(i.attributes._attrs['height'].value)
        )) for i in p.getElementsByTagName('SubTexture')}

def scrprint(sur, pos=(0, 0), cl=True):
    pygame.event.pump()
    if cl: WIN.fill((255, 255, 255))
    WIN.blit(sur, pos)
    pygame.display.update()
def allscrprint(l):
    WIN.fill((255, 255, 255))
    pos = [0, 0]
    spacingy = 0
    for i in l:
        spacingy = max(spacingy, i.get_height())
        if pos[0] + i.get_width() > WIN.get_width():
            pos[0] = 0
            pos[1] += spacingy + 10
            spacingy = 0
        scrprint(i, pos, False)
        pos[0] += i.get_width() + 10

show = lambda col: allscrprint(getAll(col).values())

from random import shuffle

def colours():
    l = ['blue', 'green', 'grey', 'red', 'yellow']
    shuffle(l)
    while True:
        for i in l:
            yield i

c = colours()
while True:
    if pygame.event.get(pygame.QUIT):
        show(next(c))

pass
