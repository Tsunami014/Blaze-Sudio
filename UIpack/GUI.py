import pygame
pygame.init()
WIN = pygame.display.set_mode((500, 500))

import os
if os.getcwd().endswith('UIpack'):
    app = ''
else: app = 'UIpack/'

from xml.dom.minidom import parse
def getAll(colour):
    if colour == 'PNG':
        return {i.name[:-4]: pygame.image.load(app+'PNGs/'+i.name).convert_alpha() for i in os.listdir(app+'PNGs')}
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

def get_specific(name):
    try:
        colour = name[:name.index('_')]
    except:
        raise NameError(
            f'The colour for the name {name} was not found!\n\
The colour of the element should be before the first \'_\' (e.g. `grey_button01` the colour would be grey)'
        )
    if colour == 'PNG':
        return pygame.image.load(app+'PNGs/'+name[4:]).convert_alpha()
    p = parse(app+'Spritesheet/%sSheet.xml'%colour)
    sur = pygame.image.load(app+'Spritesheet/%sSheet.png'%colour).convert_alpha()
    elms = p.getElementsByTagName('SubTexture')
    i = None
    for j in elms: 
        if j.attributes._attrs['name'] == name:
            i = j
            break
    if i == None:
        raise NameError(
            f'The name "{name}" was not found in the coloursheet "{colour}"!'
        )
    return sur.subsurface(pygame.Rect(
        int(i.attributes._attrs['x'].value), 
        int(i.attributes._attrs['y'].value), 
        int(i.attributes._attrs['width'].value), 
        int(i.attributes._attrs['height'].value)
    ))

import UIpack.consts as Cs
from json import load
def Element(elm, colour, state=None):
    """Get the code for an element!

    Parameters
    ----------
    elm : `Cs._____` (NOT `Cs.C______`)
        The element to get the value of
    colour : `Cs.C_____`
        The colour of the element
        Please note also that some elements are just one colour, so this value will be ignored. But not all, so still include it anyways
    state : tuple, optional
        This is only for buttons, by default None
        For a button you need to specify the following in the tuple in this order:
         - The size of the button (`Cs.S_____`)
         - Whether the button is pressed ('D' for Down) or not pressed ('U' for Up)
        PLEASE NOTE THAT OUTLINE BUTTONS HAVE NO DOWN STATE SO DO NOT ATTEMPT TO GET THEIR DOWN STATE
    Returns
    -------
    str
        The code for an element. To get the pic, use `get_specific(result)`
    """
    if elm == Cs.HEMPTY:
        return 'grey_box'
    elif elm == Cs.OINPUT:
        return 'grey_button05'
    elif elm == Cs.RBLANK:
        return 'grey_circle'
    elif elm.startswith('A'): # Arrow
        return 'grey_arrow'+elm[1:]
    elif elm.startswith('D'): # Dropdown
        'PNG_dropdown'+elm[1:]
    else:
        j = load(open(app+'Spritesheet/key.json'))
        if elm.startswith('B'): # Button
            return colour + '_' + 'button' + j[colour[1:]]['B'][elm[1]+state[0][1]+state[1]]
        else:
            return colour + '_' + j[colour[1:]][elm[0]][elm[1]]
