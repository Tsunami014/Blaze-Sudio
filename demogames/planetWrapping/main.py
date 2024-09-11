from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss
import pygame, math

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/main.ldtk")

class BaseEntity(Ss.BaseEntity):
    def __call__(self, evs):
        objs = collisions.Shapes(*G.currentScene.GetEntitiesByLayer('GravityFields'))
        oldPos = (self.pos[0]*G.currentLvL.layerInstances[0]['__gridSize'], self.pos[1]*G.currentLvL.layerInstances[0]['__gridSize'])
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
        colls = G.currentScene.GetEntitiesByLayer('Entities')
        for i in colls:
            i.bounciness = 1
        outRect, self.accel = thisObj.handleCollisionsAccel(self.accel, colls, False)
        self.pos = [outRect[0]/G.currentLvL.layerInstances[0]['__gridSize'], outRect[1]/G.currentLvL.layerInstances[0]['__gridSize']]

@G.DefaultSceneLoader
class MainGameScene(Ss.BaseScene):
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.colls = [{}, {}]
        self.sur = None
        self.entities.append(BaseEntity()) # The Player
        for e in self.currentLvl.entities:
            if e.defUid == 6:
                self.entities[0].pos = [e.UnscaledPos[0]+0.5, e.UnscaledPos[1]+0.5]
                break
    
    def GetEntitiesByLayer(self, typ):
        if typ not in self.colls[0]:
            self.colls[0][typ] = []
            for e in self.currentLvl.entities:
                if e.layerId == typ:
                    if e._identifier == 'CircleRegion':
                        self.colls[0][typ].append(collisions.Circle(e.ScaledPos[0]+e.width/2, e.ScaledPos[1]+e.height/2, e.width/2))
                    elif e._identifier == 'RectRegion':
                        self.colls[0][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
        return self.colls[0][typ]

    def GetEntitiesByID(self, typ):
        if typ not in self.colls[1]:
            self.colls[1][typ] = []
            for e in self.currentLvl.entities:
                if e._identifier == typ:
                    if e._identifier == 'CircleRegion':
                        self.colls[1][typ].append(collisions.Circle(e.ScaledPos[0]+e.width/2, e.ScaledPos[1]+e.height/2, e.width/2))
                    elif e._identifier == 'RectRegion':
                        self.colls[1][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
        return self.colls[1][typ]
    
    def CamPos(self):
        return self.entities[0].pos
    
    def CamDist(self):
        return 4
    
    def CamBounds(self):
        return [None, None, None, None]

    def render(self):
        if self.sur is not None:
            return self.sur
        @self.Game.G.Loading
        def LS(slf):
            self.sur = self.Game.world.get_pygame(self.lvl)
        fin, _ = LS()
        if not fin:
            self.Game.G.Abort()
        return self.sur
    
    def renderUI(self, win, offset, midp, scale):
        pygame.draw.circle(win, (0, 0, 0), (midp[0]-offset[0], midp[1]-offset[1]), 10)
        pygame.draw.circle(win, (255, 255, 255), (midp[0]-offset[0], midp[1]-offset[1]), 10, 2)

G.load_scene()

G.play(debug=True)
