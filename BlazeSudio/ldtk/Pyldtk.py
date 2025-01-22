import json
import pygame
import os
import BlazeSudio.collisions as colls
from math import ceil
from importlib.resources import files
from typing import Any, Callable, Dict, Iterable, List, Literal, Tuple

## This is object holds all the data for a .ldtk file
# TODO: fieldinstance class WITH DEFAULTS
# TODO: make the data, etc. 'private' (i.e. _data or __data)
# TODO: Consistent naming
# TODO: Literal["a", "b"]

class LdtkJSON:
    def __init__(self, jsoninf: Dict[str, str], fileloc: str = ''): ## It takes in JSON
        """
        Instantiate an LDtk file object with it's JSON.

        Args:
            jsoninf (dict): The LDtk file's contents
            fileloc (str, optional): The location of the file. Please fill this in or some references to images may break. Defaults to ''.
        """
        self.ldtkData: Dict = jsoninf
        self.header: Dict = self.ldtkData['__header__']
        self.defs: Dict = self.ldtkData['defs']
        
        self.tilesets: Dict[int, Tileset] = {}
        for i in self.defs['tilesets']:
            t = Tileset(fileloc, i)
            self.tilesets[t.uid] = t
        
        self.levels: List[Ldtklevel] = [Ldtklevel(lvl, self.tilesets, self.defs, fileloc) for lvl in self.ldtkData['levels']]

class Ldtk(LdtkJSON):
    def __init__(self, ldtkfile: str): ## It takes in the file path
        """
        Instantiate an LDtk file object via it's file location.
        Creates an LDtkJSON object with the file's contents.

        Args:
            ldtkfile (str): The LDtk file's path.
        """
        with open(ldtkfile, "r") as data:
            dat = json.loads(data.read())
        super().__init__(dat, ldtkfile)

class Tileset:
    def __init__(self, fileloc: str, data: Dict):
        """
        A Tileset.

        Args:
            fileloc (str): The location of the LDtk file (some of the references to files rely on this).
            data (dict): The data.
        """
        self.data: Dict = data
        self.fileLoc: str = fileloc

        self.identifier: str = self.data['identifier']
        self.uid: int = self.data['uid']
        self.tileGridSize: int = self.data['tileGridSize']

        self.width: int = self.data['__cWid']

        self.tilesetPath: str|None = None
        self.tileSet: pygame.Surface|None = None
        if self.data['relPath'] is not None:
            self.tilesetPath = self.data['relPath']
            self.tileSet = pygame.image.load(os.path.abspath(os.path.join(fileloc,'../',self.tilesetPath))).convert_alpha()
        elif self.data['embedAtlas'] == 'LdtkIcons' and self.data['relPath'] is None:
            self.tilesetPath = str(files('BlazeSudio') / 'ldtk/internal-icons.png')
            self.tileSet = pygame.image.load(self.tilesetPath).convert_alpha()
    
    def getTileData(self, x: int, y: int) -> List[str]:
        """
        Get the tile data at a specific position.

        Args:
            x (int): The x ordinate of the tile.
            y (int): The y ordinate of the tile.

        Returns:
            List[str]: The tile data.
        """
        idx = (y//self.tileGridSize)*self.width + (x//self.tileGridSize)
        datas = []
        for tag in self.data['enumTags']:
            if idx in tag['tileIds']:
                datas.append(tag['enumValueId'])
        return datas
    
    def subsurface(self, x: int, y: int, w: int, h: int) -> pygame.Surface:
        """
        Get a subsurface from this tileset image. Basically just get a smaller segment from the larger image.

        Args:
            x (int): The x ordinate of the start of the subsurfacing
            y (int): The y ordinate of the start of the subsurfacing
            w (int): The width of the subsurface.
            h (int): The height of the subsurface.

        Returns:
            pygame.Surface: The output subsurface
        """
        return self.tileSet.subsurface(pygame.Rect(x, y, w, h))
    
    def getTile(self, tile: 'tile') -> pygame.Surface:
        """
        Gets the image on this tileset that the tile uses.

        Args:
            tile (tile): The tile object.

        Returns:
            pygame.Surface: The image of the tile.
        """
        end = pygame.transform.flip(self.tileSet.subsurface(pygame.Rect(tile.src[0], tile.src[1], self.tileGridSize, self.tileGridSize)), *tile.flip)
        return end

class Entity:
    def __init__(self, layer: Dict, data: Dict, tilesets: Dict[int, Tileset]):
        """
        An entity. What more is there to say?

        Args:
            layer (Dict): The layer. This isn't a layer object as entity layers are different to the others.
            data (Dict): The entity's data.
            tilesets (Dict[int, Tileset]): All the tilesets.
        """
        self.layer: Dict[str, str] = layer
        self.data: Dict[str, str] = data
        self.tilesets: Dict[int, Tileset] = tilesets
        
        self.identifier: str = self.data['__identifier']
        self.iid: str = self.data['iid']
        self.defUid: int = self.data['defUid'] # The UID of the entity definition
        defs = self.layer.level.defs['entities']
        self.defData: Dict = defs[[i['identifier'] for i in defs].index(self.identifier)]

        self.render: Literal['Rectangle', 'Ellipse', 'Cross', 'Tile'] = self.defData['renderMode']
        self.tileRender: Literal['FitInside', 'FullSizeUncropped'] = self.defData['tileRenderMode'] # TODO: Add rest of options

        self.UItileData: Dict = self.data['__tile']
        self.tileData: Dict = self.defData['tileRect']
        self.fieldInstances: List[Dict] = self.data['fieldInstances']
        self.layerId: str = self.layer.identifier

        self.width: int = self.data['width']
        self.height: int = self.data['height']
        
        self.gridSze: int = self.layer.gridSize
        self.layerOffset: List[int] = self.layer.pxOffset
        self.pivot: List[float] = self.data['__pivot']
        #piv = (self.pivot[0] * self.width, self.pivot[1] * self.height)
        self.ScaledPos: List[float] = [
            self.data['px'][0] + self.layerOffset[0]-self.pivot[0]*self.width, 
            self.data['px'][1] + self.layerOffset[1]-self.pivot[1]*self.height
        ]
        self.UnscaledPos: List[float] = [
            self.data['px'][0] / self.gridSze,
            self.data['px'][1] / self.gridSze
        ]
        # self.ScaledPos = [
        #     self.data['px'][0] + self.layerOffset[0],# + piv[0]*self.width,
        #     self.data['px'][1] + self.layerOffset[1]# + piv[1]*self.height
        # ]
        # self.UnscaledPos = [
        #     self.data['px'][0] / self.gridSze,# + piv[0]*self.gridSze,
        #     self.data['px'][1] / self.gridSze# + piv[1]*self.gridSze
        # ]
    
    def scale_pos(self, pos: Iterable[int|float]) -> Tuple[int|float]:
        """
        Scale a position by the grid size, adding the layer offset to it too.

        Args:
            pos (Iterable[Number]): The position to scale.

        Returns:
            Tuple[Number]: The new scaled position.
        """
        return (
            pos[0] * self.gridSze + self.layerOffset[0],# - self.pivot[0] * self.width,
            pos[1] * self.gridSze + self.layerOffset[1]# - self.pivot[1] * self.height
        )

    def unscale_pos(self, pos: Iterable[int|float]) -> Tuple[int|float]:
        """
        Unscale the position by dividing it by the gridsize and removing the layer offset.

        Args:
            pos (Iterable[Number]): The position to unscale.

        Returns:
            Tuple[Number]: The unscaled position.
        """
        return (
            (pos[0] - self.layerOffset[0]) / self.gridSze,# + self.pivot[0] * self.width,
            (pos[1] - self.layerOffset[1]) / self.gridSze# + self.pivot[1] * self.height
        )
    
    def get_tile(self, ui: bool = False) -> pygame.Surface:
        """
        Get the tile image of this entity.

        Args:
            ui (bool, optional): Whether to get the tile as viewed in the sidebar (the UI) or as viewed in the level. Defaults to False (level).

        Returns:
            pygame.Surface: The surface containing the image of the tile.
        """
        data = self.UItileData if ui else self.tileData
        if not data:
            return pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        outsur = self.tilesets[data['tilesetUid']].subsurface(data['x'], 
                                                              data['y'], 
                                                              data['w'], 
                                                              data['h'])
        if not ui:
            if self.tileRender == 'FitInside':
                newsur = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                s = outsur.get_size()
                if max(s) == s[0]:
                    newsur.blit(pygame.transform.scale(outsur, (self.width, int(self.height * s[1] / s[0]))), (0, (self.height - int(self.height * s[1] / s[0])) // 2))
                else:
                    newsur.blit(pygame.transform.scale(outsur, (int(self.width * s[0] / s[1]), self.height)), ((self.width - int(self.width * s[0] / s[1])) // 2, 0))
                outsur = newsur
        
        return outsur

class Ldtklevel:
    def __init__(self, data: Dict, tilesets: Dict[int, Tileset], defs: Dict, fileloc: str):
        """
        An LDtk Level object which contains multiple layers.

        Args:
            data (Dict): The data that has info about the layer in it.
            tilesets (Dict[int, Tileset]): All the tilesets.
            defs (Dict): The defs from the main LDtk file.
            fileloc (str): The location of the LDtk file.
        """
        self.defs: Dict = defs
        self.data: Dict = data
        self.tilesets: Dict[int, Tileset] = tilesets
        self.fileLoc: str = fileloc
        
        self.identifier: str = self.data['identifier']
        self.iid: str = self.data['iid']
        self.uid: int = self.data['uid']
        self.worldPos: List[int] = [self.data['worldX'], self.data['worldY'], self.data['worldDepth']]
        self.bgColour: str = self.data['bgColor'] or self.data['__bgColor']
        self.bgPic: pygame.Surface|None = None
        if self.data['bgRelPath'] is not None:
            self.bgPic = pygame.image.load(os.path.abspath(os.path.join(fileloc,'../',self.data['bgRelPath'])))
        self.fieldInstances: List[Dict] = self.data['fieldInstances'] # The specific level flags
        self.sizePx: List[int] = [self.data['pxWid'], self.data['pxHei']]
        self.neighbours: List[Dict] = self.data['__neighbours']

        self.getCache: List[Dict] = [{}, {}, {}]
        
        # ids = [i['identifier'] for i in defs['layers']]
        
        self.entities: List[Entity] = []
        self.layers: List[layer] = []
        for lay in self.data['layerInstances']:
            if lay['__type'] == 'Entities':
                layobj = layer(lay, self)
                self.entities.extend([Entity(layobj, i, self.tilesets) for i in lay['entityInstances']])
            else:
                self.layers.append(layer(lay, self))
        self.layers.reverse()
    
    def Render(self, transparent_bg=False):
        end = pygame.Surface(self.sizePx, pygame.SRCALPHA)
        if transparent_bg:
            end.fill((0, 0, 0, 0))
        else:
            bg = self.bgPic
            if bg is not None:
                sf = max(self.sizePx[0] / bg.get_width(), self.sizePx[1] / bg.get_height())
                end.blit(pygame.transform.scale(bg, (int(bg.get_width() * sf), int(bg.get_height() * sf))), (0, 0))
            else:
                end.fill(self.bgColour)
        for i in self.layers:
            end.blit(i.getImg(), (0, 0))
        return end
    
    def CollisionLayer(self, collisionFunc: Callable[[Tileset], pygame.Surface]) -> 'Ldtklevel':
        """
        Copy this level but with a collision tileset.

        Args:
            collisionFunc (Callable[[Tileset, int, int], pygame.Surface]): The function that will be used to generate the collision data.
            This function should take in a tileset and the x and y position of the tile, and return a pygame.Surface where transparency is no collisions.
        
        Returns:
            Ldtklevel: The new level with the collision data.
        """
        newLevel = Ldtklevel(self.data, self.tilesets, self.defs, self.fileLoc)
        for i in range(len(newLevel.layers)):
            newLevel.layers[i] = newLevel.layers[i].CollisionLayer(collisionFunc)
        return newLevel
    
    def GetLayerById(self, layerid: str) -> 'layer':
        """
        Get a layer by it's identifier.

        Args:
            layerid (str): The layer identifier.

        Returns:
            layer: The layer object.
        """
        for i in self.layers:
            if i.identifier == layerid:
                return i
        raise ValueError(f"Layer with identifier {layerid} not found.")
    
    def GetAllEntities(self, processor: Callable = lambda e: e) -> List[Any]:
        """
        Get all the entities in the level. Does not use caching, unlike the other get entities functions.

        Args:
            processor (Callable, optional): This is a function that will process the entities. It takes in an Entity object and outputs anything. \
The outputs will be combined as the return list. This defaults to `lambda e: e`. Returning None in this will ignore that entity.
        
        Returns:
            List[Any]: All the entities in the level, passed through the `processor` func.
        """
        o = []
        for e in self.entities:
            resp = processor(e)
            if resp is not None:
                o.append(resp)
        return o

    def GetEntitiesByLayer(self, layerid: str, processor: Callable = lambda e: e, forceRefreshCache: bool = False) -> List[Any]:
        """
        Gets all the entities by their layer identifier. It also caches the results, so if you change the processor you will need to forceRefreshCache.

        Args:
            layerid (str): The layer identifier to get the entities from
            processor (Callable, optional): This is a function that will process the entities. It takes in an Entity object and outputs anything. \
The outputs will be combined as the return list. This defaults to `lambda e: e`. Returning None in this will ignore that entity.
            forceRefreshCache (bool, optional): Force rebuild the cache. Defaults to False.

        Returns:
            List[Any]: All the entities under the layer with layer id `layerid`, passed through the `processor` func.
        """
        if layerid not in self.getCache[0] or forceRefreshCache:
            self.getCache[0][layerid] = []
            for e in self.entities:
                if e.layerId == layerid:
                    resp = processor(e)
                    if resp is not None:
                        self.getCache[0][layerid].append(resp)
        return self.getCache[0][layerid]

    def GetEntitiesByID(self, identifier: str, processor: Callable = lambda e: e, forceRefreshCache: bool = False) -> List[Any]:
        """
        Gets all the entities by their identifier. It also caches the results, so if you change the processor you will need to forceRefreshCache.

        Args:
            identifier (str): The identifier that will be searched for within all the entities.
            processor (Callable): This is a function that will process the entities. It takes in an Entity object and outputs anything. \
The outputs will be combined as the return list. This defaults to `lambda e: e`. Returning None in this will ignore that entity.
            forceRefreshCache (bool, optional): Force rebuild the cache. Defaults to False.

        Returns:
            List[Any]: All the entities which have an identifier of `identifier`, passed through the `processor` func.
        """
        if identifier not in self.getCache[1] or forceRefreshCache:
            self.getCache[1][identifier] = []
            for e in self.entities:
                if e.identifier == identifier:
                    resp = processor(e)
                    if resp is not None:
                        self.getCache[1][identifier].append(resp)
        return self.getCache[1][identifier]
    
    def GetEntitiesByUID(self, uid: int, processor: Callable = lambda e: e, forceRefreshCache: bool = False) -> List[Any]:
        """
        Gets all the entities by their UID. It also caches the results, so if you change the processor you will need to forceRefreshCache.

        Args:
            uid (int): The UID that will be searched for within all the entities.
            processor (Callable): This is a function that will process the entities. It takes in an Entity object and outputs anything. \
The outputs will be combined as the return list. This defaults to `lambda e: e`. Returning None in this will ignore that entity.
            forceRefreshCache (bool, optional): Force rebuild the cache. Defaults to False.
        
        Returns:
            List[Any]: All the entities which have a UID of `uid`, passed through the `processor` func.
        """
        if uid not in self.getCache[1] or forceRefreshCache:
            self.getCache[1][uid] = []
            for e in self.entities:
                if e.defUid == uid:
                    resp = processor(e)
                    if resp is not None:
                        self.getCache[1][uid].append(resp)
        return self.getCache[1][uid]

class layer:
    def __init__(self, data: Dict, level: Ldtklevel):
        """
        A specific Layer.

        Args:
            data (Dict): The data.
            level (Ldtklevel): The parent level.
        """
        self.data: Dict = data
        self.level: Ldtklevel = level
        self.layerDef: Dict = level.defs['layers'][[i['uid'] for i in level.defs['layers']].index(self.data['layerDefUid'])]
        self.tilesets: Dict[int, Tileset] = level.tilesets

        self.identifier: str = self.data['__identifier']
        self.iid: str = self.data['iid']
        self.defUid: int = self.data['layerDefUid']
        self.type: str = self.data['__type']
        self.gridSize: int = self.data['__gridSize']
        self.sizeCells: List[int] = [self.data['__cWid'], self.data['__cHei']]
        self.sizePx: List[int] = [self.sizeCells[0] * self.gridSize, self.sizeCells[1] * self.gridSize]
        self.opacity: float = self.data['__opacity']
        self.visible: bool = self.data['visible']
        self.pxOffset: List[int] = [self.data['__pxTotalOffsetX'], self.data['__pxTotalOffsetY']]
        self.intGridValues: List[Dict] = self.layerDef['intGridValues']
        # TODO: if self.layerDef['parallaxScaling']
        self.tileset: Tileset|None = None
        if self.data['__tilesetDefUid'] is not None:
            self.tileset = self.tilesets[self.data['__tilesetDefUid']]

        self.tiles: List[tile]|None = None
        self.intgrid: IntGridCSV = IntGridCSV(self.data['intGridCsv'], *self.sizeCells, self.pxOffset, self.gridSize)
        
        if self.type == "Tiles":
            self.loadTileSheet()

    def loadTileSheet(self) -> None:
        """
        Load the tilesheet of the layer.
        """
        if self.data['gridTiles'] == []:
            self.tiles = [tile(t, self) for t in self.data['autoLayerTiles']]
        else:
            self.tiles = [tile(t, self) for t in self.data['gridTiles']]
    
    def getTileRects(self) -> colls.Shapes:
        """
        Gets all the tiles (if there are any) as collisions.Rect objects.

        Returns:
            colls.Shapes: The list of all the tiles as collisions.Rect objects.
        """
        if self.tiles is None:
            self.loadTileSheet()
        if self.tiles is None:
            return colls.Shapes()
        return colls.Shapes(*[colls.Rect(i.pos[0], i.pos[1], self.gridSize, self.gridSize) for i in self.tiles])
    
    def getImg(self) -> pygame.Surface:
        """
        Gets the whole layer as a pygame surface.

        Returns:
            pygame.Surface: The layer (be it intgrid or tile) compiled as a pygame surface with transparency.
        """
        end = pygame.Surface(self.sizePx, pygame.SRCALPHA)
        end.fill((255, 255, 255, 0))
        if not self.data['visible']:
            return end
        # TODO: Autotile layer support, but does it even need it???
        if self.tileset is None:
            if self.type == 'IntGrid':
                vals = [i['value'] for i in self.intGridValues]
                for y in range(len(self.intgrid)):
                    for x in range(len(self.intgrid[y])):
                        col = pygame.Surface((self.gridSize, self.gridSize)).convert_alpha()
                        if self.intgrid[y, x] == 0 or self.intgrid[y, x] not in vals:
                            col.fill((255, 255, 255, 0))
                        else:
                            h = self.intGridValues[vals.index(self.intgrid[y, x])]['color'].lstrip('#')
                            col.fill(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
                        end.blit(col, (x*self.gridSize, y*self.gridSize))
            elif self.type == 'Tiles':
                noneTile = pygame.Surface((self.gridSize, self.gridSize))
                noneTile.fill((0, 0, 0))
                for i in self.tiles:
                    end.blit(noneTile, i.pos)
            return end
        if self.tiles is None:
            self.loadTileSheet()
        for i in self.tiles:
            t = self.tileset.getTile(i)
            end.blit(t, self.add_offset(i.pos, t.get_size()))
        return end
    
    def CollisionLayer(self, collisionFunc: Callable[[Tileset, int, int], pygame.Surface]) -> 'layer':
        """
        Copy this layer but with a collision tileset.

        Args:
            collisionFunc (Callable[[Tileset, int, int], pygame.Surface]): The function that will be used to generate the collision data.
            This function should take in a tileset and the x and y position of the tile, and return a pygame.Surface where transparency is no collisions.
        
        Returns:
            layer: The new layer with the collision data.
        """
        newLayer = layer(self.data, self.level)
        tset = Tileset(newLayer.tileset.fileLoc, newLayer.tileset.data)
        newSur = pygame.Surface(tset.tileSet.get_size(), pygame.SRCALPHA)
        for x in range(0, tset.width*tset.tileGridSize, tset.tileGridSize):
            for y in range(0, tset.width*tset.tileGridSize, tset.tileGridSize):
                newSur.blit(collisionFunc(tset, x, y), (x, y))
        tset.tileSet = newSur
        newLayer.tileset = tset
        return newLayer
    
    def add_offset(self, pos: Iterable[int|float], sze: Iterable[int|float]) -> Tuple[int|float]:
        """
        Adds an offset based off of the tile pivot to the position to become correct.

        Args:
            pos (Iterable[Number]): The position to offset
            sze (Iterable[Number]): The size of the rect to offset

        Returns:
            Tuple[Number]: The offset position
        """
        return (pos[0] + self.pxOffset[0]-self.layerDef['tilePivotX']*sze[0]+self.gridSize*self.layerDef['tilePivotX'], 
                pos[1] + self.pxOffset[1]-self.layerDef['tilePivotY']*sze[1]+self.gridSize*self.layerDef['tilePivotY'])

class IntGridCSV:
    def __init__(self, intgrid: List[int], cwid: int, chei: int = None, offsets: List[int|float] = [0, 0], gridsize: int = 1):
        """
        An Intgrid parser.

        Args:
            intgrid (List[int]): The input intgrid.
            cwid (int): The width of the intgrid.
            chei (int, optional): The height of the intgrid. Defaults to auto find.
            offsets (List[int | float], optional): The offset of the rects. Defaults to [0, 0].
            gridsize (int, optional): The pixel size of one cell. Defaults to 1. Please fill this in.
        """
        self.rawintgrid: List[int] = intgrid
        self.cwid: int = cwid
        self.chei: int = chei or ceil(len(intgrid) / self.cwid)
        self.offsets: List[int|float] = offsets
        self.gridsze: int = gridsize
        self.intgrid: List[List[int]] = [intgrid[cwid*i:cwid*(i+1)] for i in range(chei)]
        self.allValues: List[int] = list(set(intgrid))
        self.rects: Dict[int, colls.Rect] = None
    
    def getRects(self, matches: List[int]) -> colls.Shapes:
        """
        Gets all the cells of types `matches`. Will cache all possible options the first time it's run, so expect slightly longer times then.

        Args:
            matches (List[int]): The different intgrid values to output.

        Returns:
            colls.Shapes: A Shapes object containing all the output shapes.
        """
        if isinstance(matches, int):
            matches = [matches]
        if self.rects is not None:
            li = []
            for i in self.rects:
                if i in matches:
                    li.extend(self.rects[i])
            return colls.Shapes(*li)
        rs = {}
        typ = None
        for y in range(len(self.intgrid)):
            for x in range(len(self.intgrid[y])):
                typ = self.intgrid[y][x]
                if typ in rs:
                    rs[typ].append(colls.Rect(x*self.gridsze+self.offsets[0], y*self.gridsze+self.offsets[1], self.gridsze, self.gridsze))
                else:
                    rs[typ] = [colls.Rect(x*self.gridsze, y*self.gridsze, self.gridsze, self.gridsze)]
        for i in rs:
            rs[i] = colls.ShapeCombiner.combineRects(*rs[i])
        self.rects = rs
        return self.getRects(matches)
    
    def __iter__(self):
        return iter(self.intgrid)
    
    def __len__(self):
        return len(self.intgrid)

    def __getitem__(self, args) -> List[int] | int:
        if isinstance(args, int):
            return self.intgrid[args]
        y, x = args[0], (None if len(args) < 2 else args[1])
        if y is None:
            return self.intgrid[y]
        return self.intgrid[y][x]

class tile:
    def __init__(self, data: Dict, lay: layer):
        """
        A single tile from a tile layer.

        Args:
            data (Dict): This tile's data.
            layer (layer): The parent layer.
        """
        self.data: Dict = data
        self.layer: layer = lay

        self.px: List[int] = self.data['px']
        self.src: List[int] = self.data['src']
        self.t = self.data['t']
        self.a: float = self.data['a']
        # what is self.data['d']???

        self.pos: Tuple[int] = (self.px[0] + self.layer.pxOffset[0], self.px[1] + self.layer.pxOffset[1])
        # self.src = self.src
        
        self.flip: Tuple[int] = (self.data['f'] in [1, 3], self.data['f'] in [2, 3])
        
        # THINGS TO KNOW:
        # self.data['f'] = flip: 0=no flip, 1=flip x, 2=flip y, 3=flip both
        # self.src = position of the tile IN THE TILESET
        # self.a = alpha (opacity) of the tile (1=full,0=invisible)
        # self.px = coordinates of the tile IN THE LAYER. Don't forget layer offsets, if they exist!
        # self.pos = coordinates of the tile IN THE LAYER,with offsets!
    
    def getImg(self) -> pygame.Surface:
        """
        Gets this tile's image.
        """
        return self.layer.tileset.getTile(self)
