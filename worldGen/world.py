from os.path import exists, join
from random import choice
from math import floor, sqrt, ceil
from copy import deepcopy
from shutil import copytree
import shutil, json

from utils.characters import *
from utils.storyline import *
from worldGen.terrainGen import *
import ldtk.Pyldtk as ldtk
from pygame import Surface, Rect
import pygame.draw

folder = 'data/worlds/'

empty = json.load(open('data/defaultWorld/world.ldtk'))

def create_iid():
    # 8d9217c0-3b70-11ee-849e-1d317aac187d
    r = lambda: choice('1234567890qwertyuiopasdfghjklzxcvbnm')
    return f'{"".join([r() for _ in range(8)])}-{"".join([r() for _ in range(4)])}-11ee-{"".join([r() for _ in range(4)])}-{"".join([r() for _ in range(12)])}'

class World:
    def __init__(self, filename, name='', idea='', size=None, size2=50, quality=None, seed=None, override=False, make_new=True, callback=lambda *args: None):
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
            The amount of levels to create (in a square).
        size2 : int, optional
            The size of the world "chunks", by default 50 (ldtk blocks)
        quality : int, optional
            The quality of the terrain generation. Also puts a limit on how much output it has.
            Think of this as the amount of pixels the output generates, and the size is the size of the chunks.
            If you leave this, it will make this number `size * size2` which is what you want 100% of the time.
        seed : int, optional
            The seed of the generation, if None will be random
        override : bool, optional
            Whether or not to override the currently saved level with the same name (if there is one), by default False
        make_new : bool, optional
            Whether or not to make a new world if the name specified does not exist. Defaults to True
        callback : function, optional
            When the progress on the generation gets further, cal this function with the info on it. Can put `print` here if you want to print out the progress.
        """
        path = (folder+filename).replace('/', '\\')
        if not path.endswith('\\'): path += '\\'
        self.path = path
        self.data = {}
        if exists(path) and not override:
            self.data = json.load(open(path+'world.ldtk', 'r'))
            dat = json.load(open(path+'dat.json', 'r'))
            self.name = dat['name']
            self.idea = dat['idea']
        elif make_new:
            if os.path.exists('data/worlds/'+filename):
                shutil.rmtree('data/worlds/'+filename)
            if name == '' or idea == '' or size == None:
                raise KeyError('You MUST have name, idea and size args OR turn make_new on OR turn override off because the file does not exist or overrride is on!')
            self.name = name
            self.idea = idea
            if quality == None: quality = int((ceil(sqrt(size)) * size2)) # TODO: Make this more efficient by generating a rectangle, not just a square
            m = MapGen()
            for i in m.generate(quality, seed):
                callback(i)
            callback('Generating map...')
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
                level["pxWid"] = 16 * size2
                level["pxHei"] = 16 * size2
                for i in level['layerInstances']:
                    i["__cWid"] = size2
                    i["__cHei"] = size2
                Wlayer = level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('World')]
                l = m(size2, size2, (j%size3)*size2, floor(j/size3)*size2)
                Wlayer['intGridCsv'] = []
                for i in l: Wlayer['intGridCsv'].extend(i)
                level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('World')] = Wlayer
                Olayer = level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('Water')]
                Olayer['intGridCsv'] = []
                for i in m.outs[0][4][floor(j/size3)*size2:(1+floor(j/size3))*size2]: Olayer['intGridCsv'].extend([(0 if k else 1) for k in i[(j%size3)*size2:(1+(j%size3))*size2]])
                
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

                layer2 = level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('Trees')]
                layer2['intGridCsv'] = []
                #l2 = find_plateaus(l)
                l2 = [i[(j%size3)*size2:((j%size3)+1)*size2] for i in m.trees[floor(j/size3)*size2:(1+floor(j/size3))*size2]]
                for i in l2: layer2['intGridCsv'].extend(i)
                level['layerInstances'][[i['__identifier'] for i in level['layerInstances']].index('Trees')] = layer2

                for i in level['layerInstances']:
                    i['iid'] = create_iid()
                    i['seed'] = randint(1000000, 9999999)
                self.data['levels'][j] = level
                j += 1
            self.data['tutorialDesc'] = 'This is your generated world! Feel free to edit anything!'
            # save to file
            callback('Stringing file into JSON...')
            txt = json.dumps(self.data)#, indent=4)
            #callback('Formatting data... (may take a while)...')
            #for i in re.findall(r'(\n *?\d+?(,|\n))', txt):
            #    txt = txt.replace(i[0], re.findall(r'\d+,?', i[0])[0])
            #for i in re.findall(r'((\d,){70})', txt):
            #    txt = txt.replace(i[0], '\n						'+i[0])
            #txt = txt.replace('"~', '[').replace('~"', ']')
            #txt = txt.replace('                            ]', ']').replace('                    ]', ']')
            callback('Copying tree...')
            copytree(join(os.getcwd(),'data/defaultWorld'), join(os.getcwd(), path))
            callback('Saving to files...')
            json.dump({
                'version': "1.0", # Change every time the version OF THE JSON/LDTK FILES UPDATES;
                # MINOR version update = anything to do with world loading changes
                # MAJOR version update = something updates and is so bad it breaks any feature
                'name': name,
                'idea': idea
                }, open(join(os.getcwd(), path, 'dat.json'), 'w+'))
            open(join(os.getcwd(), path, 'world.ldtk'), 'w+').write(txt)
        self.ldtk = ldtk.LdtkJSON(self.data, self.path)
    
    def gen_minimap(self, maxsize=(64, 64), highlights={}):
        """
        Makes a minimap!

        Parameters
        ----------
        maxsize : tuple[int], optional
            The size of the minimap, stretch to fit, by default (64, 64)
        highlights : dict{int: tuple[int,int,int]}, optional
            A dictionary of level numbers and their colours shown on the minimap, by default {}

        Returns
        -------
        pygame.Surface
            The surface of the minimap
        """
        sur = Surface((maxsize[0], maxsize[1])).convert_alpha()
        sur.fill((255, 255, 255, 1))
        w = 8-ceil(sqrt(len(self.ldtk.levels)))
        if w < 2: w = 2

        diff = (min([i.worldX for i in self.ldtk.levels]), 
                min([i.worldY for i in self.ldtk.levels]))
        maxs = (maxsize[0]/max([i.worldX+i.width for i in self.ldtk.levels]), 
                maxsize[1]/max([i.worldY+i.height for i in self.ldtk.levels]))
        for i in range(len(self.ldtk.levels)):
            lvl = self.ldtk.levels[i]
            pygame.draw.rect(sur,
                       ((125, 125, 125) if i not in highlights else highlights[i]), 
                       Rect((lvl.worldX-diff[0])*maxs[0], 
                            (lvl.worldY-diff[1])*maxs[1], 
                            lvl.width*maxs[0], 
                            lvl.height*maxs[1]),
                        border_radius=w)
        pygame.draw.rect(sur, (0, 0, 0), sur.get_rect(), w, 4)
        return sur

    def get_pygame(self, lvl=0):
        if self.data != {}:
            level = self.ldtk.levels[lvl]
            end = Surface((level.width, level.height))
            end.fill(tuple(int(level._bgColor.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)))
            end = end.convert_alpha()
            for i in level.layers:
                end.blit(i.getImg(), (0, 0))
            return end
    # TODO: have a number in the intgrid specifically for oceans, and get that from the terrain gen
