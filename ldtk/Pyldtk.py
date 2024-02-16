import json
from math import floor
import pygame
import os

def get_data(file):
    with open(file, "r") as data:
        return json.loads(data.read())

## This is object holds all the data for a .ldtk file
class Ldtk:
    def __init__(self, ldtkfile): ## It takes in the file path
        self.ldtkData = get_data(ldtkfile) ## Loads the JSON
        self.header = self.ldtkData['__header__'] ## Sets the header info to something more convenient

        for k, v in self.ldtkData.items(): ## Here what it does is load all the floating information into the object as attributes  
            if not isinstance(v, dict) or not isinstance(v, list): ## but it ignores all the lists and dictionary to handle them seperately
                self.__dict__[k] = v
            else:
                print(v)
        
        self.levels = []

        for l in self.ldtkData['levels']:
            self.levels.append(Ldtklevel(l, ldtkfile, self.defs))

class LdtkJSON:
    def __init__(self, jsoninf, fileloc=''): ## It takes in JSON
        self.ldtkData = jsoninf
        self.header = self.ldtkData['__header__'] ## Sets the header info to something more convenient

        for k, v in self.ldtkData.items(): ## Here what it does is load all the floating information into the object as attributes
            if not isinstance(v, dict) or not isinstance(v, list): ## but it ignores all the lists and dictionary to handle them seperately
                self.__dict__[k] = v
            else:
                print(v)
        
        self.tilesets = {}
        for i in self.defs['tilesets']:
            t = Tileset(fileloc, i)
            self.tilesets[t.uid] = t
        
        self.levels = []

        for l in self.ldtkData['levels']:
            self.levels.append(Ldtklevel(l, self.tilesets, self.defs))

class Tileset:
    def __init__(self, fileloc, data):
        self.data = data
        for k, v in self.data.items():
            if k.startswith('__'): 
                k = k[1:]
            self.__dict__[k] = v
        if self.relPath != None:
            self.tilesetPath = self.relPath
            if self.tilesetPath.startswith('..'):
                self.tilesetPath = os.path.abspath(os.path.join(os.getcwd(), fileloc, self.tilesetPath))
            self.tileSet = pygame.image.load(os.path.join(os.getcwd(),fileloc,self.tilesetPath)).convert_alpha()
    
    def getTile(self, tile, gridsize):
        end = self.tileSet.subsurface(pygame.Rect(tile.src.x, tile.src.y, self.tileGridSize, self.tileGridSize))
        return pygame.transform.scale(end, (gridsize, gridsize))

class Ldtklevel:
    def __init__(self, data, tilesets, defs):
        self.defs = defs
        self.data = data
        self.tilesets = tilesets
        for k, v in self.data.items():
            if k.startswith('__'): 
                k = k[1:]
            self.__dict__[k] = v
        
        ids = [i['identifier'] for i in defs['layers']]
        
        self.layers = [layer(l, self, defs['layers'][ids.index(l['__identifier'])]) for l in self.layerInstances]
        self.layers.reverse() 

        self.width, self.height = self.pxWid, self.pxHei   
    
    def getTileLayers(self):
        return list(l for l in self.layers if l._type == "Tiles")

class layer:
    def __init__(self, data, level, moreData):
        self.data = data
        md = moreData.copy()
        md.pop('__type') # These are already in self.data, so we don't need the extra keys 
        md.pop('type')
        md.pop('identifier')
        self.data.update(md)
        self.level = level
        self.tilesets = level.tilesets
        self.tiles = None
        for k, v in self.data.items():
            if k[0:2] == '__':      ## Note this part where python seems to dislike the use of __ so I reduced it to a single underscore
                self.__dict__[k[1:]] = v
            else:
                self.__dict__[k] = v
        
        if self._type == "Tiles":
            self.loadTileSheet()

    def loadTileSheet(self):
        if self.gridTiles == []:
            self.tiles = [tile(t, self) for t in self.autoLayerTiles]
        else:
            self.tiles = [tile(t, self) for t in self.gridTiles]
    
    def getImg(self):
        end = pygame.Surface((self._cWid * self._gridSize, self._cHei * self._gridSize)).convert_alpha()
        end.fill((255, 255, 255, 1))
        if self._tilesetDefUid == None:
            # TODO: add support for non-tileset things for not just intgrid (i.e. is just colour, non-rendered)
            if self._type == 'IntGrid':
                vals = [i['value'] for i in self.intGridValues]
                for i in range(len(self.intGridCsv)):
                    col = pygame.Surface((self.gridSize, self.gridSize)).convert_alpha()
                    if self.intGridCsv[i] == 0 or self.intGridCsv[i] not in vals:
                        col.fill((255, 255, 255, 1))
                    else:
                        h = self.intGridValues[vals.index(self.intGridCsv[i])]['color'].lstrip('#')
                        col.fill(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
                    end.blit(col, ((i%self._cWid)*self.gridSize, floor(i/self._cWid)*self.gridSize))
            else:
                end.fill((255, 255, 255, 1))
            return end
        tset = self.tilesets[self._tilesetDefUid]
        if self.tiles == None: self.loadTileSheet()
        for j in range(len(self.tiles)):
            i = self.tiles[j]
            end.blit(tset.getTile(i, self._gridSize), i.pos)
        return end

class tile:
    def __init__(self, data, layer):
        self.data = data
        self.layer = layer
        for k, v in self.data.items():
            if k[0:2] == '__':      
                self.__dict__[k[1:]] = v
            else:
                self.__dict__[k] = v

        self.pos = pygame.Vector2(tuple(self.px))
        self.src = pygame.Vector2(tuple(self.src))
        
        # THINGS TO KNOW:
        # self.f = flip: 0=no flip, 1=flip x, 2=flip y, 3=flip both
        # self.src = position of the tile IN THE TILESET
        # self.a = alpha (opacity) of the tile (1=full,0=invisible)
        # self.px (as from above, self.pos) = coordinates of the tile IN THE LAYER. Don't forget layer offsets, if they exist!
    
    def getImg(self):
        return self.layer.tileSet[self.layer._tilesetDefUid].getTile(self.src.x, self.src.y, self.layer._gridSize)
