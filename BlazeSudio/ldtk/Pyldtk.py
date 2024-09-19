import json
import pygame
import os
import BlazeSudio.collisions as colls
from math import ceil
from importlib.resources import files

## This is object holds all the data for a .ldtk file
# TODO: fieldinstance class WITH DEFAULTS
class LdtkJSON:
    def __init__(self, jsoninf, fileloc=''): ## It takes in JSON
        self.ldtkData = jsoninf
        self.header = self.ldtkData['__header__']
        self.defs = self.ldtkData['defs']
        
        self.tilesets = {}
        for i in self.defs['tilesets']:
            t = Tileset(fileloc, i)
            self.tilesets[t.uid] = t
        
        self.levels = [Ldtklevel(lvl, self.tilesets, self.defs) for lvl in self.ldtkData['levels']]

class Ldtk(LdtkJSON):
    def __init__(self, ldtkfile): ## It takes in the file path
        with open(ldtkfile, "r") as data:
            dat = json.loads(data.read())
        super().__init__(dat)

class Tileset:
    def __init__(self, fileloc, data):
        self.data = data
        self.fileLoc = fileloc

        self.identifier = self.data['identifier']
        self.uid = self.data['uid']
        self.tileGridSize = self.data['tileGridSize']

        self.tilesetPath = None
        if self.data['relPath'] is not None:
            self.tilesetPath = self.data['relPath']
            if self.tilesetPath.startswith('..'):
                self.tilesetPath = os.path.abspath(os.path.join(fileloc,'../',self.tilesetPath))
            self.tileSet = pygame.image.load(os.path.abspath(os.path.join(fileloc,'../',self.tilesetPath))).convert_alpha()
        elif self.data['embedAtlas'] == 'LdtkIcons' and self.data['relPath'] is None:
            self.tilesetPath = str(files('BlazeSudio') / 'ldtk/internal-icons.png')
            self.tileSet = pygame.image.load(self.tilesetPath).convert_alpha()
    
    def subsurface(self, x, y, w, h):
        return self.tileSet.subsurface(pygame.Rect(x, y, w, h))
    
    def getTile(self, tile):
        end = pygame.transform.flip(self.tileSet.subsurface(pygame.Rect(tile.src[0], tile.src[1], self.tileGridSize, self.tileGridSize)), *tile.flip)
        return pygame.transform.scale(end, (self.tileGridSize, self.tileGridSize))

class Entity:
    def __init__(self, layer, data, tilesets):
        self.layer = layer
        self.data = data
        self.tilesets = tilesets
        
        self.identifier = self.data['__identifier']
        self.iid = self.data['iid']
        self.defUid = self.data['defUid'] # The UID of the entity definition
        self.tileData = self.data['__tile']
        self.fieldInstances = self.data['fieldInstances']
        self.layerId = self.data['layerId']

        self.width = self.data['width']
        self.height = self.data['height']
        
        self.gridSze = self.layer['__gridSize']
        self.layerOffset = [self.layer['pxOffsetX'], self.layer['pxOffsetY']]
        self.pivot = self.data['__pivot']
        self.ScaledPos = [
            self.data['px'][0] + self.layerOffset[0],# - self.pivot[0] * self.width,
            self.data['px'][1] + self.layerOffset[1]# - self.pivot[1] * self.height
        ]
        self.UnscaledPos = [
            self.data['px'][0] / self.gridSze,
            self.data['px'][1] / self.gridSze
        ]
    
    def scale_pos(self, pos):
        return (
            pos[0] * self.gridSze + self.layerOffset[0],# - self.pivot[0] * self.width,
            pos[1] * self.gridSze + self.layerOffset[1]# - self.pivot[1] * self.height
        )

    def unscale_pos(self, pos):
        return (
            pos[0] / self.gridSze - self.layerOffset[0],# + self.pivot[0] * self.width,
            pos[1] / self.gridSze - self.layerOffset[1]# + self.pivot[1] * self.height
        )
    
    def get_tile(self, ui=False):
        if not self.tileData:
            return pygame.Surface((self.width, self.height)).convert_alpha()
        return self.tilesets[self.tileData['tilesetUid']].subsurface(self.tileData['x'], 
                                                                     self.tileData['y'], 
                                                                     self.tileData['w'], 
                                                                     self.tileData['h'])

class Ldtklevel:
    def __init__(self, data, tilesets, defs):
        self.defs = defs
        self.data = data
        self.tilesets = tilesets
        
        self.identifier = self.data['identifier']
        self.iid = self.data['iid']
        self.uid = self.data['uid']
        self.worldPos = [self.data['worldX'], self.data['worldY'], self.data['worldDepth']]
        self.bgColour = self.data['bgColor'] or self.data['__bgColor']
        self.fieldInstances = self.data['fieldInstances'] # The specific level flags
        self.sizePx = [self.data['pxWid'], self.data['pxHei']]
        self.neighbours = self.data['__neighbours']
        
        ids = [i['identifier'] for i in defs['layers']]
        
        self.entities = []
        self.layers = []
        for lay in self.data['layerInstances']:
            if lay['__type'] == 'Entities':
                self.entities.extend([Entity(lay, {**i, 'layerId': lay['__identifier']}, self.tilesets) for i in lay['entityInstances']])
            else:
                self.layers.append(layer(lay, self))
        self.layers.reverse() 
    
    # TODO: Get layer by id
    
    def getTileLayers(self):
        return list(l for l in self.layers if l._type == "Tiles")

class layer:
    def __init__(self, data, level):
        self.data = data
        self.level = level
        self.layerDef = level.defs['layers'][[i['uid'] for i in level.defs['layers']].index(self.data['layerDefUid'])]
        self.tilesets = level.tilesets

        self.identifier = self.data['__identifier']
        self.iid = self.data['iid']
        self.defUid = self.data['layerDefUid']
        self.type = self.data['__type']
        self.gridSize = self.data['__gridSize']
        self.sizeCells = [self.data['__cWid'], self.data['__cHei']]
        self.sizePx = [self.sizeCells[0] * self.gridSize, self.sizeCells[1] * self.gridSize]
        self.opacity = self.data['__opacity']
        self.visible = self.data['visible']
        self.pxOffset = [self.data['__pxTotalOffsetX'], self.data['__pxTotalOffsetY']]
        self.intGridValues = self.layerDef['intGridValues']
        # TODO: if self.layerDef['parallaxScaling']
        self.tileset = None
        if self.data['__tilesetDefUid'] is not None:
            self.tileset = self.tilesets[self.data['__tilesetDefUid']]

        self.tiles = None
        self.intgrid = IntGridCSV(self.data['intGridCsv'], *self.sizeCells, self.pxOffset, self.gridSize)
        
        if self.type == "Tiles":
            self.loadTileSheet()

    def loadTileSheet(self):
        if self.data['gridTiles'] == []:
            self.tiles = [tile(t, self) for t in self.data['autoLayerTiles']]
        else:
            self.tiles = [tile(t, self) for t in self.data['gridTiles']]
    
    def getImg(self):
        end = pygame.Surface(self.sizePx).convert_alpha()
        end.fill((255, 255, 255, 1))
        if not self.data['visible']:
            return end
        if self.tileset is None:
            if self.type == 'IntGrid':
                vals = [i['value'] for i in self.intGridValues]
                for y in range(len(self.intgrid)):
                    for x in range(len(self.intgrid[y])):
                        col = pygame.Surface((self.gridSize, self.gridSize)).convert_alpha()
                        if self.intgrid[y, x] == 0 or self.intgrid[y, x] not in vals:
                            col.fill((255, 255, 255, 1))
                        else:
                            h = self.intGridValues[vals.index(self.intgrid[y, x])]['color'].lstrip('#')
                            col.fill(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
                        end.blit(col, (x*self.gridSize, y*self.gridSize))
            return end
        if self.tiles is None:
            self.loadTileSheet()
        for i in self.tiles:
            end.blit(self.tileset.getTile(i), i.pos)
        return end

class IntGridCSV:
    def __init__(self, intgrid, cwid, chei=None, offsets=[0, 0], gridsize=1):
        self.rawintgrid = intgrid
        self.cwid = cwid
        self.chei = chei or ceil(len(intgrid) / self.cwid)
        self.offsets = offsets
        self.gridsze = gridsize
        self.intgrid = [intgrid[cwid*i:cwid*(i+1)] for i in range(chei)]
        self.rects = None
    
    def getRects(self, matches):
        if isinstance(matches, int):
            matches = [matches]
        if self.rects is not None:
            li = []
            for i in self.rects:
                if i in matches:
                    li.extend(self.rects[i])
            return li
        rs = {}
        typ = None
        for y in range(len(self.intgrid)):
            for x in range(len(self.intgrid[y])):
                typ = self.intgrid[y][x]
                if typ in rs:
                    rs[typ].append(colls.Rect(x*self.gridsze+self.offsets[0], y*self.gridsze+self.offsets[1], self.gridsze, self.gridsze))
                else:
                    rs[typ] = [colls.Rect(x*self.gridsze, y*self.gridsze, self.gridsze, self.gridsze)]
        if typ is not None:
            rs[typ] = colls.ShapeCombiner.to_rects(*rs[typ])
        self.rects = rs
        return self.getRects(matches)
    
    def __iter__(self):
        return iter(self.intgrid)
    
    def __len__(self):
        return len(self.intgrid)

    def __getitem__(self, args):
        if isinstance(args, int):
            return self.intgrid[args]
        y, x = args[0], (None if len(args) < 2 else args[1])
        if y is None:
            return self.intgrid[y]
        return self.intgrid[y][x]

class tile:
    def __init__(self, data, layer):
        self.data = data
        self.layer = layer

        self.px = self.data['px']
        self.src = self.data['src']
        self.t = self.data['t']
        self.a = self.data['a']
        # what is self.data['d']???

        self.pos = [self.px[0] + self.layer.pxOffset[0], self.px[1] + self.layer.pxOffset[1]]
        self.src = self.src
        
        self.flip = [self.data['f'] in [1, 3], self.data['f'] in [2, 3]]
        
        # THINGS TO KNOW:
        # self.data['f'] = flip: 0=no flip, 1=flip x, 2=flip y, 3=flip both
        # self.src = position of the tile IN THE TILESET
        # self.a = alpha (opacity) of the tile (1=full,0=invisible)
        # self.px = coordinates of the tile IN THE LAYER. Don't forget layer offsets, if they exist!
        # self.pos = coordinates of the tile IN THE LAYER,with offsets!
    
    def getImg(self):
        return self.layer.tileset.getTile(self)
