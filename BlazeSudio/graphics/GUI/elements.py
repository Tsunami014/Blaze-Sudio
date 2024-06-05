import pygame
from BlazeSudio.graphics import options as GO

# sur/win, pause, mousePos, events, G, func

class Element:
    def __init__(self, typ, uid, G, **kwargs):
        if not isinstance(typ, GO.T___):
            raise TypeError(
                f'Input \'type\' MUST be GO.T___ (e.g. GO.TBUTTON), not {str(typ)}!'
            )
        self.uid = uid
        self.name = typ.name
        self.type = typ
        self.G = G
        try:
            if self.type == GO.TBUTTON:
                self.btn = kwargs['btn']
                self.txt = self.btn.txt
            elif self.type == GO.TTEXTBOX:
                self.sprite = kwargs['sprite']
            elif self.type == GO.TINPUTBOX:
                self.sprite = kwargs['sprite']
                self.txt = kwargs['txt']
            elif self.type == GO.TSWITCH:
                self.sprite = kwargs['sw']
        except KeyError as e:
            raise TypeError(
                f'{self.name} Element requires kwarg "{str(e)}" but was not provided!'
            )
    
    def remove(self):
        """Removes an element.

        Only works on:
         - GO.TTEXTBOX
         - GO.TINPUTBOX
         - GO.TSWITCH
        """
        if self.type == GO.TTEXTBOX:
            self.G.sprites.remove(self.sprite)
        elif self.type == GO.TINPUTBOX:
            self.G.input_boxes.remove(self.sprite)
        elif self.type == GO.TSWITCH:
            self.G.sprites.remove(self.sprite)
        else:
            raise NotImplementedError(
                f'Remove has not been implemented for this element with type {self.name}!'
            )
    
    def set_text(self, txt):
        """Sets text of an element.

        Only works on:
         - GO.TTEXTBOX (A TextBox element)
         
        Parameters:
        txt : str
        """
        if self.type == GO.TTEXTBOX:
            self.sprite.reset(hard=True)
            self.sprite.set_text(txt)
        else:
            raise NotImplementedError(
                f'Set text has not been implemented for this element with type {self.name}!'
            )
    
    def get(self):
        """Gets the state of this element.
        
        Only works on:
         - GO.TSWITCH
         - GO.TINPUTBOX
        
        Returns
        -------
        bool
            Whether the switch is on or not 
        """
        if self.type == GO.TSWITCH:
            return self.sprite.get()
        elif self.type == GO.TINPUTBOX:
            return self.sprite.text
        else:
            raise NotImplementedError(
                f'Set text has not been implemented for this element with type {self.name}!'
            )
    
    def __eq__(self, other):
        return self.uid == other
class Switch:
    def __init__(self, win, x, y, size=20, speed=10, default=False):
        self.isswitch = True
        self.WIN = win
        self.pos = (x, y)
        self.size = size
        self.anim = 0
        self.speed = speed
        self.state = default
        self.rect = pygame.Rect(x, y, size, size)
        self.barrect = pygame.Rect(x+size/4, y, size, size/2)
        self.image = pygame.Surface((0, 0))
        self.source_rect = pygame.Rect(0, 0, 0, 0)
    def update(self, pause, mousePos, events, G, func):
        if self.anim < 0: self.anim = 0
        if self.anim > 15*self.speed: self.anim = 15*self.speed
        if self.anim != (0 if not self.state else 15*self.speed):
            if self.state: self.anim += 1
            else: self.anim -= 1
        pygame.draw.rect(self.WIN, (125, 125, 125), self.barrect, border_radius=self.size)
        pygame.draw.circle(self.WIN, ((0, 255, 0) if self.state else (255, 0, 0)), (self.pos[0]+self.size/4+(self.anim/self.speed)*(self.size/20), self.pos[1]+self.size/4), self.size/2)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and not pause:
                if event.button == pygame.BUTTON_LEFT:
                    if self.rect.collidepoint(mousePos):
                        self.state = not self.state
                        func(GO.EELEMENTCLICK, Element(GO.TSWITCH, G.uids.index(self), G, sw=self))
    def get(self):
        return self.state

# InputBoxes code modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame 

class InputBox:
    def __init__(self, x, y, w, h, resize=GO.RWIDTH, placeholder='Type here!', font=GO.FSMALL, maxim=None, starting_text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = GO.CINACTIVE
        self.text = starting_text
        self.active = False
        self.resize = resize
        self.maxim = maxim
        self.font = font
        self.blanktxt = placeholder
        self.render_txt()
    
    def get(self):
        return self.text
    
    def render_txt(self):
        txtcol = self.colour
        self.text = self.text[:self.maxim]
        txt = self.text
        if txt == '':
            txt = self.blanktxt
            txtcol = GO.CINACTIVE
        self.txt_surface = self.font.render(txt, txtcol, allowed_width=(None if self.resize == GO.RWIDTH else self.rect.w - 5))
        if self.resize == GO.RWIDTH:
            self.rect.w = self.txt_surface.get_width() + 10
        elif self.resize == GO.RHEIGHT:
            self.rect.h = self.txt_surface.get_height() + 10

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box.
            self.colour = GO.CACTIVE if self.active else GO.CINACTIVE
            self.render_txt()
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.render_txt()
                if event.key == pygame.K_RETURN:
                    return False

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.colour, self.rect, 2)
    
    def update(self, sur):
        self.draw(sur)

class NumInputBox:
    def __init__(self, x, y, w, h, resize=GO.RWIDTH, start=0, max=float('inf'), min=float('-inf'), font=GO.FSMALL):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = GO.CINACTIVE
        self.num = str(start)
        self.active = False
        self.resize = resize
        self.bounds = (max, min)
        self.font = font
        self.render_txt()
    
    def get(self):
        if self.num.startswith('-'):
            self.num = '-' + self.num.strip('-') # remove any accidental extra -'s
        self.num = str(min(max(int(self.num), self.bounds[0]), self.bounds[1]))
        return int(self.num)
    
    def render_txt(self):
        self.get()
        self.txt_surface = self.font.render(self.num, self.colour, allowed_width=self.rect.w - 5, renderdash=False)
        if self.resize == GO.RWIDTH:
            self.rect.w = self.txt_surface.get_width() + 10
        elif self.resize == GO.RHEIGHT:
            self.rect.h = self.txt_surface.get_height() + 10

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current colour of the input box.
            self.colour = GO.CACTIVE if self.active else GO.CINACTIVE
            self.render_txt()
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    try: self.num = ('-' if self.num.startswith('-') else '') + \
                                    str(int(self.num[:-1]))
                    except: self.num = '0'
                elif event.key == pygame.K_MINUS:
                    if self.num.startswith('-'): self.num = self.num[1:]
                    else: self.num = '-' + self.num
                else:
                    try: self.num = ('-' if self.num.startswith('-') else '') + \
                                    str(int(self.num+event.unicode))
                    except: pass
                # Re-render the text.
                self.render_txt()
                if event.key == pygame.K_RETURN:
                    return False

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.colour, self.rect, 2)
    
    def update(self, sur, pause, events, G):
        self.draw(sur)
        if not pause:
            for event in events:
                if self.handle_event(event) == False:
                    G.Abort()

class Scrollable:
    def __init__(self, sur, pos, goalrect, bounds=(0, float('inf')), outline=10, bar=True, outlinecol=(155, 155, 155)):
        self.sur = sur
        self.bar = bar
        self.pos = pos
        self.goalrect = goalrect
        self.scroll = 0
        self.bounds = bounds
        self.outline = (outline, outlinecol)
    def event_handle(self, event):
        y = event.y - 1
        if 0 <= y <= 1: y = 2
        self.scroll += y * 2
        self.scroll = -min(max(self.bounds[0], -self.scroll), self.bounds[1])
    
    def __call__(self, WIN):
        s = pygame.Surface(self.goalrect)
        s.blit(self.sur, (0, self.scroll))
        WIN.blit(s, self.pos)
        if self.outline[0] != 0: pygame.draw.rect(WIN, self.outline[1], pygame.Rect(*self.pos, *self.goalrect), self.outline[0], 3)
        if self.bar:
            try:
                try: w = self.outline[0]/2
                except ZeroDivisionError: w = 0
                p = (self.pos[0]+self.goalrect[0]-w, self.pos[1]+((-self.scroll) / self.bounds[1])*(self.goalrect[1]-40)+20)
                pygame.draw.line(WIN, (200, 50, 50), (p[0], p[1]-20), (p[0], p[1]+20), 10)
            except: pass
