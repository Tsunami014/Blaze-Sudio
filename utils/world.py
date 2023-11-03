import json, re
from os.path import exists
from random import choice
from math import floor, sqrt
from copy import deepcopy

try:
    from utils.characters import *
    from utils.storyline import *
    from utils.terrainGen import *
    import utils.Pyldtk as ldtk
except ImportError:
    from characters import *
    from storyline import *
    from terrainGen import *
    import Pyldtk as ldtk

folder = 'data/worlds/'

# because sometimes this needs to be separate from the try and except above
try:
    empty = json.load(open('utils/blank.ldtk'))
except:
    empty = json.load(open('empty.ldtk'))
    folder = '../' + folder

def create_iid():
    # 8d9217c0-3b70-11ee-849e-1d317aac187d
    r = lambda: choice('1234567890qwertyuiopasdfghjklzxcvbnm')
    return f'{"".join([r() for _ in range(8)])}-{"".join([r() for _ in range(4)])}-11ee-{"".join([r() for _ in range(4)])}-{"".join([r() for _ in range(12)])}'

class World:
    def __init__(self, filename, name='', idea='', size=None, size2=50, quality=500, override=False, make_new=True):
        """
        A World!

        Parameters
        ----------
        filename : str
            The name of the path. Does not affect anything. Must be unique.
        name : str
            the name of the world. Can be anything.
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
        make_new : bool, optional
            Whether or not to make a new world if the name specified does not exist. Defaults to True
        """
        path = (folder+filename).replace('/', '\\')
        if not path.endswith('\\'): path += '\\'
        self.path = path
        if (not exists(path) or override) and not make_new:
            if name == '' or idea == '' or size == None:
                raise KeyError('You MUST have name, idea and size args OR turn make_new on OR turn override off because the file does not exist or overrride is on!')
            self.name = name
            self.idea = idea
        self.data = {}
        if exists(path) and not override:
            self.data = json.load(open(path+'world.ldtk', 'r'))
            dat = json.load(open(path+'dat.json', 'r'))
            self.name = dat['name']
            self.idea = dat['idea']
        elif make_new:
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
            json.dump({
                'version': 1.0, # Change every time the version OF THE JSON/LDTK FILES UPDATES;
                # MINOR version update = anything to do with world loading changes
                # MAJOR version update = something updates and is so bad it breaks any feature
                'name': name,
                'idea': idea
                }, os.getcwd()+'\\'+path+'dat.json')
            open(os.getcwd()+'\\'+path+'world.ldtk', 'w+').write(txt)
    def get_pygame(self, lvl=0):
        if self.data != {}: return ldtk.LdtkJSON(self.data, folder).levels[lvl].layers[1].getImg()
    # TODO: have a number in the intgrid specifically for oceans, and get that from the terrain gen

if __name__ == '__main__':
    w = World('test', 'Test World', 'A world for testing random stuff', 25, quality=500, override=True)
    pass
