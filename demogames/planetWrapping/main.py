from BlazeSudio import ldtk
from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss
from demogames.planetWrapping.planetCollisions import approximate_polygon
import pygame, math

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/main.ldtk")

class DebugCommands:
    def __init__(self):
        self.showingColls = False
        G.AddCommand('/colls', 'Toggle collision debug', self.toggleColls)
    
    def toggleColls(self):
        self.showingColls = not self.showingColls
        G.G.Toast(('Showing' if self.showingColls else 'Not showing') + ' collisions')

debug = DebugCommands()

class BaseEntity(Ss.BaseEntity):
    def __call__(self, evs):
        objs = collisions.Shapes(*G.currentScene.GetCollEntitiesByLayer('GravityFields'))
        oldPos = self.scaled_pos
        thisObj = collisions.Point(*oldPos)
        cpoints = [(i.closestPointTo(thisObj), i) for i in objs]
        if cpoints:
            cpoints.sort(key=lambda x: (thisObj.x-x[0][0])**2+(thisObj.y-x[0][1])**2)
            # Find the point on the unit circle * 0.2 that is closest to the object
            closest = cpoints[0][0]
            ydiff, xdiff = thisObj.y-closest[1], thisObj.x-closest[0]
            angle = math.atan2(ydiff, xdiff)
            tan = cpoints[0][1].tangent(closest, [xdiff, ydiff])
            gravity = [-0.2*math.cos(angle), -0.2*math.sin(angle)]
        else:
            gravity = [0, 0]
            tan = 0
        self.gravity = gravity
        prevaccel = self.accel
        self.accel = [0, 0]
        self.handle_keys()
        self.accel = collisions.rotateBy0(self.accel, tan-90)
        self.accel = [self.accel[0]+prevaccel[0], self.accel[1]+prevaccel[1]]
        self.handle_accel()
        colls = G.currentScene.collider()
        outRect, self.accel = thisObj.handleCollisionsAccel(self.accel, colls, False)
        self.pos = self.entity.unscale_pos(outRect)
    
    @property
    def scaled_pos(self):
        return self.entity.scale_pos(self.pos)

@G.DefaultSceneLoader
class MainGameScene(Ss.BaseScene):
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.colls = [{}, {}]
        self.sur = None
        self.showingColls = True
        self._collider = None
        self.CamDist = 4
        self.CamBounds = [None, None, None, None]
        for e in self.currentLvl.entities:
            if e.defUid == 6:
                self.entities.append(BaseEntity(e)) # The Player
                self.entities[0].pos = [e.UnscaledPos[0]+0.5, e.UnscaledPos[1]+0.5]
                break
        if self.entities == []:
            raise Ss.IncorrectLevelError(
                'Need a player start!'
            )
    
    def GetCollEntitiesByLayer(self, typ):
        if typ not in self.colls[0]:
            self.colls[0][typ] = []
            for e in self.currentLvl.entities:
                if e.layerId == typ:
                    if e.identifier == 'CircleRegion':
                        self.colls[0][typ].append(collisions.Circle(*e.ScaledPos, e.width/2))
                    elif e.identifier == 'RectRegion':
                        self.colls[0][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
        return self.colls[0][typ]
    
    @property
    def CamPos(self):
        return self.entities[0].scaled_pos
    
    def collider(self):
        if self._collider is not None:
            return self._collider
        lay = G.currentLvL.layers[1]
        tmpl = ldtk.layer(lay.data, lay.level)
        d = lay.tileset.data.copy()
        d.update({'relPath': d['relPath'] + '/../colls.png'})
        tmpl.tileset = ldtk.Tileset(lay.tileset.fileLoc, d)
        self._collider = collisions.Shapes(approximate_polygon(tmpl.getImg()), *G.currentScene.GetCollEntitiesByLayer('Entities'))
        return self._collider

    def render(self):
        if self.sur is not None and debug.showingColls == self.showingColls:
            return self.sur
        self.showingColls = debug.showingColls
        self.sur = self.Game.world.get_pygame(self.lvl)
        if self.showingColls:
            colls = self.collider()
            pygame.draw.polygon(self.sur, (255, 50, 10), colls[0].toPoints(), 1)
            for s in colls[1:] + self.GetCollEntitiesByLayer('GravityFields'):
                if isinstance(s, collisions.Rect):
                    pygame.draw.rect(self.sur, (255, 10, 50), (s.x, s.y, s.w, s.h), 1)
                elif isinstance(s, collisions.Circle):
                    pygame.draw.circle(self.sur, (10, 50, 255), (s.x, s.y), s.r, 1)
        return self.sur
    
    def renderUI(self, win, offset, midp, scale):
        pygame.draw.circle(win, (0, 0, 0), (midp[0]-offset[0], midp[1]-offset[1]), 10)
        pygame.draw.circle(win, (255, 255, 255), (midp[0]-offset[0], midp[1]-offset[1]), 10, 2)

G.load_scene()

G.play(debug=True)
