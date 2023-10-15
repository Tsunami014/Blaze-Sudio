import json, re
from noise import pnoise2
from os.path import exists
from random import choice
from math import floor, sqrt
from copy import deepcopy

try:
    from utils.characters import *
    from utils.storyline import *
    from utils.terrainGen import *
except ImportError:
    from characters import *
    from storyline import *
    from terrainGen import *

# because sometimes this needs to be separate from the try and except above
try:
    empty = json.load(open('utils/blank.ldtk'))
except:
    empty = json.load(open('empty.ldtk'))

def create_iid():
    # 8d9217c0-3b70-11ee-849e-1d317aac187d
    r = lambda: choice('1234567890qwertyuiopasdfghjklzxcvbnm')
    return f'{"".join([r() for _ in range(8)])}-{"".join([r() for _ in range(4)])}-11ee-{"".join([r() for _ in range(4)])}-{"".join([r() for _ in range(12)])}'

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
            m = Map(quality, None)
            print('Generating file...')
            self.data = empty.copy()
            self.data['tutorialDesc'] = 'ERROR!!' # So that if you look at the file and this hasn't finished it's setup then... Oh no! MAYBE TODO: error codes (300 error)
            self.data['worldLayout'] = choice(['Gridvania', 'Free'])
            self.data['levels'] = [
                deepcopy(empty['levels'][0]) for _ in range(size)
            ]
            size3 = floor(sqrt(size))
            j = 0
            for level in self.data['levels']:
                level['identifier'] = 'Level_'+str(j)
                level['iid'] = create_iid()
                level['uid'] = j
                level['worldX'] = (j%size3) * size2 * 16
                level['worldY'] = floor(j/size3) * size2 * 16
                layer = level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('World')]
                l = m(size2, size2, (j%size3)*size2, floor(j/size3)*size2)
                layer['intGridCsv'] = []
                for i in l: layer['intGridCsv'].extend(i)
                level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('World')] = layer
                
                """entities = level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('Entities')]
                entities['entityInstances'] = []
                for ii in m.structures:
                    for i in ii:
                        entities['entityInstances'].append({
							"__identifier": "NPC",
							"__grid": [i[0]//16,i[1]//16],
							"__pivot": [0,0],
							"__tags": ["characters"],
							"__tile": { "tilesetUid": 7, "x": 112, "y": 240, "w": 16, "h": 16 },
							"__smartColor": "#EAD4AA",
							"__worldX": i[0],
							"__worldY": i[1],
							"iid": create_iid(),
							"width": 16,
							"height": 16,
							"defUid": 14,
							"px": [320,336],
							"fieldInstances": [
								{ "__identifier": "Name", "__type": "String", "__value": "A thingy", "__tile": None, "defUid": 15, "realEditorValues": [] },
								{ "__identifier": "Health", "__type": "Int", "__value": 10, "__tile": None, "defUid": 16, "realEditorValues": [] },
								{ "__identifier": "Personality", "__type": "String", "__value": "", "__tile": None, "defUid": 17, "realEditorValues": [] }
							]
						})
                level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('Entities')] = entities"""

                layer2 = level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('Structures')]
                layer2['intGridCsv'] = []
                #l2 = find_plateaus(l)
                l2 = m.get_structs(size2, size2, (j%size3)*size2, floor(j/size3)*size2)
                for i in l2: layer2['intGridCsv'].extend(i)
                level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('Structures')] = layer2

                for i in level['layerInstances']:
                    i['iid'] = create_iid()
                    i['seed'] = randint(1000000, 9999999)
                self.data['levels'][j] = level
                j += 1
            self.data['tutorialDesc'] = 'This is your generated world! Feel free to edit anything!'
            # save to file
            print('Stringing file into JSON...')
            txt = json.dumps(self.data, indent=4)
            print('Formatting data... (may take a while)...')
            for i in re.findall(r'(\n *?\d+?(,|\n))', txt):
                txt = txt.replace(i[0], re.findall(r'\d+,?', i[0])[0])
            #for i in re.findall(r'((\d,){70})', txt):
            #    txt = txt.replace(i[0], '\n						'+i[0])
            #txt = txt.replace('"~', '[').replace('~"', ']')
            txt = txt.replace('                            ]', ']').replace('                    ]', ']')
            print('Saving to file...')
            open(path, 'w+').write(txt)

w = World('test', '', 16, quality=500, override=True)
pass
