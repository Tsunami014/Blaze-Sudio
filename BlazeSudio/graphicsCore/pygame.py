from BlazeSudio.graphicsCore import Surface
from typing import Iterable, overload

# This is so you can use 'graphicsCore.draw.line' in replacement of pygame's 'pygame.draw.line'
__all__ = [
    'draw'
]

class draw:
    def __new__(cls):
        raise NotImplementedError(
            'Do not instance this class! Instead, call the class functions.'
        )

    @staticmethod
    def line(sur: Surface, col: int, start_pos: Iterable[int|float], end_pos: Iterable[int|float], width: int|float = 1):
        """
        Draw a line

        Args:
            sur (BlazeSudio.Surface): The surface to draw a line on
            col (int): The colour of the line
            start_pos (Iterable[int | float]): The starting point of the line
            end_pos (Iterable[int | float]): The ending point of the line
            width (int | float): The thickness of the line. Must be > 0. Defaults to 1.
        """
        sur.drawLine(start_pos, end_pos, width, col)

    @staticmethod
    def polygon(sur: Surface, col: int, ps: Iterable[Iterable[int|float]], width: int|float = 0):
        """
        Draw a closed polygon

        Args:
            sur (BlazeSudio.Surface): The surface to draw a line on
            col (int): The colour of the line
            ps (Iterable[Iterable[int | float]]): The points making up the polygon
            width (int | float): The thickness of the line. Must be > 0. Defaults to 0.
        """
        sur.drawPolygon(ps, width, col)

    @staticmethod
    def rect(sur: Surface, col: int, rect: Iterable[int|float], width: int|float = 0, /, border_radius: int|float = 0):
        """
        Draws a rectangle

        Args:
            sur: The surface to draw a line on
            x: The x position of the rect
            y: The y position of the rect
            width: The width of the rect
            height: The height of the rect
            width: The thickness of the rect. If == 0, will fill the entire rect. Must be >= 0.
            col: The colour of the rect

        Keyword args:
            roundness: The roundness of the rect. 0 = ends of lines rounded, >0 = ends rounded by that many pixels, <0 = do not round the lines at all
        """
        sur.drawRect((rect[0], rect[1]), (rect[2], rect[3]), width, col, roundness=border_radius)

    @staticmethod
    def circle(sur: Surface, col: int, center: Iterable[int|float], radius: int|float, width: int|float = 0):
        """
        Draws a circle!

        Args:
            sur: The surface to draw a line on
            col: The colour to fill the circle with
            center: The position of the circle
            radius: The radius of the circle
            width: The thickness of the circle. If == 0, will fill the circle entirely. Must be >= 0.
        """
        sur.drawCircle(center, radius, width, col)

# TODO: Draw methods for elipse (I'm not bothered rn)
