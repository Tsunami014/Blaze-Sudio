import json, re
from noise import pnoise2
from os.path import exists
from random import choice
from math import floor

try:
    from utils.characters import *
    from utils.storyline import *
    from utils.terrainGen import Map
except ImportError:
    from characters import *
    from storyline import *
    from terrainGen import Map

# because sometimes this needs to be separate from the try and except above
try:
    empty = json.load(open('utils/blank.ldtk'))
except:
    empty = json.load(open('empty.ldtk'))

def create_iid():
    # 8d9217c0-3b70-11ee-849e-1d317aac187d
    r = lambda: choice('1234567890qwertyuiopasdfghjklzxcvbnm')
    return f'{"".join([r() for _ in range(8)])}-{"".join([r() for _ in range(4)])}-{"".join([r() for _ in range(4)])}-{"".join([r() for _ in range(4)])}-{"".join([r() for _ in range(12)])}'

class World:
    def __init__(self, name, idea, size, size2=50, quality=500, override=False):
        """
        A World!

        Parameters
        ----------
        name : str
            the name of the world. Can be anything that you would name a file. *foreshadowing* Needs to be unique with other worlds.
        idea : str
            the idea of the world.
        size : int
            The amount of layers to create.
        size2 : int, optional
            The size of the world "chunks", by default 50 (ldtk blocks)
        quality : int, optional
            The quality of the terrain generation. Also puts a limit on how much output it has. Defaults to 500
            Think of this as the amount of pixels the output generates, and the size is the size of the chunks.
        override : bool, optional
            Whether or not to override the currently saved level with the same name (if there is one), by default False
        """
        path = name+'.ldtk'
        self.path = path
        self.idea = idea
        self.data = None
        if exists(path) and not override:
            self.data = json.load(open(path, 'r'))
        else:
            self.data = empty.copy()
            self.data['tutorialDesc'] = 'ERROR!!' # So that if you look at the file and this hasn't finished it's setup then... Oh no! MAYBE TODO: error codes (300 error)
            self.data['worldLayout'] = choice(['Gridvania', 'Free'])
            self.data['levels'] = [
                empty['levels'][0].copy() for i in range(size)
            ]
            j = 0
            m = Map(quality, None, generateTrees=False)
            print('Generating levels...')
            for level in self.data['levels']:
                level['identifier'] = 'Level_'+str(j)
                level['iid'] = create_iid()
                level['uid'] = j
                level['worldX'] = j * size2 * 16
                layer = level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('World')]
                l = m(size2, size2, j*size2)
                layer['intGridCsv'] = []
                for i in l: layer['intGridCsv'].extend(i)
                for i in level['layerInstances']:
                    i['iid'] = create_iid()

                j += 1
            self.data['tutorialDesc'] = 'This is your generated world! Feel free to edit anything!'
            # save to file
            print('Formatting and saving output... (may take a while)...')
            txt = json.dumps(self.data, indent=4)
            for i in re.findall(r'(\n *?\d+?(,|\n))', txt):
                txt = txt.replace(i[0], re.findall(r'\d+,?', i[0])[0])
            #for i in re.findall(r'((\d,){70})', txt):
            #    txt = txt.replace(i[0], '\n						'+i[0])
            #txt = txt.replace('"~', '[').replace('~"', ']')
            txt = txt.replace('                            ]', ']')
            open(path, 'w+').write(txt)

w = World('test', '', 2, override=True)
pass
