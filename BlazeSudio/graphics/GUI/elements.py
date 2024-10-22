import pygame
from typing import Callable
from string import printable
from BlazeSudio.graphics import options as GO
from BlazeSudio.graphics.GUI.base import Element, ReturnState

__all__ = [
    'Switch',
    'InputBox',
    'NumInputBox',
    'Empty',
    'Static',
    'Text',
    'Button'
]

class Switch(Element):
    type = GO.TSWITCH
    def __init__(self, G, pos: GO.P___, size=20, speed=1, default=False):
        """
        A switch that can be either on or off.

        Args:
            G (Graphic): The graphic screen to attach to.
            pos (GO.P___): The position of this element in the screen.
            size (int, optional): The size of this element. Defaults to 20.
            speed (int, optional): The speed of the toggling of the switch. Defaults to 1.
            default (bool, optional): Whether the switch is either on or off on creation. Defaults to False.
        """
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
            if event.type == pygame.MOUSEBUTTONDOWN and \
               (not self.G.pause) and \
               event.button == pygame.BUTTON_LEFT and \
               pygame.Rect(x, y, *self.size).collidepoint(mousePos):
                self.state = not self.state
                return ReturnState.CALL
    
    def get(self):
        """Get the state of the switch (on or off)"""
        return self.state
    def set(self, newState):
        """Set the state of the switch (on or off)"""
        self.state = newState

# InputBoxes code modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame 

# TODO: A text cursor
class InputBox(Element):
    type = GO.TINPUTBOX
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 width: int, 
                 resize: GO.R___ = GO.RWIDTH, 
                 placeholder: str = 'Type here!', 
                 font: GO.F___ = GO.FSMALL, 
                 maxim: int = None, 
                 starting_text: str = ''
                ):
        """
        A box for inputting text.

        Args:
            G (Graphic): The graphic screen to attach to.
            pos (GO.P___): The position of this element in the screen.
            width (int): The width of the box. This will get overridden if using GO.RWIDTH.
            resize (GO.R___, optional): How to overflow text if the box is too large. Defaults to GO.RWIDTH.
            placeholder (str, optional): The placeholder text visible when there is no text in the box. Defaults to 'Type here!'.
            font (GO.F___, optional): The font of the text in the box. Defaults to GO.FSMALL.
            maxim (int, optional): The maximum number of characters that can be inputted. Defaults to None (infinite).
            starting_text (str, optional): The text in the box on creation. Defaults to ''.
        """
        
        self.colour = GO.CINACTIVE
        self.text = starting_text
        self.active = False
        self.resize = resize
        self.maxim = maxim
        self.font = font
        self.blanktxt = placeholder
        self.renderdash = True

        self.size = [width+5, font.linesize+5]
        self._render_txt()
        super().__init__(G, pos, self.size)
    
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
    
    def _handle_text(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            if event.unicode in printable:
                self.text += event.unicode
    
    def update(self, mousePos, events):
        if not self.G.pause:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    # If the user clicked on the input_box rect.
                    if pygame.Rect(*self.stackP(), *self.size).collidepoint(mousePos):
                        # Toggle the active variable.
                        self.active = not self.active
                    else:
                        self.active = False
                    # Change the current colour of the input box.
                    self.colour = GO.CACTIVE if self.active else GO.CINACTIVE
                    self._render_txt()
                elif event.type == pygame.KEYDOWN:
                    if self.active:
                        self._handle_text(event)
                        # Re-render the text.
                        self._render_txt()
                        if event.key == pygame.K_RETURN:
                            return ReturnState.CALL
        # Blit the text.
        x, y = self.stackP()
        self.G.WIN.blit(self.txt_surface, (x+5, y+5))
        # Blit the rect.
        pygame.draw.rect(self.G.WIN, self.colour, pygame.Rect(x, y, *self.size), 2)

class NumInputBox(InputBox): # TODO: Decimals
    type = GO.TNUMBOX
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 width: int, 
                 resize: GO.R___ = GO.RWIDTH, 
                 font: GO.F___ = GO.FSMALL, 
                 start: int = 0, 
                 max: int = float('inf'), 
                 min: int = float('-inf'), 
                 placeholder: str = 'Type number here!'
                ):
        """
        A box for inputting numbers.

        Args:
            G (Graphic): The graphic screen to attach to.
            pos (GO.P___): The position of this element in the screen.
            width (int): The width of the box. This will get overridden if using GO.RWIDTH.
            resize (GO.R___, optional): How to overflow text if the box is too large. Defaults to GO.RWIDTH.
            font (GO.F___, optional): The font of the text in the box. Defaults to GO.FSMALL.
            start (int, optional): The number present in the box on creation. Defaults to 0.
            max (int, optional): The maximum value that can be submitted in this box. Defaults to infinity.
            min (int, optional): The minimum value that can be submitted in this box. Defaults to -infinity.
            placeholder (str, optional): The placeholder text visible when there is no text in the box. \
                Defaults to 'Type number here!'. I don't think this one will be present very much if at all.
        """
        super().__init__(G, pos, width, resize, placeholder, font, None, starting_text=str(start))
        self.realnum = start
        self.limits = (min, max)
        self.renderdash = False
    
    def get(self):
        """Get the number in the numbox"""
        return self.realnum

    def set(self, newNum):
        """Set the number in the numbox"""
        self.realnum = newNum

    def _handle_text(self, event):
        if event.key == pygame.K_BACKSPACE:
            # if str(self.realnum)[:-1].endswith('.'):
            #     self.realnum = int(self.realnum)
            # else:
            try:
                self.realnum = int(str(self.realnum)[:-1])
            except:
                self.realnum = 0
        elif event.key == pygame.K_MINUS:
            self.realnum = self.realnum * -1
        else:
            if event.unicode in '0123456789':
                self.realnum = int(str(self.realnum) + event.unicode)
            # elif event.unicode == '.':
            #     self.realnum = float(self.realnum)
        self.realnum = max(min(self.realnum, self.limits[1]), self.limits[0])
        self.text = str(self.realnum)

class Empty(Element):
    type = GO.TEMPTY
    def __init__(self, G, pos: GO.P___, size):
        """
        Some empty space.

        Args:
            G (Graphic): The graphic screen to attach to.
            pos (GO.P___): The position of this element in the screen.
            size (Iterable[number, number]): The size of the empty space.
        """
        super().__init__(G, pos, size)
    
    def get(self):
        """Get the size"""
        return self.size
    
    def set(self, size):
        """Set the size"""
        self.size = size

class Static(Element):
    type = GO.TSTATIC
    def __init__(self, G, pos: GO.P___, sur: pygame.Surface):
        """
        A static surface.

        Args:
            G (Graphic): The graphic screen to attach to.
            pos (GO.P___): The position of this element in the screen.
            sur (pygame.Surface): The surface.
        """
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
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 txt: str, 
                 col: GO.C___ = GO.CBLACK, 
                 font: GO.F___ = GO.FFONT, 
                 **settings):
        """
        A Text element.

        Args:
            G (Graphic): The graphic this element is in.
            pos (GO.P___): The position of this element.
            txt (str): The text that will be displayed.
            col (GO.C___, optional): The colour of the text. Defaults to GO.CBLACK.
            font (GO.F___, optional): The font of the text. Defaults to GO.FFONT.
            **settings: The settings for rendering the text. See `GO.F___.render` for more information.
        """
        self.font = font
        self.col = col
        self.settings = settings
        self.set(txt)
        super().__init__(G, pos, self.size)
    
    def get(self):
        """Get the text of this text element"""
        return self.txt
    
    def set(self, newTxt, **settings):
        """Sets the text of this text element, and optionally update the render settings."""
        self.settings.update(settings)
        self.txt = newTxt
        self.sur = self.font.render(self.txt, self.col, **self.settings)
        self.size = self.sur.get_size()
    
    def update(self, mpos, events):
        self.G.WIN.blit(self.sur, self.stackP())


class Button(Element):
    type = GO.TBUTTON
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 BGcol: GO.C___, 
                 txt: str, 
                 TXTcol: GO.C___ = GO.CBLACK, 
                 font: GO.F___ = GO.FFONT, 
                 spacing=2, 
                 on_hover_enlarge=5, 
                 func: Callable = lambda: None, 
                 **settings
                ):
        """
        A Button element.

        Args:
            G (Graphic): The graphic this element is in.
            pos (GO.P___): The position of this element.
            BGcol (GO.C___): The background colour of the button.
            txt (str): The text on the button.
            TXTcol (GO.C___, optional): The colour of the text. Defaults to GO.CBLACK.
            font (GO.F___, optional): The font of the text. Defaults to GO.FFONT.
            spacing (int, optional): The spacing between the outer edge of the button and the inner text. Defaults to 2.
            on_hover_enlarge (int, optional): The amount to enlarge the outer edge of the button when hovering. Defaults to 5.
            func (Callable, optional): The function to call when the button is pressed. Defaults to a do nothing func.
        """
        self.font = font
        self.spacing = spacing
        self.OHE = on_hover_enlarge
        self.settings = settings
        self.cols = {"BG": BGcol, "TXT": TXTcol}
        self.func = func

        self.set(txt) # Sets self.txt and generates self.TxtSur
        super().__init__(G, pos, self.size)
    
    def get(self):
        """Get the text on the button"""
        return self.textElm.txt
    
    def set(self, newTxt, **settings):
        """Set the text on the button, and optionally update some text settings settings."""
        self.settings.update(settings)
        self.txt = newTxt
        self.TxtSur = self.font.render(self.txt, self.cols['TXT'], **self.settings)
        s = self.TxtSur.get_size()
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
                    if any([i.type == pygame.MOUSEBUTTONDOWN and i.button == pygame.BUTTON_LEFT for i in events]):
                        ret = self.func()
                        if ret:
                            if ReturnState.DONTCALL not in ret:
                                return ReturnState.REDRAW + ReturnState.CALL + ret
                        else:
                            return ReturnState.REDRAW + ReturnState.CALL
                    else:
                        return ReturnState.REDRAW
        pygame.draw.rect(self.G.WIN, self.cols['BG'], r, border_radius=8)
        self.G.WIN.blit(self.TxtSur, (r.x + (r.width-self.TxtSur.get_width())/2, r.y + (r.height-self.TxtSur.get_height())/2))
