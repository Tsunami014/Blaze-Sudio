from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss
from BlazeSudio.graphics import options as GO
import pygame, math

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/levels.ldtk")
# TODO: A more uniform way to access things (e.g. the current level)

class DebugCommands:
    def __init__(self):
        G.AddCommand('/load', 'Load any level', lambda x: G.load_scene(lvl=int(x[0])))
        G.AddCommand('/next', 'Load the next level', lambda: G.load_scene(lvl=G.currentScene.lvl+1))
        G.AddCommand('/prev', 'Load the previous level', lambda: G.load_scene(lvl=G.currentScene.lvl-1))
        G.AddCommand('/splash', 'Go back to the splash screen', lambda: G.load_scene(SplashScreen))
        G.AddCommand('/reload', 'Reload the current level', lambda: G.load_scene(lvl=G.currentScene.lvl))
        self.dotCollisionDebug = False
        G.AddCommand('/dot', 'Toggle dot collision debug', self.toggleDot)
    
    def toggleDot(self):
        self.dotCollisionDebug = not self.dotCollisionDebug
        G.G.Toast('Dot collision toggled to ' + ('enabled' if self.dotCollisionDebug else 'disabled'))

debug = DebugCommands()

class PlayerEntity(Ss.BaseEntity):
    def __init__(self):
        super().__init__()
        self.collided = False
        self.accel_amnt = [[5, 5], [0.5, 0.5]]
        self.max_accel = [60, 60]
    
    def __call__(self, keys):
        objs = collisions.Shapes(*G.currentScene.GetEntitiesByLayer('GravityFields'))
        oldPos = (self.pos[0]*G.currentLvL.layerInstances[0]['__gridSize'], self.pos[1]*G.currentLvL.layerInstances[0]['__gridSize'])
        thisObj = collisions.Point(*oldPos)
        cpoints = objs.closestPointTo(thisObj) # [(i, i.closestPointTo(curObj)) for i in objs]
        if cpoints:
            cpoints.sort(key=lambda x: (thisObj.x-x[0])**2+(thisObj.y-x[1])**2)
            # Find the point on the unit circle * 0.2 that is closest to the object
            closest = cpoints[0]
            angle = math.atan2(thisObj.y-closest[1], thisObj.x-closest[0])
            gravity = [-math.cos(angle), -math.sin(angle)]
        else:
            gravity = [0, 0]
        self.gravity = gravity
        self.handle_accel()
        oldaccel = self.accel
        outRect, self.accel = thisObj.handleCollisionsAccel(self.accel, G.currentScene.GetEntitiesByLayer('Collisions'), False)
        if collisions.Line(oldPos, outRect).collides(collisions.Shapes(*G.currentScene.GetEntitiesByID('Goal'))):
            if G.currentScene.lvl+1 >= len(G.world.ldtk.levels):
                G.load_scene(SplashScreen)
            else:
                G.load_scene(lvl=G.currentScene.lvl+1)
            return
        self.collided = oldaccel != self.accel
        if self.collided and debug.dotCollisionDebug:
            pygame.draw.circle(G.currentScene.sur, (255, 0, 0), 
                               (int(outRect[0]), int(outRect[1])), 5)
        self.pos = [outRect[0]/G.currentLvL.layerInstances[0]['__gridSize'], outRect[1]/G.currentLvL.layerInstances[0]['__gridSize']]

class SplashScreen(Ss.BaseScene):
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.rendered = False
    def render(self):
        if not self.rendered:
            G.G.WIN.fill((0, 0, 0))
            G.G.add_empty_space(GO.PCTOP, 0, 30)
            G.G.add_text('Gravity golf!', (255, 255, 255), GO.PCTOP, GO.FTITLE)
            G.G.add_button('Play!!!', GO.CGREEN, GO.PCCENTER, callback=lambda x: self.Game.load_scene())
            self.rendered = True
        return pygame.Surface((0, 0))

@G.DefaultSceneLoader
class MainGameScene(Ss.BaseScene):
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.lvl = settings.get('lvl', 0)
        self.colls = [{}, {}]
        self.sur = None
        self.last_playerPos = [0, 0]
        self.entities.append(PlayerEntity()) # The Player
        for e in self.currentLvl.entities:
            if e.defUid == 7:
                self.entities[0].pos = [e.UnscaledPos[0]+0.5, e.UnscaledPos[1]+0.5]
                break
    
    def tick(self, keys):
        super().tick(keys)
        if pygame.mouse.get_pressed()[0] and self.entities[0].collided:
            angle = math.atan2(self.last_playerPos[1]-pygame.mouse.get_pos()[1], self.last_playerPos[0]-pygame.mouse.get_pos()[0])
            addAccel = [-40*math.cos(angle), -40*math.sin(angle)]
            self.entities[0].accel[0] += addAccel[0]
            self.entities[0].accel[1] += addAccel[1]
    
    def GetEntitiesByLayer(self, typ):
        if typ not in self.colls[0]:
            self.colls[0][typ] = []
            for e in self.currentLvl.entities:
                if e.layerId == typ:
                    if e._identifier == 'CircleRegion':
                        self.colls[0][typ].append(collisions.Circle(e.ScaledPos[0], e.ScaledPos[1], e.width/2))
                    elif e._identifier == 'RectRegion':
                        self.colls[0][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
                    elif e._identifier == 'Goal':
                        self.colls[0][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
        return self.colls[0][typ]

    def GetEntitiesByID(self, typ):
        if typ not in self.colls[1]:
            self.colls[1][typ] = []
            for e in self.currentLvl.entities:
                if e._identifier == typ:
                    if e._identifier == 'CircleRegion':
                        self.colls[1][typ].append(collisions.Circle(e.ScaledPos[0], e.ScaledPos[1], e.width/2))
                    elif e._identifier == 'RectRegion':
                        self.colls[1][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
                    elif e._identifier == 'Goal':
                        self.colls[1][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
        return self.colls[1][typ]
    
    def CamPos(self):
        return self.entities[0].pos
    
    def CamDist(self):
        return 2
    
    def CamBounds(self):
        return [None, None, None, None]

    def render(self):
        if self.sur is not None:
            return self.sur
        lvl = self.currentLvl
        sur = pygame.Surface((lvl.pxWid, lvl.pxHei))
        for e in lvl.entities:
            typs = ['Collisions', 'GravityFields']
            col = (255, 255, 255) if e.layerId not in typs else [(255, 50, 50), (10, 255, 50)][typs.index(e.layerId)]
            if e._identifier == 'CircleRegion':
                pygame.draw.circle(sur, col, (e.ScaledPos[0], e.ScaledPos[1]), e.width//2)
            elif e._identifier == 'RectRegion':
                pygame.draw.rect(sur, col, (*e.ScaledPos, e.width, e.height))
            elif e._identifier == 'Goal':
                # The star shape was made by me which is why it probably doesn't look very good
                pygame.draw.polygon(sur, col, [(e.ScaledPos[0]+i[0]*e.width, e.ScaledPos[1]+i[1]*e.height) for i in 
                                               [(0, 0), (0.5, 0.23), (1, 0), (0.7, 0.35), 
                                                (1, 0.5), (0.6, 0.6), (0.5, 1), (0.4, 0.6), 
                                                (0, 0.5), (0.3, 0.35)]])
        self.sur = sur
        return self.sur
    
    def renderUI(self, win, offset, midp, scale):
        pygame.draw.circle(win, (0, 0, 0), (midp[0]-offset[0], midp[1]-offset[1]), 10)
        pygame.draw.circle(win, (255, 255, 255), (midp[0]-offset[0], midp[1]-offset[1]), 10, 2)
        if self.entities[0].collided:
            angle = math.atan2(self.last_playerPos[1]-pygame.mouse.get_pos()[1], self.last_playerPos[0]-pygame.mouse.get_pos()[0])
            addPos = [-200*math.cos(angle), -200*math.sin(angle)]
            pygame.draw.line(win, (255, 155, 155), (midp[0]-offset[0], midp[1]-offset[1]), 
                            (midp[0]-offset[0]+addPos[0], midp[1]-offset[1]+addPos[1]), 5)
        self.last_playerPos = (midp[0]-offset[0], midp[1]-offset[1])

G.load_scene(SplashScreen)

G.play(debug=True)
