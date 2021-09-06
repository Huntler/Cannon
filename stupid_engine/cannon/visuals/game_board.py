from stupid_engine.backend.visuals.font import Font
import pygame as py


class Board:

    VERT_NAMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    HORIN_NAMES = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]

    def __init__(self, screen, screen_dim, grid_size: int = 10, font: str = Font.ARIAL, font_size: int = 12) -> None:
        self._screen = screen
        self._width, self._height, self._x_border, self._y_border = screen_dim
        self._grid_size = 10

        self._background = (20, 15, 0)
        self._foreground = (255, 235, 200)
        self._line_color = (150, 100, 0)

        self._font_size = font_size
        self._font_color = (255, 255, 255)

        # init the font
        py.font.init()
        self._font = py.font.SysFont(font, self._font_size)
    
    def set_color(self, background, foreground, font_color, line_color) -> None:
        self._background = background
        self._foreground = foreground
        self._line_color = font_color
        self._font_color = line_color
    
    def draw(self):
        scaling = self._width / self._grid_size
        py.draw.rect(self._screen, self._background,
                     (0, 0, self._width + 2 * self._x_border, self._height + 2 * self._y_border))
        py.draw.rect(self._screen, self._foreground, (self._x_border + scaling / 2,
                     self._y_border + scaling / 2, self._width - scaling, self._height - scaling))

        # draw the board lines and the board notations
        dist = self._width / 10
        for vert in range(0, 10):
            # draw the line
            x = self._x_border + vert * dist + scaling / 2
            py.draw.line(self._screen, self._line_color, (x, self._y_border + scaling / 2),
                         (x, self._y_border + self._height - scaling / 2))

            # draw the text A-Z above and below the board
            text = self._font.render(
                Board.VERT_NAMES[vert], False, self._font_color)
            self._screen.blit(text, (x - self._font_size / 2,
                         self._y_border - self._font_size / 2))
            self._screen.blit(text, (x - self._font_size / 2, self._y_border + self._height))

        for horin in range(0, 10):
            # draw the horizontal lines
            y = self._y_border + horin * dist + scaling / 2
            py.draw.line(self._screen, self._line_color, (self._x_border + scaling / 2, y),
                         (self._x_border + self._width - scaling / 2, y))

            # draw the text 1-10 next to the board
            text = self._font.render(
                Board.HORIN_NAMES[horin], False, self._font_color)
            self._screen.blit(text, (self._x_border - self._font_size /
                         2, y - self._font_size / 2))
            self._screen.blit(text, (self._x_border + self._width, y - self._font_size / 2))
