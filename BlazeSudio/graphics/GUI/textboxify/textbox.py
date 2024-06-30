"""This module contains classes for creating text boxes.

Both TextBox and TextBoxAdv are the same when it comes to print out
text inside a box on the screen. However, TextBox has less features than
TextBoxAdv.

TextBox is useful if you only want to print out text on the
screen without much configurations.

TextBoxAdv is useful if you want to design unique dialog boxes with certain
borders, backgrounds, portraits, indication symbols and animations.
"""


import string

import pygame

from . import settings
from .util import CustomSprite, fix_corners

from BlazeSudio.graphics.GUI.elements import Element, ReturnState
from BlazeSudio.graphics.options import TTEXTBOX

class TextBox(Element):
    type = TTEXTBOX
    """Class for creating simple text boxes.

    Args:
        G (BlazeGudio.Graphic.Graphic): The graphic screen to be on (required).
        pos (BlazeSudio.Graphic.P___): The position of the textbox on the screen (required).
        font (BlazeSudio.Graphic.F___): The font to render the text with (required).
        dist (int): The distance from the position to where you want the textbox to be (e.g. if you specified the position being at the bottom centre, then this would be the distance up from that point)
        padding (tuple): Space between text and edge
        speeds (tuple): The speeds of the text, in frames: (regular char speed, punctuation char speed).
        lines (int): Number of printed lines.
        text (str): Text to print.
        font_colour (tuple|BlazeSudio.Graphic.C___): Text colour, RGB value.
        text_wid (tuple): The maximum width of the text.
        bg_colour (tuple|BlazeSudio.Graphic.C___): Background colour, RGB value.
        transparent (bool): if the box should be transparent or have a background colour.

    """

    def __init__(
        self,
        G,
        pos,
        font,
        dist=20,
        padding=(10, 10),
        speeds=(2, 5),
        lines=2,
        text=None,
        font_colour=(255, 255, 255),
        text_wid=300,
        bg_colour=(0, 0, 0),
        transparent=False,
    ):
        self.linesize = font.linesize
        self.size = self._adjust((text_wid + padding[0] * 2, self.linesize * lines + padding[1] * 2), True)
        super().__init__(G, pos.copy(), self.size)

        self.full = False
        self.forceFull = False
        self.timer = 0

        if text:
            self.words = text
        else:
            self.words = ""
        self.printedWrds = ""
        
        self.speeds = speeds
        self.font = font
        self.padding = padding

        self.__dist = dist
        self.__font_colour = font_colour
        self.__text_wid = text_wid
        self.__lines = lines
        self.__bg_colour = (transparent, bg_colour)

    def set(self, text):
        """Set new text message to print out.

        Args:
            words (str): new text to print.
        """
        self.clear()
        self.words = text
    
    def get(self):
        """Returns a tuple: (Entire text, Text printed so far)"""
        return self.words, self.printedWrds
    
    def _adjust(self, position, typ):
        """Function used when setting a size or position that can be filled in for a subclass (e.g. to include a border)
        typ = False: is setting the position
        typ = True: is setting the size"""
        return position

    def clear(self):
        """Clears the dialog box, ready for new text to be filled"""
        self.words = self.words[len(self.printedWrds):]
        self.timer = 0
        self.printedWrds = ""
        self.full = False
        self.forceFull = False

    def update(self, mousePos, events):
        sur = pygame.Surface(self.size)
        if self.__bg_colour[0]:
            sur.fill(self.__bg_colour[1])
        else:
            sur.fill((255, 255, 255, 1))
        
        if not self.words:
            self.full = True
        
        if not self.full:
            self.timer += 1
            nxtChar = self.words[len(self.printedWrds)]
            doNext = False
            if nxtChar in string.punctuation:
                if self.timer >= self.speeds[1]:
                    doNext = True
            else:
                if self.timer >= self.speeds[0]:
                    doNext = True
            if doNext or self.forceFull:
                _, lines = self.font.render(self.printedWrds + self.words[len(self.printedWrds)], 0, allowed_width=self.__text_wid-(self.padding[0]//2), verbose=True)
                if lines <= self.__lines:
                    self.timer = 0
                    self.printedWrds += self.words[len(self.printedWrds)]
                    if len(self.printedWrds) >= len(self.words):
                        self.full = True
                else:
                    self.full = True
        
        if self.full:
            self.forceFull = False
        
        outSur = self.font.render(self.printedWrds, self.__font_colour, allowed_width=self.__text_wid-self.padding[0])
        
        x, y = self.stackP()
        pygame.draw.rect(self.G.WIN, self.__bg_colour[1], (*self._adjust((x, y), False), *self._adjust(self.size, True)))
        self.G.WIN.blit(outSur, self._adjust((x + self.padding[0], y + self.__dist + self.padding[1]), False))
        
        for ev in events:
            if ev.type == pygame.MOUSEBUTTONDOWN or \
               ev.type == pygame.KEYDOWN and (
                   ev.key == pygame.K_RETURN or \
                   ev.key == pygame.K_SPACE
               ):
                if not self.full:
                    self.forceFull = True
                else:
                    if len(self.printedWrds) < len(self.words):
                        self.clear()
                    else:
                        return ReturnState.CALL
    
    def remove(self):
        self.G.pause = False
        super().remove()


class TextBoxAdv(TextBox):
    """Class for creating customizable dialog boxes.

    Args:
        G (BlazeGudio.Graphic.Graphic): The graphic screen to be on (required).
        pos (BlazeSudio.Graphic.P___): The position of the textbox on the screen (required).
        font (BlazeSudio.Graphic.F___): The font to render the text with (required).
        dist (int): The distance from the position to where you want the textbox to be (e.g. if you specified the position being at the bottom centre, then this would be the distance up from that point)
        padding (tuple): The spacing between the border of the box and the text itself.
        portrait_padding (tuple): The padding between the border and the portrait and the text (border to portrait x, border to portrait y, portrait to text x)
        speeds (tuple): The speeds of the text, in frames: (regular char speed, punctuation char speed).
        lines (int): Number of printed lines.
        text (str): Text to print.
        font_colour (tuple|BlazeSudio.Graphic.C___): Text colour, RGB value.
        text_wid (int): Max width of the printed text.
        bg_colour (tuple|BlazeSudio.Graphic.C___): Background colour, RGB value.
        border (dict): Border sprite settings.
        transparent (bool): if the box should be transparent or have a background colour.

    """

    def __init__(
        self,
        G,
        pos,
        font,
        dist=20,
        padding=(10, 10),
        portrait_padding=(10, 10, 10),
        speeds=(2, 5),
        lines=2,
        text=None,
        font_colour=(255, 255, 255),
        text_wid=200,
        bg_colour=(0, 0, 0),
        border=None,
        transparent=False,
    ):
        super().__init__(
            G,
            pos,
            font,
            dist,
            padding,
            speeds,
            lines,
            text,
            font_colour,
            text_wid,
            bg_colour,
            transparent
        )
        self.portrait_padding = portrait_padding

        self.__indicator = None
        self.__portrait = None
        self.__border = border

        # Always check if border evaluate to true because corner and side
        # doesn't get created when there isn't any border to draw.
        if self.__border:
            # Create topleft corner sprite.
            self.__corner = CustomSprite(
                self.__border["corner"],
                self.__border["size"],
                self.__border["colorkey"],
            )

            # Create left side sprite.
            self.__side = CustomSprite(
                self.__border["side"],
                self.__border["size"],
                self.__border["colorkey"]
            )

    def set_indicator(self, sprite=None, size=None, colorkey=None, scale=None):
        """Initilize animated idle symbol.

        Note:
            If sprite is ommited, the default indicator
            will be used and all other arguments will be ignored.

        Args:
            sprite (str): path to sprite file.
            size (tuple): width, height of sprite frame.
            colorkey (tuple): colour to remove from sprite, RGB value.
            scale (tuple): new width, height to scale sprite to.
        """

        if sprite:
            self.__indicator = CustomSprite(sprite, size, colorkey, scale)
        else:
            self.__indicator = CustomSprite(
                settings.DEFAULT_INDICATOR["file"],
                settings.DEFAULT_INDICATOR["size"],
                (0, 0, 0),
            )

    def set_portrait(self, sprite=None, size=None, colorkey=None):
        """Initilize portrait image on the left side of the text.

        Note:
            The sprite will be scaled to be the same size as the total
            height of the text line limit.

        Note:
            If sprite is ommited, a default placeholder animation
            will be used and all other arguments will be ignored.

        Args:
            sprite (str): path to sprite file.
            size (tuple): width, height of sprite frame.
            colorkey (tuple): colour to remove from sprite, RGB value.
            scale (tuple): new width, height to scale sprite to.

        """

        # Set portrait to have the same height as the text lines.
        scale = [self.__textbox.linesize * self.__lines] * 2

        # Set custom sprite for portrait.
        if sprite:

            # Shut down if no size.
            if not size:
                raise SystemExit("Error: Need to give a size for the portrait sprite.")

            self.__portrait = CustomSprite(sprite, size, colorkey, scale)

        # Use default portrait sprite.
        else:
            self.__portrait = CustomSprite(
                file=settings.DEFAULT_PORTRAIT["file"],
                size=settings.DEFAULT_PORTRAIT["size"],
                colorkey=(241, 0, 217),
                scale=scale,
            )

        # Adjust box text to the portrait.
        w = self.__portrait.width + self.__text_width + self.__padding[0]
        h = self.size[1]
        size = (w, h)

        # Update textbox data with portrait implemented.
        pos = self.rect.topleft
        self.size = self._adjust(size, self.__side) if self.__border else size
        self.image = pygame.Surface(self.size).convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, mousePos, events):
        # Update the text.
        ret = super().update(mousePos, events)
        
        x, y = self.stackP()

        if self.full and self.__indicator:
            self.__indicator.animate(pygame.time.get_ticks())
            im = self.__indicator.image
            self.G.WIN.blit(im, (x + self.size[0] - (self.padding[0] // 2) - im.get_width(), y + self.size[1] - (self.padding[1] // 2) - im.get_height()))
        
        # Draw portrait

        # Draw box border.
        # if self.__border:
        #     self._draw_border(
        #         self.image,
        #         self.__border,
        #         self.__corner,
        #         self.__side,
        #         self.__bg_colour,
        #     )
        return ret

    def _adjust(self, size, typ):
        """Include the border size and portrait"""
        return size

        w = size[0] - size[0] % side.width
        h = size[1] - size[1] % side.height

        return (w, h)

    def _blit_border(self, src, dest, blocks, type):
        """Draw the borders of the dialog box."""

        src_w, src_h = src.get_size()
        dest_w, dest_h = dest.get_size()

        if type == "CORNER":
            dest.blit(blocks["TOP_LEFT"], (0, 0))
            dest.blit(blocks["TOP_RIGHT"], (dest_w - src_w, 0))
            dest.blit(blocks["BOTTOM_LEFT"], (0, dest_h - src_h))
            dest.blit(blocks["BOTTOM_RIGHT"], (dest_w - src_w, dest_h - src_h))

        elif type == "SIDE":
            # Left & right side
            for block in range(1, dest_h // src_h - 1):
                dest.blit(blocks["LEFT"], (0, 0 + src_h * block))
                dest.blit(blocks["RIGHT"], (dest_w - src_w, 0 + src_h * block))

            # Top & bottom side
            for block in range(1, dest_w // src_h - 1):
                dest.blit(blocks["TOP"], (0 + src_w * block, 0))
                dest.blit(blocks["BOTTOM"], (0 + src_w * block, dest_h - src_h))

    def _draw_content(self, surface, text, portrait, padding):
        """Draw box text and portrait."""

        if portrait:
            portrait.animate(pygame.time.get_ticks())
            pos = (padding[0] - 10, padding[1])
            surface.blit(portrait.image, pos)

            # Draw new text.
            surface.blit(text.image, (padding[0] + portrait.width, padding[1]))
        else:
            surface.blit(text.image, padding)

    def _draw_border(self, surface, border, corner, side, bg_colour):
        """Draws the border and then fixes the corners if needed."""

        blocks = self._rotate_border_blocks(corner, side)

        # Animation is turned on.
        if border["animate"]:
            corner.animate(pygame.time.get_ticks())
            side.animate(pygame.time.get_ticks())
            self._blit_border(corner.image, surface, blocks, "CORNER")
            self._blit_border(side.image, surface, blocks, "SIDE")

        # Border is not going to have animation.
        else:
            self._blit_border(corner.image, surface, blocks, "CORNER")
            self._blit_border(side.image, surface, blocks, "SIDE")

        # Make pixels outside rounded corners transparent.
        fix_corners(
            surface=surface,
            corner_size=corner.size,
            bg_colour=bg_colour,
            colorkey=border["colorkey"],
        )

    def _rotate_border_blocks(self, corner, side):
        """Return dictionary with rotated border sprites."""

        blocks = {
            "TOP_LEFT": corner.image,
            "TOP_RIGHT": pygame.transform.rotate(corner.image, -90),
            "BOTTOM_LEFT": pygame.transform.rotate(corner.image, 90),
            "BOTTOM_RIGHT": pygame.transform.rotate(corner.image, 180),
            "LEFT": side.image,
            "TOP": pygame.transform.rotate(side.image, -90),
            "BOTTOM": pygame.transform.rotate(side.image, 90),
            "RIGHT": pygame.transform.rotate(side.image, 180),
        }
        return blocks
