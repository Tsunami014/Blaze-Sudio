import pygame
from typing import Callable
from string import printable
from BlazeSudio.graphics import mouse, options as GO
from BlazeSudio.graphics.GUI.base import Element, ReturnState
from BlazeSudio.graphics.GUI.theme import GLOBALTHEME
from BlazeSudio.graphics.GUI.events import Dropdown

__all__ = [
    'Switch',
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
        mcollides = pygame.Rect(x, y, *self.size).collidepoint(mousePos)
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
    
    def get(self):
        """Get the state of the switch (on or off)"""
        return self.state
    def set(self, newState):
        """Set the state of the switch (on or off)"""
        self.state = newState

# InputBoxes code modified from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame 

# TODO: A text cursor
class InputBox(Element): # TODO: Change colours
    type = GO.TINPUTBOX
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 width: int, 
                 resize: GO.R___ = GO.RWIDTH, 
                 placeholder: str = 'Type here!', 
                 font: GO.F___ = GO.FSMALL, 
                 maxim: int = None, 
                 weight: GO.SW__ = GO.SWMID,
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
        self._force_placeholder_col = False

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
        if self._force_placeholder_col:
            txtcol = GO.CINACTIVE
        self.txt_surface = self.font.render(txt, txtcol, leftrightweight=self.weight, allowed_width=(None if self.resize == GO.RWIDTH else self.size[0] - 5), renderdash=self.renderdash)
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
            mcollide = pygame.Rect(*self.stackP(), *self.size).collidepoint(mousePos)
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
        # Blit the text.
        x, y = self.stackP()
        self.G.WIN.blit(self.txt_surface, (x+5+((self.size[0]-10)-self.txt_surface.get_width())*self.weight.w, y+5))
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
                 placeholder: str = 'Type number here!',
                 placeholdOnNum: None|bool|int = False
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
            placeholder (str, optional): The placeholder text visible when there is no text in the box. Defaults to 'Type number here!'.
            placeholdOnNum (bool|int, optional): **True** = show the placeholder on original number, \
                **False** = only show the placeholder once before you input your first number, \
                **None** = don't show the placeholder ever \
                **int** = show the placeholder if the number is equal to this int. Defaults to False.
        """
        super().__init__(G, pos, width, resize, placeholder, font, None, starting_text=str(start))
        if isinstance(placeholdOnNum, bool):
            if placeholdOnNum:
                self.placehold = start
            else:
                self.placehold = True
        elif placeholdOnNum is None:
            self.placehold = False
        else:
            self.placehold = placeholdOnNum
        self.empty = True
        self.emptyValue = start
        self.realnum = start
        self.limits = (min, max)
        self.renderdash = False
        self.fix()
        self._render_txt()
    
    def get(self, noneIfEmpty=False):
        """Get the number in the numbox, optionally returning None if the textbox is empty (default False)"""
        if noneIfEmpty and self.empty:
            return None
        return self.realnum

    def set(self, newNum):
        """Set the number in the numbox"""
        self.realnum = newNum

    def _handle_text(self, event):
        if event.key == pygame.K_BACKSPACE:
            if self.empty:
                return
            # if str(self.realnum)[:-1].endswith('.'):
            #     self.realnum = int(self.realnum)
            # else:
            if len(str(self.realnum)) == 1:
                self.realnum = self.emptyValue
                self.empty = True
            else:
                try:
                    self.realnum = int(str(self.realnum)[:-1])
                except:
                    self.realnum = 0
        elif event.key == pygame.K_MINUS:
            if self.empty:
                self.empty = False
            self.realnum = self.realnum * -1
        else:
            if event.unicode in '0123456789':
                if self.empty:
                    self.realnum = int(event.unicode)
                else:
                    self.realnum = int(str(self.realnum) + event.unicode)
                self.empty = False
                if self.placehold is True:
                    self.placehold = False
            # elif event.unicode == '.':
            #     self.realnum = float(self.realnum)
        self.fix()
    
    def fix(self):
        self.realnum = max(min(self.realnum, self.limits[1]), self.limits[0])
        self._force_placeholder_col = self.empty
        if self.placehold is self.realnum or self.placehold is True:
            self.text = ''
        else:
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

        self._set_txt(txt) # Sets self.txt and generates self.TxtSur
        super().__init__(G, pos, self.size)
    
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
    
    def update(self, mousePos, events, force_draw=False):
        r = pygame.Rect(*self.stackP(), *self.size)
        r.x += self.OHE
        r.y += self.OHE
        r.width -= self.OHE
        r.height -= self.OHE
        if not self.G.pause:
            if r.collidepoint(mousePos):
                if pygame.mouse.get_pressed()[0]:
                    mouse.Mouse.set(mouse.MouseState.CLICKING)
                else:
                    mouse.Mouse.set(mouse.MouseState.HOVER)
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
        if GLOBALTHEME.THEME.BUTTON is None:
            pygame.draw.rect(self.G.WIN, self.cols['BG'], r, border_radius=8)
        else:
            self.G.WIN.blit(GLOBALTHEME.THEME.BUTTON.get(), r)
        self.G.WIN.blit(self.TxtSur, (r.x + (r.width-self.TxtSur.get_width())/2, r.y + (r.height-self.TxtSur.get_height())/2))

class DropdownButton(Button): # TODO: Different button and dropdown colours
    def __init__(self, 
                 G, 
                 pos: GO.P___, 
                 opts: list[str],
                 BGcol: GO.C___ = GO.CBLACK, 
                 TXTcol: GO.C___ = GO.CWHITE, 
                 Selectcol: GO.C___ = GO.CBLUE, 
                 format: str = '[{0}]',
                 default: int = 0,
                 font: GO.F___ = GO.FFONT,
                 spacing: int = 2,
                 func: Callable = lambda selected: None,
                 **settings
                ):
        self.opts = opts
        self._format = format
        self.actualuserfunc = func
        self.selected = default
        self.dropdown = None
        super().__init__(G, pos, BGcol, self.formatted, TXTcol, font, spacing, 0, self.onclick, **settings)
        self.cols.update({"SELECT": Selectcol})
    
    @property
    def formatted(self):
        return self._format.format(self.opts[self.selected])
    
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
        self.dropdown = Dropdown(self.G, 
                                 (x, y+self.size[1]), 
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

    def update(self, mousePos, events, force_draw=False):
        resp = None
        if self.dropdown is not None:
            resp = self.dropdown.update(mousePos, events, force_draw)
        if super().update(mousePos, events, False) is not None:
            super().update(mousePos, events, True)
        
        return resp

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
    def __init__(self, G, pos, sur, size=(300, 300)):
        super().__init__(G, pos, size)
        self.sur = sur
        self.lastMP = (0, 0)
        self.centre()
    
    def reset(self):
        self.scroll = 1
        self.offset = [self.size[0]/2, self.size[1]/2]
    
    def centre(self):
        if self.sur.get_size() == (0, 0):
            self.reset()
            return
        self.scroll = 1
        self.offset = [self.sur.get_width()/2, self.sur.get_height()/2]
        self.update_scroll(max(self.size) / max(self.sur.get_size()))
    
    def update_scroll(self, newscroll):
        self.offset[0] *= abs(newscroll) / abs(self.scroll)
        self.offset[1] *= abs(newscroll) / abs(self.scroll)
        self.scroll = newscroll
    
    def unscale_pos(self, pos):
        thisP = self.stackP()
        pos = (pos[0] - thisP[0], pos[1] - thisP[1])
        return (pos[0] - self.size[0] / 2 + self.offset[0]) / abs(self.scroll), (pos[1] - self.size[1] / 2 + self.offset[1]) / abs(self.scroll)
    
    def update(self, mousePos, events, overrideSur=None):
        if overrideSur is not None:
            sur = overrideSur
        else:
            sur = self.sur
        pos = self.stackP()
        if not self.G.pause and pygame.Rect(*pos, *self.size).collidepoint(mousePos):
            mouse.Mouse.set(mouse.MouseState.GRAB)
            scrolling = any(e.type == pygame.MOUSEWHEEL for e in events)
            for e in events:
                if e.type == pygame.MOUSEWHEEL:
                    self.update_scroll(self.scroll + e.y*0.05)
                
                elif not scrolling and e.type == pygame.MOUSEBUTTONDOWN:
                    self.lastMP = mousePos
            if pygame.mouse.get_pressed()[0]:
                self.offset[0] -= mousePos[0] - self.lastMP[0]
                self.offset[1] -= mousePos[1] - self.lastMP[1]
                self.lastMP = mousePos
        newSur = pygame.Surface((self.size[0]/abs(self.scroll), self.size[1]/abs(self.scroll)), pygame.SRCALPHA)
        newSur.blit(sur, ((self.size[0]/2-self.offset[0])/abs(self.scroll), (self.size[1]/2-self.offset[1])/abs(self.scroll)))
        self.G.WIN.blit(
            buildTransparencySur(self.size), 
            pos
        )
        self.G.WIN.blit(
            pygame.transform.scale(newSur, self.size), 
            pos
        )
        pygame.draw.rect(self.G.WIN, GO.CGREY, (*pos, *self.size), 2)
