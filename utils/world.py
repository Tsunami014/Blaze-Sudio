import json, re
from noise import pnoise2
from os.path import exists
from random import choice
from math import floor

try:
    from utils.characters import *
    from utils.storyline import *
except ImportError:
    from characters import *
    from storyline import *

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
    def __init__(self, path, idea, size, override=False):
        self.path = path
        self.idea = idea
        self.data = None
        if exists(path) and not override:
            self.data = json.load(open(path, 'r'))
        else:
            self.data = empty.copy()
            self.data['tutorialDesc'] = 'ERROR!!' # So that if you look at the file and this hasn't finished it's setup then... Oh no!
            self.data['worldLayout'] = choice(['Gridvania', 'Free'])
            self.data['levels'] = [
                empty['levels'][0].copy() for i in range(size)
            ]
            j = 0
            for level in self.data['levels']:
                level['identifier'] = 'Level_'+str(j)
                j += 1
                level['iid'] = create_iid()
                layer = level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('World')]
                mapfunc = lambda inp: round((inp * (10/3) + 1) * 2 - 1)
                layer['intGridCsv'] = list(map(mapfunc, [pnoise2(
                            (i % layer['__cWid']) / layer['__cWid'], 
                            floor(i / layer['__cWid']) / ((len(layer['intGridCsv'])+1)//2) // layer['__cWid'])
                for i in range((len(layer['intGridCsv'])+1)//2)]))
            self.data['tutorialDesc'] = 'This is your generated world! Feel free to edit anything!'
            # save to file
            txt = json.dumps(self.data, indent=4)
            for i in re.findall(r'\n *?\d+?(,|\n)', txt):
                txt.replace(i, re.findall(r'\d+', i)[0])
            #txt = txt.replace('"~', '[').replace('~"', ']')
            open(path, 'w+').write(txt)

w = World('test.ldtk', '', 3, True)
pass