from enum import Enum
import pygame
from BlazeSudio.graphics import options as GO

class Element:
    NEXT_UID = [0]
    type = None
    def __init__(self, G):
        self.G = G
        self.uid = self.NEXT_UID[0]
        self.NEXT_UID[0] += 1
    
    def remove(self):
        self.G.Stuff.remove(self)
    
    # Required subclass functions
    def update(self, mousePos, events):
        pass
    
    def get(self):
        pass
    
    # Utility functions
    def __eq__(self, other):
        return self.uid == other
    
    def __hash__(self):
        return hash(self.uid)
    
    def __str__(self):
        return f'<{self.__class__.__name__}({str(self.get())})>'
    def __repr__(self): return str(self)

class ReturnGroup:
    def __init__(self, *states):
        self.states = list(states)
    
    def append(self, otherState):
        self.states.append(otherState)
    
    def get(self):
        return self.states
    
    def __str__(self):
        return f'<ReturnGroup with states {self.states}>'
    def __repr__(self): return str(self)

class ReturnState(Enum):
    # If nothing happpens, return None as usual
    ABORT = 1
    """Abort the Graphics screen"""
    
    CALL = 2
    """Call the function on this"""
    
    TBUTTON = 3
    """Add this to the touchingButtons list"""
    
    def __add__(self, otherState):
        if not isinstance(otherState, (ReturnState, ReturnGroup)):
            raise TypeError(
                'Invalid type for add: %s! Must be a ReturnState or a ReturnGroup!'%str(type(otherState))
            )
        if isinstance(otherState, ReturnGroup):
            otherState.append(self)
            return otherState
        return ReturnGroup(self, otherState)
    def get(self):
        return [self]

class Switch(Element):
    type = GO.TSWITCH
    def __init__(self, G, x, y, size=20, speed=10, default=False):
        super().__init__(G)
        self.pos = (x, y)
        self.size = size
        self.anim = 0
        self.speed = speed
        self.state = default
        self.rect = pygame.Rect(x, y, size, size)
        self.barrect = pygame.Rect(x+size/4, y, size, size/2)
    
    def update(self, mousePos, events):
        if self.anim < 0: self.anim = 0
        if self.anim > 15*self.speed: self.anim = 15*self.speed
        if self.anim != (0 if not self.state else 15*self.speed):
            if self.state: self.anim += 1
            else: self.anim -= 1
        pygame.draw.rect(self.G.WIN, (125, 125, 125), self.barrect, border_radius=self.size)
        pygame.draw.circle(self.G.WIN, ((0, 255, 0) if self.state else (255, 0, 0)), (self.pos[0]+self.size/4+(self.anim/self.speed)*(self.size/20), self.pos[1]+self.size/4), self.size/2)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.G.pause:
                if event.button == pygame.BUTTON_LEFT:
                    if self.rect.collidepoint(mousePos):
                        self.state = not self.state
                        return ReturnState.CALL
    
    def get(self):
        """Get the state of the switch"""
        return self.state

# InputBoxes code modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame 

class InputBox(Element): # TODO: Make not need separate x, y, w, h, but instead have it get inputted as a rect-like tuple
    type = GO.TINPUTBOX
    def __init__(self, G, x, y, w, h, resize=GO.RWIDTH, placeholder='Type here!', font=GO.FSMALL, maxim=None, starting_text=''):
        super().__init__(G)
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = GO.CINACTIVE
        self.text = starting_text
        self.active = False
        self.resize = resize
        self.maxim = maxim
        self.font = font
        self.blanktxt = placeholder
        self.renderdash = True
    
    def get(self):
        """Get the text in the inputbox"""
        return self.text
    
    def _render_txt(self):
        txtcol = self.colour
        self.text = self.text[:self.maxim]
        txt = self.text
        if txt == '':
            txt = self.blanktxt
            txtcol = GO.CINACTIVE
        self.txt_surface = self.font.render(txt, txtcol, allowed_width=(None if self.resize == GO.RWIDTH else self.rect.w - 5), renderdash=self.renderdash)
        if self.resize == GO.RWIDTH:
            self.rect.w = self.txt_surface.get_width() + 10
        elif self.resize == GO.RHEIGHT:
            self.rect.h = self.txt_surface.get_height() + 10

    def _handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box.
            self.colour = GO.CACTIVE if self.active else GO.CINACTIVE
            self._render_txt()
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self._render_txt()
                if event.key == pygame.K_RETURN:
                    return False
    
    def update(self, mousePos, events):
        if not self.G.pause:
            for event in events:
                if self._handle_event(event) == False:
                    return ReturnState.CALL
        self._render_txt()
        # Blit the text.
        self.G.WIN.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(self.G.WIN, self.colour, self.rect, 2)
    
    def get(self):
        return self.text

class NumInputBox(InputBox):
    type = GO.TNUMBOX
    def __init__(self, G, x, y, w, h, resize=GO.RWIDTH, start=0, max=float('inf'), min=float('-inf'), font=GO.FSMALL, placeholder='Type number here!'):
        super().__init__(G, x, y, w, h, resize, placeholder, font, None, starting_text=str(start))
        self.realnum = start
        self.limits = (min, max)
        self.renderdash = False
    
    def get(self):
        """Get the number in the numbox"""
        return self.realnum

    def _handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box.
            self.colour = GO.CACTIVE if self.active else GO.CINACTIVE
            self._render_txt()
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    try:
                        self.realnum = int(str(self.realnum)[:-1])
                    except:
                        self.realnum = 0
                elif event.key == pygame.K_MINUS:
                    self.realnum = self.realnum * -1
                else:
                    try:
                        self.realnum = int(str(self.realnum) + event.unicode)
                    except:
                        pass
                self.realnum = max(min(self.realnum, self.limits[0]), self.limits[1])
                self.text = str(self.realnum)
                if event.key == pygame.K_RETURN:
                    return False
    
    def get(self):
        return self.realnum

class Scrollable(Element):
    type = GO.TSCROLLABLE
    def __init__(self, G, pos, goalrect, bounds=(0, float('inf')), outline=10, bar=True, outlinecol=(155, 155, 155)):
        super().__init__(G)
        self.bar = bar
        self.pos = pos
        self.goalrect = goalrect
        self.scroll = 0
        self.bounds = bounds
        self.outline = (outline, outlinecol)
    
    def get(self):
        """Get the scroll value"""
        return self.scroll
    
    def update(self, mousePos, events):
        for ev in events:
            if ev.type == pygame.MOUSEWHEEL:
                y = ev.y - 1
                if 0 <= y <= 1: y = 2
                self.scroll += y * 2
                self.scroll = -min(max(self.bounds[0], -self.scroll), self.bounds[1])
        s = pygame.Surface(self.goalrect)
        s.blit(self.sur, (0, self.scroll))
        self.G.WIN.blit(s, self.pos)
        if self.outline[0] != 0: pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(*self.pos, *self.goalrect), self.outline[0], 3)
        if self.bar:
            try:
                try:
                    w = self.outline[0]/2
                except ZeroDivisionError:
                    w = 0
                p = (self.pos[0]+self.goalrect[0]-w, self.pos[1]+((-self.scroll) / self.bounds[1])*(self.goalrect[1]-40)+20)
                pygame.draw.line(self.G.WIN, (200, 50, 50), (p[0], p[1]-20), (p[0], p[1]+20), 10)
            except:
                pass
