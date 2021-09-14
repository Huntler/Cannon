from typing import Tuple
from stupid_engine.backend.visuals.font import Font
import pygame as py


class Board:

    VERT_NAMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    HORIN_NAMES = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]

    def __init__(self, screen, window_size, draw_area, grid_size: int = 10, font: str = Font.ARIAL, font_size: int = 24) -> None:
        self._grid_size = grid_size
        self._screen = screen

        self._background = (20, 15, 0)
        self._foreground = (255, 235, 200)
        self._line_color = (150, 100, 0)

        self._font_size = font_size
        self._font_color = (255, 255, 255)

        w, h = self._window_size = window_size
        wd, hd = self._draw_area = draw_area

        self._x = int((w - wd) / 2)
        self._y = int((h - hd) / 2)
        self._w = wd
        self._h = hd

        self._scaling = wd / self._grid_size

        # init the font
        py.font.init()
        self._font = py.font.SysFont(font, self._font_size)
    
    def set_color(self, background, foreground, font_color, line_color) -> None:
        self._background = background
        self._foreground = foreground
        self._line_color = font_color
        self._font_color = line_color
    
    def get_draw_area(self) -> Tuple[int, int, int, int]:
        return self._x, self._y, self._w, self._h
    
    def draw(self):
        # drawing the background color over the whole screen
        py.draw.rect(self._screen, self._background, (0, 0) + self._window_size)

        # draw the board itself
        py.draw.rect(self._screen, self._foreground, (self._x, self._y, self._w, self._h))

        # draw the board lines and the board notations
        dist = self._scaling
        for vert in range(0, self._grid_size):
            # calculate the x coordinate and start / end y coordinates
            x = self._x + vert * dist + dist / 2
            y_start = self._y + dist / 2
            y_end = self._y + self._h - dist / 2

            # draw the line
            py.draw.line(self._screen, self._line_color, (x, y_start), (x, y_end), 2)

            # draw the text A-Z above and below the board
            text = self._font.render(Board.VERT_NAMES[vert], False, self._font_color)

            self._screen.blit(text, (x - self._font_size / 2, y_start - self._font_size * 4))
            self._screen.blit(text, (x - self._font_size / 2, y_end + self._font_size * 3))

        for horin in range(0, self._grid_size):
            # calculate the y coordinate and start / end x coordinates
            y = self._y + horin * dist + dist / 2
            x_start = self._x + dist / 2
            x_end = self._x + self._w - dist / 2

            # draw the horizontal lines
            py.draw.line(self._screen, self._line_color, (x_start, y), (x_end, y), 2)

            # draw the text 1-10 next to the board
            text = self._font.render(Board.HORIN_NAMES[horin], False, self._font_color)

            self._screen.blit(text, (x_start - self._font_size * 4, y - self._font_size / 2))
            self._screen.blit(text, (x_end + self._font_size * 3, y - self._font_size / 2))
