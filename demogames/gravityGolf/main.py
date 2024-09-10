from BlazeSudio.Game import Game
from BlazeSudio.collisions import collisions
import BlazeSudio.Game.statics as Ss
import pygame, math

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/levels.ldtk")
# TODO: A more uniform way to access things (e.g. the current level)

class BaseEntity(Ss.BaseEntity):
    def __init__(self):
        super().__init__()
        self.accel_amnt = [[5, 5], [0.5, 0.5]]
        self.max_accel = [15, 15]
    
    def __call__(self, keys):
        objs = collisions.Shapes(*G.currentScene.GetEntities('GravityFields'))
        thisObj = collisions.Point(self.pos[0]*G.currentLvL.layerInstances[0]['__cWid'], self.pos[1]*G.currentLvL.layerInstances[0]['__cHei'])
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
        outRect, self.accel = thisObj.handleCollisionsAccel(self.accel, G.currentScene.GetEntities('Collisions'), False)
        self.pos = [outRect[0]/G.currentLvL.layerInstances[0]['__cWid'], outRect[1]/G.currentLvL.layerInstances[0]['__cHei']]

@G.DefaultSceneLoader
class MainGameScene(Ss.BaseScene):
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.colls = {}
        self.last_playerPos = [0, 0]
        self.entities.append(BaseEntity()) # The Player
        for e in self.currentLvl.entities:
            if e['defUid'] == 7:
                self.entities[0].pos = [e['px'][0] / e['width'], e['px'][1] / e['height']]
                break
    
    def tick(self, keys):
        super().tick(keys)
        if pygame.mouse.get_pressed()[0]:
            angle = math.atan2(self.last_playerPos[1]-pygame.mouse.get_pos()[1], self.last_playerPos[0]-pygame.mouse.get_pos()[0])
            addAccel = [-10*math.cos(angle), -10*math.sin(angle)]
            self.entities[0].accel[0] += addAccel[0]
            self.entities[0].accel[1] += addAccel[1]
    
    def GetEntities(self, typ):
        if typ not in self.colls:
            self.colls[typ] = []
            for e in self.currentLvl.entities:
                if e['layerId'] == typ:
                    if e['__identifier'] == 'CircleRegion':
                        self.colls[typ].append(collisions.Circle(e['__worldX']+e['width']//2, e['__worldY']+e['height']//2, e['width'])) # TODO: Elipses
                    elif e['__identifier'] == 'RectRegion':
                        self.colls[typ].append(collisions.Rect(e['__worldX'], e['__worldY'], e['width'], e['height']))
        return self.colls[typ]
    
    def CamPos(self):
        return self.entities[0].pos
    
    def CamDist(self):
        return 8
    
    def CamBounds(self):
        return [None, None, None, None]

    def render(self):
        lvl = self.currentLvl
        sur = pygame.Surface((lvl.pxWid, lvl.pxHei))
        for e in lvl.entities:
            typs = ['Collisions', 'GravityFields']
            col = (255, 255, 255) if e['layerId'] not in typs else [(255, 50, 50), (10, 255, 50)][typs.index(e['layerId'])]
            if e['__identifier'] == 'CircleRegion':
                pygame.draw.circle(sur, col, (e['__worldX']+e['width']//2, e['__worldY']+e['height']//2), e['width']) # TODO: Elipses
            elif e['__identifier'] == 'RectRegion':
                pygame.draw.rect(sur, col, (e['__worldX'], e['__worldY'], e['width'], e['height']))
        return sur
    
    def renderUI(self, win, offset, midp, scale):
        pygame.draw.circle(win, (0, 0, 0), (midp[0]-offset[0], midp[1]-offset[1]), 10)
        pygame.draw.circle(win, (255, 255, 255), (midp[0]-offset[0], midp[1]-offset[1]), 10, 2)
        angle = math.atan2(self.last_playerPos[1]-pygame.mouse.get_pos()[1], self.last_playerPos[0]-pygame.mouse.get_pos()[0])
        addPos = [-200*math.cos(angle), -200*math.sin(angle)]
        pygame.draw.line(win, (255, 155, 155), (midp[0]-offset[0], midp[1]-offset[1]), 
                         (midp[0]-offset[0]+addPos[0], midp[1]-offset[1]+addPos[1]), 5)
        self.last_playerPos = (midp[0]-offset[0], midp[1]-offset[1])

G.load_scene(None)

G.play(debug=True)
