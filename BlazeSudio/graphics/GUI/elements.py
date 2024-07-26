from enum import Enum
from typing import Any
import pygame
from BlazeSudio.graphics import options as GO
from BlazeSudio.graphics.stacks import StackPart

class Element:
    NEXT_UID = [0]
    type = None
    def __init__(self, G, pos, size):
        self.G = G
        self.pos = pos
        self.size = size
        self.stackP = StackPart(G.stacks, pos, size, G.size)
        self.uid = self.NEXT_UID[0]
        self.NEXT_UID[0] += 1
    
    def remove(self):
        self.stackP.remove()
        self.G.Stuff.remove(self)
    
    def change_pos(self, newPos):
        self.stackP.remove()
        self.pos = newPos
        self.stackP = StackPart(self.G.stacks, newPos, self.size, self.G.size)
    
    # Required subclass functions
    def update(self, mousePos, events):
        pass
    
    def get(self):
        pass
    
    def set(self):
        pass
    
    # Utility functions
    def __eq__(self, other):
        return self.uid == other
    
    def __hash__(self):
        return hash(self.uid)
    
    def __setattr__(self, name: str, value: Any) -> None: # TODO: Use @size.setter
        super().__setattr__(name, value)
        if name == 'size' and 'stackP' in self.__dict__: # Safeguard against running this before initialisation of stackP
            self.stackP.setSize(self.size) # Automatically update stackP size whenever you set self.size
    
    def __str__(self):
        return f'<{self.__class__.__name__}({str(self.get())})>'
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


class Switch(Element):
    type = GO.TSWITCH
    def __init__(self, G, pos, size=20, speed=1, default=False):
        self.btnSze = size
        super().__init__(G, pos, (size*2, size))
        self.anim = 0
        self.speed = speed
        self.state = default
    
    def update(self, mousePos, events):
        self.anim = min(max(self.anim, 0), self.btnSze)
        if self.anim != (0 if not self.state else self.btnSze):
            if self.state:
                self.anim += self.speed
            else:
                self.anim -= self.speed
        x, y = self.stackP()
        pygame.draw.rect(self.G.WIN, (125, 125, 125), pygame.Rect(x+self.btnSze/2, y+self.btnSze/4, self.btnSze, self.btnSze/2), border_radius=self.btnSze)
        pygame.draw.circle(self.G.WIN, ((0, 255, 0) if self.state else (255, 0, 0)), (x+self.btnSze/2+self.anim, y+self.btnSze/2), self.btnSze/2)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.G.pause:
                if event.button == pygame.BUTTON_LEFT:
                    if pygame.Rect(x, y, *self.size).collidepoint(mousePos):
                        self.state = not self.state
                        return ReturnState.CALL
    
    def get(self):
        """Get the state of the switch (on or off)"""
        return self.state
    def set(self, newState):
        """Set the state of the switch (on or off)"""
        self.state = newState

# InputBoxes code modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame 

class InputBox(Element):
    type = GO.TINPUTBOX
    def __init__(self, G, pos, sze, resize=GO.RWIDTH, placeholder='Type here!', font=GO.FSMALL, maxim=None, starting_text=''):
        super().__init__(G, pos, sze)
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
    
    def set(self, txt):
        """Set the text in the textbox"""
        self.text = txt
    
    def _render_txt(self):
        txtcol = self.colour
        self.text = self.text.strip('\r\n')[:self.maxim]
        txt = self.text
        if txt == '':
            txt = self.blanktxt
            txtcol = GO.CINACTIVE
        self.txt_surface = self.font.render(txt, txtcol, allowed_width=(None if self.resize == GO.RWIDTH else self.size[0] - 5), renderdash=self.renderdash)
        if self.resize == GO.RWIDTH:
            self.size[0] = self.txt_surface.get_width() + 10
        elif self.resize == GO.RHEIGHT:
            self.size[1] = self.txt_surface.get_height() + 10

    def _handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if pygame.Rect(*self.stackP(), *self.size).collidepoint(event.pos):
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
        x, y = self.stackP()
        self.G.WIN.blit(self.txt_surface, (x+5, y+5))
        # Blit the rect.
        pygame.draw.rect(self.G.WIN, self.colour, pygame.Rect(x, y, *self.size), 2)
    
    def get(self):
        return self.text

class NumInputBox(InputBox):
    type = GO.TNUMBOX
    def __init__(self, G, pos, sze, resize=GO.RWIDTH, start=0, max=float('inf'), min=float('-inf'), font=GO.FSMALL, placeholder='Type number here!'):
        super().__init__(G, pos, sze, resize, placeholder, font, None, starting_text=str(start))
        self.realnum = start
        self.limits = (min, max)
        self.renderdash = False
    
    def get(self):
        """Get the number in the numbox"""
        return self.realnum

    def set(self, newNum):
        """Set the number in the numbox"""
        self.realnum = newNum

    def _handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if pygame.Rect(*self.stackP(), *self.size).collidepoint(event.pos):
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
        super().__init__(G, pos, goalrect)
        self.bar = bar
        self.scroll = 0
        self.bounds = bounds
        self.outline = (outline, outlinecol)
    
    def get(self):
        """Get the scroll value"""
        return self.scroll
    
    def set(self, scroll):
        """Set the scroll value"""
        self.scroll = scroll
    
    def update(self, mousePos, events):
        for ev in events:
            if ev.type == pygame.MOUSEWHEEL:
                y = ev.y - 1
                if 0 <= y <= 1:
                    y = 2
                self.scroll += y * 2
                self.scroll = -min(max(self.bounds[0], -self.scroll), self.bounds[1])
        s = pygame.Surface(self.size)
        s.blit(self.sur, (0, self.scroll))
        x, y = self.stackP()
        self.G.WIN.blit(s, (x, y))
        if self.outline[0] != 0:
            pygame.draw.rect(self.G.WIN, self.outline[1], pygame.Rect(x, y, *self.size), self.outline[0], 3)
        if self.bar:
            try:
                try:
                    w = self.outline[0]/2
                except ZeroDivisionError:
                    w = 0
                p = (x+self.size[0]-w, y+((-self.scroll) / self.bounds[1])*(self.size[1]-40)+20)
                pygame.draw.line(self.G.WIN, (200, 50, 50), (p[0], p[1]-20), (p[0], p[1]+20), 10)
            except:
                pass

class Empty(Element):
    type = GO.TEMPTY
    def __init__(self, G, pos, size):
        super().__init__(G, pos, size)
    
    def get(self):
        """Get the size"""
        return self.size
    
    def set(self, size):
        """Set the size"""
        self.size = size

class Static(Element):
    type = GO.TSTATIC
    def __init__(self, G, pos, sur):
        self.sur = sur
        super().__init__(G, pos, self.sur.get_size())
    
    def get(self):
        """Get the surface"""
        return self.sur
    
    def set(self, sur):
        """Set the surface"""
        self.sur = sur
        self.size = self.sur.get_size()
    
    def update(self, mpos, events):
        self.G.WIN.blit(self.sur, self.stackP())

class Text(Element):
    type = GO.TSTATIC
    def __init__(self, G, pos, func, txt):
        self.func = func
        self.set(txt)
        super().__init__(G, pos, self.size)
    
    def get(self):
        """Get the text of this text element"""
        return self.txt
    
    def set(self, newTxt):
        """Sets the text of this text element"""
        self.txt = newTxt
        self.sur = self.func(self.txt)
        self.size = self.sur.get_size()
    
    def update(self, mpos, events):
        self.G.WIN.blit(self.sur, self.stackP())


class Button(Element):
    type = GO.TBUTTON
    def __init__(self, G, pos, col, spacing, fontfunc, txt, on_hover_enlarge):
        self.fontFunc = fontfunc
        self.spacing = spacing
        self.OHE = on_hover_enlarge
        self.set(txt) # Sets self.txt and generates self.sur
        super().__init__(G, pos, self.size)
        self.col = col
    
    def get(self):
        """Get the text on the button"""
        return self.txt
    
    def set(self, newTxt):
        """Set the text on the button"""
        self.txt = newTxt
        self.sur = self.fontFunc(self.txt)
        s = self.sur.get_size()
        self.size = (s[0] + self.OHE*2 + self.spacing*2, s[1] + self.OHE*2 + self.spacing*2)
    
    def update(self, mousePos, events, force_draw=False):
        r = pygame.Rect(*self.stackP(), *self.size)
        r.x += self.OHE
        r.y += self.OHE
        r.width -= self.OHE
        r.height -= self.OHE
        if not self.G.pause:
            if r.collidepoint(mousePos):
                if self.OHE != -1:
                    r.x -= self.OHE
                    r.y -= self.OHE
                    r.width += self.OHE*2
                    r.height += self.OHE*2
                if not force_draw:
                    if any([i.type == pygame.MOUSEBUTTONDOWN for i in events]):
                        return ReturnState.CALL + ReturnState.TBUTTON
                    return ReturnState.TBUTTON
        pygame.draw.rect(self.G.WIN, self.col, r, border_radius=8)
        self.G.WIN.blit(self.sur, (r.x + (r.width-self.sur.get_width())/2, r.y + (r.height-self.sur.get_height())/2))
