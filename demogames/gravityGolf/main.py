from BlazeSudio.Game import Game
from BlazeSudio import collisions
import BlazeSudio.Game.statics as Ss
from BlazeSudio.graphics import options as GO
import pygame

thispth = __file__[:__file__.rindex('/')]

G = Game()
G.load_map(thispth+"/levels.ldtk")
# TODO: A more uniform way to access things (e.g. the current level)

class DebugCommands:
    def __init__(self, Game):
        self.Game = Game
        Game.AddCommand('/load', 'Load any level', lambda x: Game.load_scene(lvl=int(x[0])))
        Game.AddCommand('/next', 'Load the next level', lambda: Game.load_scene(lvl=Game.currentScene.lvl+1))
        Game.AddCommand('/prev', 'Load the previous level', lambda: Game.load_scene(lvl=Game.currentScene.lvl-1))
        Game.AddCommand('/splash', 'Go back to the splash screen', lambda: Game.load_scene(SplashScreen))
        Game.AddCommand('/reload', 'Reload the current level', lambda: Game.load_scene(lvl=Game.currentScene.lvl))
        self.dotCollisionDebug = False
        Game.AddCommand('/dot', 'Toggle dot collision debug', self.toggleDot)
    
    def toggleDot(self):
        self.dotCollisionDebug = not self.dotCollisionDebug
        self.Game.G.Toast('Dot collision toggled to ' + ('enabled' if self.dotCollisionDebug else 'disabled'))

debug = DebugCommands(G)

class PlayerEntity(Ss.BaseEntity):
    def __init__(self, Game, entity):
        super().__init__(Game, entity)
        self.collided = False
        self.accel_amnt = [[5, 5], [0.5, 0.5]]
        self.max_accel = [60, 60]
        self.defcollideDelay = 3
        self.collidingDelay = self.defcollideDelay
        self.defClickDelay = 3
        self.clicked = 0
    
    def __call__(self, keys):
        objs = collisions.Shapes(*self.Game.currentScene.GetEntitiesByLayer('GravityFields'))
        pygame.event.pump()
        oldPos = self.scaled_pos
        thisObj = collisions.Point(*oldPos)
        cpoints = objs.closestPointTo(thisObj) # [(i, i.closestPointTo(curObj)) for i in objs]
        if cpoints:
            cpoints.sort(key=lambda x: (thisObj.x-x[0])**2+(thisObj.y-x[1])**2)
            closest = cpoints[0]
            angle = collisions.direction(closest, thisObj)
            gravity = collisions.pointOnUnitCircle(angle, -1)
        else:
            gravity = [0, 0]
        self.gravity = gravity
        self.handle_accel()
        oldaccel = self.accel
        outRect, self.accel = thisObj.handleCollisionsAccel(self.accel, self.Game.currentScene.GetEntitiesByLayer('Collisions'), False)
        mvementLine = collisions.Line(oldPos, outRect)
        if mvementLine.collides(collisions.Shapes(*self.Game.currentScene.GetEntitiesByID('BlackHole'))):
            self.Game.load_scene(lvl=self.Game.currentScene.lvl)
        if mvementLine.collides(collisions.Shapes(*self.Game.currentScene.GetEntitiesByID('Goal'))):
            if self.Game.currentScene.lvl+1 >= len(self.Game.world.ldtk.levels):
                self.Game.load_scene(SplashScreen)
            else:
                self.Game.load_scene(lvl=self.Game.currentScene.lvl+1)
            return
        newcolliding = oldaccel != self.accel
        if newcolliding != self.collided:
            if self.collidingDelay <= 0:
                self.collided = newcolliding
            else:
                self.collidingDelay -= 1
                if self.collidingDelay <= 0:
                    self.collided = newcolliding
        else:
            if self.collidingDelay >= self.defcollideDelay:
                pass
            else:
                self.collidingDelay += 0.25
        if self.collided and debug.dotCollisionDebug:
            pygame.draw.circle(self.Game.currentScene.sur, (255, 0, 0), 
                               (int(outRect[0]), int(outRect[1])), 5)
        self.pos = self.entity.unscale_pos(outRect)
    
    @property
    def scaled_pos(self):
        return self.entity.scale_pos(self.pos)

class SplashScreen(Ss.SkeletonScene):
    useRenderer = False
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.rendered = False
    def render(self):
        if not self.rendered:
            graphic = self.Game.G
            graphic.bgcol = self.Game.world.get_level(0).bgColour
            graphic.add_empty_space(GO.PCTOP, 0, 30)
            graphic.add_text('Gravity golf!', GO.CWHITE, GO.PCTOP, GO.FTITLE)
            graphic.add_button('Play!!!', GO.CGREEN, GO.PCCENTER, callback=lambda x: self.Game.load_scene())
            self.rendered = True

@G.DefaultSceneLoader
class MainGameScene(Ss.BaseScene):
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.CamDist = 2
        self.CamBounds = [None, None, None, None]
        self.lvl = settings.get('lvl', 0)
        self.colls = [{}, {}]
        self.sur = None
        self.last_playerPos = [0, 0]
        for e in self.currentLvl.entities:
            if e.defUid == 7:
                self.entities.append(PlayerEntity(Game, e)) # The Player
                self.entities[0].pos = [e.UnscaledPos[0]+0.5, e.UnscaledPos[1]+0.5]
                break
        if self.entities == []:
            raise Ss.IncorrectLevelError(
                'Need a player start!'
            )
    
    def tick(self, evs):
        super().tick(evs)
        playere = self.entities[0]
        didClick = any(e.type == pygame.MOUSEBUTTONDOWN for e in evs)
        if didClick or playere.clicked > 0:
            if playere.collided:
                playere.collidingDelay = playere.defcollideDelay
                playere.collided = False
                angle = collisions.direction(pygame.mouse.get_pos(), self.last_playerPos)
                addPos = collisions.pointOnUnitCircle(angle, -40)
                def sign(x):
                    if x > 0:
                        return 1
                    if x < 0:
                        return -1
                    return 0
                addAccel = [min(abs(addPos[0]), abs(self.last_playerPos[0]-pygame.mouse.get_pos()[0])/4)*sign(addPos[0]),
                            min(abs(addPos[1]), abs(self.last_playerPos[1]-pygame.mouse.get_pos()[1])/4)*sign(addPos[1])]
                playere.accel[0] += addAccel[0]
                playere.accel[1] += addAccel[1]
            else:
                if didClick:
                    playere.clicked = playere.defClickDelay
                else:
                    playere.clicked -= 1
    
    def GetEntitiesByLayer(self, typ): # TODO: Move into pyLDtk
        if typ not in self.colls[0]:
            self.colls[0][typ] = []
            for e in self.currentLvl.entities:
                if e.layerId == typ:
                    if e.identifier == 'CircleRegion' or e.identifier == 'BlackHole':
                        self.colls[0][typ].append(collisions.Circle(e.ScaledPos[0], e.ScaledPos[1], e.width/2))
                    elif e.identifier == 'RectRegion':
                        self.colls[0][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
                    elif e.identifier == 'Goal':
                        self.colls[0][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
        return self.colls[0][typ]

    def GetEntitiesByID(self, typ):
        if typ not in self.colls[1]:
            self.colls[1][typ] = []
            for e in self.currentLvl.entities:
                if e.identifier == typ:
                    if e.identifier == 'CircleRegion' or e.identifier == 'BlackHole':
                        self.colls[1][typ].append(collisions.Circle(e.ScaledPos[0], e.ScaledPos[1], e.width/2))
                    elif e.identifier == 'RectRegion':
                        self.colls[1][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
                    elif e.identifier == 'Goal':
                        self.colls[1][typ].append(collisions.Rect(*e.ScaledPos, e.width, e.height))
        return self.colls[1][typ]
    
    @property
    def CamPos(self):
        return self.entities[0].scaled_pos

    def render(self):
        if self.sur is not None:
            return self.sur
        lvl = self.currentLvl
        sur = pygame.Surface(lvl.sizePx)
        sur.fill(self.Game.currentLvL.bgColour)
        for e in lvl.entities:
            typs = ['Collisions', 'GravityFields']
            col = (255, 255, 255) if e.layerId not in typs else [(255, 50, 50), (10, 50, 50)][typs.index(e.layerId)]
            if e.identifier == 'CircleRegion' or e.identifier == 'BlackHole':
                pygame.draw.circle(sur, col, (e.ScaledPos[0], e.ScaledPos[1]), e.width//2)
            elif e.identifier == 'RectRegion':
                pygame.draw.rect(sur, col, (*e.ScaledPos, e.width, e.height))
            elif e.identifier == 'Goal':
                # The star shape was made by me which is why it probably doesn't look very good
                pygame.draw.polygon(sur, (255, 180, 10), [(e.ScaledPos[0]+i[0]*e.width, e.ScaledPos[1]+(1-i[1])*e.height) for i in 
                                               [(0, 0), (0.5, 0.23), (1, 0), (0.7, 0.35), 
                                                (1, 0.5), (0.6, 0.6), (0.5, 1), (0.4, 0.6), 
                                                (0, 0.5), (0.3, 0.35)]])
        self.sur = sur
        return self.sur
    
    def renderUI(self, win, offset, midp, scale):
        pos = self.entities[0].scaled_pos
        p = (pos[0]*scale+offset[0], pos[1]*scale+offset[1])
        pygame.draw.circle(win, (0, 0, 0), (p[0], p[1]), 10)
        pygame.draw.circle(win, (255, 255, 255), (p[0], p[1]), 10, 2)
        if self.entities[0].collided:
            angle = collisions.direction(pygame.mouse.get_pos(), self.last_playerPos)
            addPos = collisions.pointOnUnitCircle(angle, -200)
            pygame.draw.line(win, (255, 155, 155), (p[0], p[1]), 
                            (p[0]+addPos[0], p[1]+addPos[1]), 5)
        self.last_playerPos = (p[0], p[1])

G.load_scene(SplashScreen)

G.play(debug=True)
