from math import floor
import pygame
from typing import Callable, Iterable
from string import printable
from random import random
from BlazeSudio.graphics import mouse, options as GO
from BlazeSudio.graphics.base import Element, ReturnGroup, ReturnState
from BlazeSudio.graphics.GUI.theme import GLOBALTHEME
from BlazeSudio.graphics.GUI.events import Dropdown

__all__ = [
    'Switch',
    'Checkbox',
    'InputBox',
    'NumInputBox',
    'Empty',
    'Static',
    'Text',
    'Button',
    'DropdownButton',
    'ImageViewer'
]

class Switch(Element):
    type = GO.TSWITCH
    def __init__(self, pos: GO.P___, size=20, speed=1, default=False):
        """
        A switch that can be either on or off.

        Args:
            pos (GO.P___): The position of this element in the screen.
            size (int, optional): The size of this element. Defaults to 20.
            speed (int, optional): The speed of the toggling of the switch. Defaults to 1.
            default (bool, optional): Whether the switch is either on or off on creation. Defaults to False.
        """
        self.btnSze = size
        super().__init__(pos, (size*2, size))
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
        if mousePos:
            mcollides = pygame.Rect(x, y, *self.size).collidepoint(mousePos)
        else:
            mcollides = False
        if not self.G.pause:
            if mcollides:
                if pygame.mouse.get_pressed()[0]:
                    mouse.Mouse.set(mouse.MouseState.CLICKING)
                else:
                    mouse.Mouse.set(mouse.MouseState.HOVER)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and \
                event.button == pygame.BUTTON_LEFT and mcollides:
                    self.state = not self.state
                    return ReturnState.CALL
    
    def draw(self):
        x, y = self.stackP()
        pygame.draw.rect(self.G.WIN, (125, 125, 125), pygame.Rect(x+self.btnSze/2, y+self.btnSze/4, self.btnSze, self.btnSze/2), border_radius=self.btnSze)
        pygame.draw.circle(self.G.WIN, ((0, 255, 0) if self.state else (255, 0, 0)), (x+self.btnSze/2+self.anim, y+self.btnSze/2), self.btnSze/2)
    
    def get(self):
        """Get the state of the switch (on or off)"""
        return self.state
    def set(self, newState):
        """Set the state of the switch (on or off)"""
        self.state = newState

class Checkbox(Element):
    type = GO.TCHECKBOX
    def __init__(self, pos: GO.P___, size=40, thickness=5, check_size=15, radius=5, default=False):
        """
        A checkbox that can be either checked or unchecked.

        Args:
            pos (GO.P___): The position of this element in the screen.
            size (int, optional): The size of this element. Defaults to 40.
            thickness (int, optional): The thickness of the lines. Defaults to 5.
            check_size (int, optional): The size of the check mark arrow. Defaults to 20.
            radius (int, optional): The border radius of the drawn boxes. Defaults to 5.
            default (bool, optional): Whether the checkbox is either on or off on creation. Defaults to False.
        """
        self.thickness = thickness
        self.BR = radius
        self.Csize = check_size
        self.rerandomise()
        super().__init__(pos, (size, size))
        self.state = default
    
    def rerandomise(self):
        self.randoms = [random()+1, random()+1, random()+3, random()*2+4]
    
    def update(self, mousePos, events):
        x, y = self.stackP()
        if mousePos:
            mcollides = pygame.Rect(x, y, *self.size).collidepoint(mousePos)
        else:
            mcollides = False
        if not self.G.pause:
            if mcollides:
                if pygame.mouse.get_pressed()[0]:
                    mouse.Mouse.set(mouse.MouseState.CLICKING)
                else:
                    mouse.Mouse.set(mouse.MouseState.HOVER)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and \
                event.button == pygame.BUTTON_LEFT and mcollides:
                    self.state = not self.state
                    self.rerandomise()
                    return ReturnState.CALL
    
    def draw(self):
        x, y = self.stackP()
        pygame.draw.rect(self.G.WIN, (125, 125, 125), pygame.Rect(x, y, *self.size), self.thickness, self.BR)
        if self.state:
            midp = (x+self.size[0]/2, y+self.size[1]-(self.size[1]/self.randoms[3]))
            p1 = (midp[0]-self.Csize*self.randoms[0], midp[1]-self.Csize)
            p2 = (midp[0]+self.Csize*self.randoms[1], midp[1]-self.Csize*self.randoms[2])
            pygame.draw.line(self.G.WIN, GO.CGREEN, p1, midp, self.thickness+1)
            pygame.draw.line(self.G.WIN, GO.CGREEN, midp, p2, self.thickness+1)
            for p in (p1, midp, p2):
                pygame.draw.circle(self.G.WIN, GO.CGREEN, p, self.thickness//2+1)
    
    def get(self):
        """Get the state of the checkbox (on or off)"""
        return self.state
    def set(self, newState):
        """Set the state of the checkbox (on or off)"""
        self.state = newState

# InputBoxes code modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame 

# TODO: A text cursor
class InputBox(Element): # TODO: Change colours
    type = GO.TINPUTBOX
    def __init__(self, 
                 pos: GO.P___, 
                 width: int, 
                 resize: GO.R___ = GO.RWIDTH, 
                 placeholder: str = 'Type here!', 
                 font: GO.F___ = GO.FREGULAR, 
                 maxim: int = None, 
                 weight: GO.SW__ = GO.SWMID,
                 starting_text: str = ''
                ):
        """
        A box for inputting text.

        Args:
            pos (GO.P___): The position of this element in the screen.
            width (int): The width of the box. This will get overridden if using GO.RWIDTH.
            resize (GO.R___, optional): How to overflow text if the box is too large. Defaults to GO.RWIDTH.
            placeholder (str, optional): The placeholder text visible when there is no text in the box. Defaults to 'Type here!'.
            font (GO.F___, optional): The font of the text in the box. Defaults to GO.FREGULAR.
            maxim (int, optional): The maximum number of characters that can be inputted. Defaults to None (infinite).
            weight (GO.SW__, optional): The weighting of the text left-right. Defaults to GO.SWMID.
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
        self.weight = weight
        self.useMD = False

        self.size = [width+5, font.linesize+5]
        self._render_txt()
        super().__init__(pos, self.size)
    
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
        self.txt_surface = self.font.render(txt, txtcol, leftrightweight=self.weight, allowed_width=(None if self.resize == GO.RWIDTH else self.size[0] - 5), useMD=self.useMD, renderdash=self.renderdash)
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
            mcollide = bool(mousePos) and pygame.Rect(*self.stackP(), *self.size).collidepoint(*mousePos)
            if mcollide:
                mouse.Mouse.set(mouse.MouseState.TEXT)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    # If the user clicked on the input_box rect.
                    if mcollide:
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
    
    def draw(self):
        # Blit the text.
        x, y = self.stackP()
        self.G.WIN.blit(self.txt_surface, (x+5+((self.size[0]-10)-self.txt_surface.get_width())*self.weight.w, y+5))
        # Blit the rect.
        pygame.draw.rect(self.G.WIN, self.colour, pygame.Rect(x, y, *self.size), 2)

class NumInputBox(InputBox):
    type = GO.TNUMBOX
    def __init__(self, 
                 pos: GO.P___, 
                 width: int, 
                 resize: GO.R___ = GO.RWIDTH, 
                 font: GO.F___ = GO.FREGULAR, 
                 start: int|None = None, 
                 empty: int|None = 0,
                 maxim: int = float('inf'), 
                 minim: int = float('-inf'), 
                 decimals: bool|int = False,
                 placeholder: str = 'Type number here!',
                 placeholdOnNum: None|bool|int = False
                ):
        """
        A box for inputting numbers.

        Args:
            pos (GO.P___): The position of this element in the screen.
            width (int): The width of the box. This will get overridden if using GO.RWIDTH.
            resize (GO.R___, optional): How to overflow text if the box is too large. Defaults to GO.RWIDTH.
            font (GO.F___, optional): The font of the text in the box. Defaults to GO.FREGULAR.
            start (int|None, optional): The number present in the box on creation, or None to start empty. Defaults to None.
            empty (int|None, optional): The number to set the box to if the box is empty, or None to be the 'start' param. Defaults to 0.
            maxim (int, optional): The maximum value that can be submitted in this box. Defaults to infinity.
            minim (int, optional): The minimum value that can be submitted in this box. Defaults to -infinity.
            decimals (bool|int, optional): Whether to allow decimals in the number (and if an int, to how many decimal places). Defaults to False.
            placeholder (str, optional): The placeholder text visible when there is no text in the box. Defaults to 'Type number here!'.
            placeholdOnNum (bool|int, optional): **True** = show the placeholder on empty, \
                **False** = only show the placeholder once before you input your first number, \
                **None** = don't show the placeholder ever \
                **int** = show the placeholder if the number is equal to this int. Defaults to False.
        """
        if placeholdOnNum is True:
            self.placehold = ''
        elif placeholdOnNum is False:
            self.placehold = True
        elif placeholdOnNum is None:
            self.placehold = False
        else:
            self.placehold = str(placeholdOnNum)
        if empty is None:
            self.emptyValue = start or 0
        else:
            self.emptyValue = empty
        self.emptyValue = min(max(self.emptyValue, minim), maxim)
        super().__init__(pos, width, resize, placeholder, font, None, starting_text=(str(start) if start is not None else ''))
        self.limits = (minim, maxim)
        self.decimals = decimals
        self.renderdash = False
        self.fix()
        self._render_txt()
    
    def get(self, noneIfEmpty=False):
        """Get the number in the numbox, optionally returning None if the textbox is empty (default False)"""
        if noneIfEmpty and self.text == '':
            return None
        if self.text == '':
            return self.emptyValue
        elif '.' in self.text:
            return float(self.text)
        return int(self.text)

    def set(self, newNum):
        """Set the number in the numbox"""
        self.text = str(newNum)
        self.fix()
    
    def _render_txt(self):
        txtcol = self.colour

        t = self.text
        if self.placehold is True or self.text == self.placehold:
            placeholdCol = True
            t = self.blanktxt
        else:
            if t == '':
                t = str(self.emptyValue)
                placeholdCol = True
            else:
                placeholdCol = False
        
        if placeholdCol:
            txtcol = GO.CINACTIVE
        
        self.txt_surface = self.font.render(t, txtcol, leftrightweight=self.weight, allowed_width=(None if self.resize == GO.RWIDTH else self.size[0] - 5), useMD=self.useMD, renderdash=self.renderdash)
        if self.resize == GO.RWIDTH:
            self.size[0] = self.txt_surface.get_width() + 10
        elif self.resize == GO.RHEIGHT:
            self.size[1] = self.txt_surface.get_height() + 10

    def _handle_text(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.key == pygame.K_MINUS:
            if self.text.startswith('-'):
                self.text = self.text[1:]
            else:
                self.text = '-' + self.text
        elif event.key == pygame.K_PERIOD:
            if '.' not in self.text and self.decimals:
                self.text += '.'
        else:
            if event.unicode in '0123456789':
                self.text += event.unicode
        self.fix()
    
    def fix(self):
        if self.text == '':
            return
        if self.text == '-':
            num = 0
        else:
            num = float(self.text)
        if float(num) > self.limits[1]:
            self.text = str(self.limits[1])
        elif float(num) < self.limits[0]:
            self.text = str(self.limits[0])
        
        if '.' in self.text and not self.decimals:
            self.text = self.text[:self.text.index('.')]
        elif '.' in self.text and not isinstance(self.decimals, bool):
            self.text = self.text[:self.text.index('.')+1+self.decimals]
        
        if not self.active and self.text.endswith('.'):
            self.text = self.text[:-1]
        
        if self.placehold is True and self.text != str(self.emptyValue):
            self.placehold = None
        
        if self.text.startswith('0') and not self.text.startswith('0.') and len(self.text) > 1:
            self.text = self.text[1:]

class Empty(Element):
    type = GO.TEMPTY
    def __init__(self, pos: GO.P___, size):
        """
        Some empty space.

        Args:
            G (Graphic): The graphic screen to attach to.
            pos (GO.P___): The position of this element in the screen.
            size (Iterable[number, number]): The size of the empty space.
        """
        super().__init__(pos, size)
    
    def get(self):
        """Get the size"""
        return self.size
    
    def set(self, size):
        """Set the size"""
        self.size = size

class Static(Element):
    type = GO.TSTATIC
    def __init__(self, pos: GO.P___, sur: pygame.Surface):
        """
        A static surface.

        Args:
            pos (GO.P___): The position of this element in the screen.
            sur (pygame.Surface): The surface.
        """
        self.sur = sur
        super().__init__(pos, self.sur.get_size())
    
    def get(self):
        """Get the surface"""
        return self.sur
    
    def set(self, sur):
        """Set the surface"""
        self.sur = sur
        self.size = self.sur.get_size()
    
    def draw(self):
        self.G.WIN.blit(self.sur, self.stackP())

class Text(Element):
    type = GO.TSTATIC
    def __init__(self, 
                 pos: GO.P___, 
                 txt: str, 
                 col: GO.C___ = GO.CBLACK, 
                 font: GO.F___ = GO.FREGULAR, 
                 useMD: bool = True,
                 **settings):
        """
        A Text element.

        Args:
            pos (GO.P___): The position of this element.
            txt (str): The text that will be displayed.
            col (GO.C___, optional): The colour of the text. Defaults to GO.CBLACK.
            font (GO.F___, optional): The font of the text. Defaults to GO.FREGULAR.
            useMD (bool, optional): Whether or not to use markdown. Defaults to True.
            \\*\\*settings: The settings for rendering the text. See `GO.F___.render` for more information.
        
        Useful Settings:
            allowed_width (int): The maximum width of the text. Defaults to None.
            leftrightweight (GO.SW__): The weighting of the text left-right. Defaults to GO.SWMID.
        """
        self.font = font
        self.col = col
        self.settings = settings
        self.settings['useMD'] = useMD
        self.set(txt)
        super().__init__(pos, self.size)
    
    def get(self):
        """Get the text of this text element"""
        return self.txt
    
    def set(self, newTxt, **settings):
        """Sets the text of this text element, and optionally update the render settings."""
        self.settings.update(settings)
        self.txt = newTxt
        self.sur = self.font.render(self.txt, self.col, **self.settings)
        self.size = self.sur.get_size()
    
    def draw(self):
        self.G.WIN.blit(self.sur, self.stackP())

class Button(Element):
    type = GO.TBUTTON
    def __init__(self, 
                 pos: GO.P___, 
                 BGcol: GO.C___, 
                 txt: str, 
                 TXTcol: GO.C___ = GO.CBLACK, 
                 font: GO.F___ = GO.FREGULAR, 
                 spacing=2, 
                 on_hover_enlarge=5, 
                 func: Callable = lambda: None, 
                 **settings
                ):
        """
        A Button element.

        Args:
            pos (GO.P___): The position of this element.
            BGcol (GO.C___): The background colour of the button.
            txt (str): The text on the button.
            TXTcol (GO.C___, optional): The colour of the text. Defaults to GO.CBLACK.
            font (GO.F___, optional): The font of the text. Defaults to GO.FREGULAR.
            spacing (int, optional): The spacing between the outer edge of the button and the inner text. Defaults to 2.
            on_hover_enlarge (int, optional): The amount to enlarge the outer edge of the button when hovering. Defaults to 5.
            func (Callable, optional): The function to call when the button is pressed. Defaults to a do nothing func.
            \\*\\*settings: The settings for rendering the text. See `GUI.Text.__init__` or `GO.F___.render` for more information.
        
        Useful Settings:
            allowed_width (int, optional): The maximum width of the text. Defaults to None.
        """
        self.font = font
        self.spacing = spacing
        self.OHE = on_hover_enlarge
        self.settings = settings
        self.cols = {"BG": BGcol, "TXT": TXTcol}
        self.func = func

        self._set_txt(txt) # Sets self.txt and generates self.TxtSur
        super().__init__(pos, self.size)
    
    def get(self):
        """Get the text on the button"""
        return self.txt
    
    def set(self, newTxt, **settings):
        """Set the text on the button, and optionally update some text settings settings."""
        self._set_txt(newTxt, **settings)

    def _set_txt(self, newTxt, **settings):
        self.settings.update(settings)
        self.txt = newTxt
        self.TxtSur = self.font.render(self.txt, self.cols['TXT'], **self.settings)
        s = self.TxtSur.get_size()
        self.size = (s[0] + self.OHE*2 + self.spacing*2, s[1] + self.OHE*2 + self.spacing*2)
    
    def update(self, mousePos, events):
        r = pygame.Rect(*self.stackP(), *self.size)
        r.x += self.OHE
        r.y += self.OHE
        r.width -= self.OHE
        r.height -= self.OHE
        if not self.G.pause:
            if bool(mousePos) and r.collidepoint(*mousePos):
                if pygame.mouse.get_pressed()[0]:
                    mouse.Mouse.set(mouse.MouseState.CLICKING)
                else:
                    mouse.Mouse.set(mouse.MouseState.HOVER)
                if any([i.type == pygame.MOUSEBUTTONDOWN and i.button == pygame.BUTTON_LEFT for i in events]):
                    ret = self.func()
                    if isinstance(ret, (ReturnState, ReturnGroup)):
                        if ReturnState.DONTCALL not in ret:
                            return ReturnState.REDRAW + ReturnState.CALL + ret
                    else:
                        return ReturnState.REDRAW + ReturnState.CALL
                else:
                    return ReturnState.REDRAW
    
    def draw(self, mousePos):
        r = pygame.Rect(*self.stackP(), *self.size)
        r.x += self.OHE
        r.y += self.OHE
        r.width -= self.OHE
        r.height -= self.OHE
        if not self.G.pause:
            if bool(mousePos) and r.collidepoint(*mousePos):
                if self.OHE != -1:
                    r.x -= self.OHE
                    r.y -= self.OHE
                    r.width += self.OHE*2
                    r.height += self.OHE*2
        if GLOBALTHEME.THEME.BUTTON is None:
            pygame.draw.rect(self.G.WIN, self.cols['BG'], r, border_radius=8)
        else:
            self.G.WIN.blit(GLOBALTHEME.THEME.BUTTON.get(), r)
        self.G.WIN.blit(self.TxtSur, (r.x + (r.width-self.TxtSur.get_width())/2, r.y + (r.height-self.TxtSur.get_height())/2))

class DropdownButton(Button): # TODO: Different button and dropdown colours
    def __init__(self, 
                 pos: GO.P___, 
                 opts: Iterable[str],
                 BGcol: GO.C___ = GO.CBLACK, 
                 TXTcol: GO.C___ = GO.CWHITE, 
                 Selectcol: GO.C___ = GO.CBLUE, 
                 format: str = '[{0}]',
                 default: int = 0,
                 font: GO.F___ = GO.FREGULAR,
                 spacing: int = 2,
                 func: Callable = lambda selected: None,
                 **settings
                ):
        """
        A button which when pressed allows you to change the selected element.

        Args:
            pos (GO.P___): The position of this element.
            opts (Iterable[str]): The options in the dropdown.
            BGcol (GO.C___, optional): The background colour of the button and dropdown. Defaults to GO.CBLACK.
            TXTcol (GO.C___, optional): The colour of the text and dropdown. Defaults to GO.CWHITE.
            Selectcol (GO.C___, optional): The colour of selected dropdown elements. Defaults to GO.CBLUE.
            format (str, optional): The format to display the selected element on on the button, {0} being the currently selected value. Defaults to '[{0}]'.
            default (int, optional): The default index into the opts list of which element is selected. Defaults to 0.
            font (GO.F___, optional): The font to use to render the text. Defaults to GO.FREGULAR.
            spacing (int, optional): The spacing between the text and the edge of the button/dropdown. Defaults to 2.
            func (_type_, optional): The function to call when a value is selected. Defaults to a do nothing func.
            \\*\\*settings: The settings for rendering the text. See `GUI.Button.__init__` or `GUI.Text.__init__` or `GO.F___.render` for more information.
        
        Useful Settings:
            allowed_width (int, optional): The maximum width of the text. Defaults to None.
        """
        self.opts = opts
        self._format = format
        self.actualuserfunc = func
        self.selected = default
        self.dropdown = None
        super().__init__(pos, BGcol, self.formatted, TXTcol, font, spacing, 0, self.onclick, **settings)
        self.cols.update({"SELECT": Selectcol})
    
    @property
    def formatted(self):
        return self._format.format(self.opts[self.selected])
    
    @property
    def linesize(self):
        return self.font.linesize + self.spacing*2
    
    def set(self, num, **settings):
        """Set the index of the current selected object (None = don't set) in the list of selected objects \
            and optionally some text render settings."""
        self.settings.update(settings)
        self.selected = num or self.get()
        self._set_txt(self.formatted)
    
    def get(self, index=False):
        """Get the current selected index or object."""
        if index:
            return self.selected
        else:
            return self.opts[self.selected]
    
    def actualfunc(self, resp):
        self.dropdown = None
        if resp is not None:
            self.selected = resp
            self._set_txt(self.formatted)
        self.actualuserfunc(resp)
    
    def onclick(self):
        x, y = self.stackP()
        self.dropdown = Dropdown((x, y+self.size[1]), 
                                 self.opts, 
                                 self.spacing, 
                                 self.font, 
                                 self.cols['BG'], 
                                 self.cols['TXT'],
                                 self.cols['SELECT'],
                                 False,
                                 self.size[0],
                                 self.actualfunc
        )
        self.dropdown.G = self.G
        self.dropdown._init2()
        self.dropdown._init2Ran = True

    def update(self, mousePos, events):
        resp = None
        if self.dropdown is not None:
            resp = self.dropdown.update(mousePos, events)
        super().update(mousePos, events)
        return resp

    def draw(self, mousePos):
        super().draw(mousePos)
        if self.dropdown is not None:
            self.dropdown.draw(mousePos)

def buildTransparencySur(size, squareSize=10):
    # The checked pattern
    s = pygame.Surface(size)
    s.fill((100, 100, 100))
    for x in range(0, size[0], squareSize):
        for y in range(0, size[1], squareSize):
            if (x//squareSize + y//squareSize) % 2 == 0:
                pygame.draw.rect(s, (200, 200, 200), (x, y, squareSize, squareSize))
    return s

class ImageViewer(Element):
    def __init__(self, pos: GO.P___, sur: pygame.Surface, size: Iterable[int]=(300, 300)):
        """
        A

        Args:
            pos (GO.P___): The position of this element.
            sur (pygame.Surface): The image to display.
            size (Iterable[int], optional): The size of the element in the Screen. Defaults to (300, 300).
        """
        super().__init__(pos, size)
        self._sur = sur
        self.scrollVel = 0
        self.lastMP = (0, 0)
        self.cache = None
        self.lastGPause = None
        self.centre()
    
    @property
    def sur(self):
        return self._sur
    
    @sur.setter
    def sur(self, newsur):
        self._sur = newsur
        self.cache = None
    
    def set(self, newsur):
        self.sur = newsur
        self.centre()
    
    def get(self):
        return self._sur
    
    def reset(self):
        self.scroll = 1
        self.offset = [self.size[0]/2, self.size[1]/2]
    
    def modifySur(self, sur):
        return sur
    
    def _modifySur(self, sur):
        if self.cache is None:
            self.cache = self.modifySur(sur.copy())
        return self.cache
    
    def centre(self):
        sur = self._modifySur(self._sur)
        if sur.get_size() == (0, 0):
            self.reset()
            return
        self.scroll = 1
        self.offset = [sur.get_width()/2, sur.get_height()/2]
        self.update_scroll(max(self.size) / max(sur.get_size()))
    
    def update_scroll(self, newscroll):
        if newscroll == self.scroll:
            return
        self.offset[0] *= abs(newscroll) / abs(self.scroll)
        self.offset[1] *= abs(newscroll) / abs(self.scroll)
        self.scroll = newscroll
    
    def unscale_pos(self, pos):
        thisP = self.stackP()
        pos = (pos[0] - thisP[0], pos[1] - thisP[1])
        return (pos[0] - self.size[0] / 2 + self.offset[0]) / self.scroll, (pos[1] - self.size[1] / 2 + self.offset[1]) / self.scroll
    
    def update(self, mousePos, events):
        pos = self.stackP()
        if not self.G.pause and pygame.Rect(*pos, *self.size).collidepoint(mousePos.pos):
            mouse.Mouse.set(mouse.MouseState.GRAB)
            scrolling = any(e.type == pygame.MOUSEWHEEL for e in events)
            for e in events:
                if e.type == pygame.MOUSEWHEEL:
                    self.scrollVel += e.y * 0.25
                    self.scrollVel += e.x * 0.25
                                
                elif not scrolling and e.type == pygame.MOUSEBUTTONDOWN:
                    self.lastMP = mousePos
                    self.lastGPause = self.G.pause
        if pygame.mouse.get_pressed()[0] and self.lastGPause is not None:
            mouse.Mouse.set(mouse.MouseState.GRAB)
            self.offset[0] -= mousePos.pos[0] - self.lastMP[0]
            self.offset[1] -= mousePos.pos[1] - self.lastMP[1]
            self.lastMP = mousePos.pos
            self.G.pause = True
        elif self.lastGPause is not None:
            self.G.pause = self.lastGPause
            self.lastGPause = None
        
        self.update_scroll(
            max(min(self.scroll + self.scrollVel, 10000), max(self.size) / 5000)
        )
        self.scrollVel = round(self.scrollVel * 0.7, 3)
        if abs(self.scrollVel) <= 0.003:
            self.scrollVel = 0

    def draw(self):
        sur = self._modifySur(self._sur)
        pos = self.stackP()

        # FIXME: Please. This code is the stupidest mess, and I have no clue why regular methods don't work.
        newSur = pygame.Surface((self.size[0]/self.scroll+2, self.size[1]/self.scroll+2), pygame.SRCALPHA)
        ox, oy = (self.size[0]/2-self.offset[0])/self.scroll, (self.size[1]/2-self.offset[1])/self.scroll
        newSur.blit(sur, (floor(ox)+1, floor(oy)+1))
        self.G.WIN.blit(
            buildTransparencySur(self.size), 
            pos
        )

        ox2, oy2 = (-ox % 1) * self.scroll, (-oy % 1) * self.scroll

        if ox2 == 0:
            ox2 = self.scroll
        if oy2 == 0:
            oy2 = self.scroll

        self.G.WIN.blit(
            pygame.transform.scale(newSur, (self.size[0] + 2 * self.scroll, self.size[1] + 2 * self.scroll)),
            pos,
            (ox2, oy2, *self.size)
        )
        pygame.draw.rect(self.G.WIN, GO.CGREY, (*pos, *self.size), 2)
