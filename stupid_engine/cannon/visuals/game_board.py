from stupid_engine.backend.visuals.font import Font
import pygame as py


class Board:

    FOREGROUND = (255, 235, 200)
    BACKGROUND = (20, 15, 0)

    LINES = (150, 100, 0)
    FONT_COLOR = (255, 255, 255)
    FONT_SIZE = 12
    FONT = None

    VERT_NAMES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    HORIN_NAMES = ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]

    def __init__(self, screen, screen_dim, font: str = Font.COMIC_SANS) -> None:
        self._screen = screen
        self._width, self._height, self._x_border, self._y_border = screen_dim
        self._grid_size = 10

        # init the font
        py.font.init()
        self._font = py.font.SysFont(font, Board.FONT_SIZE)
    
    def draw(self):
        scaling = self._width / self._grid_size
        py.draw.rect(self._screen, Board.BACKGROUND,
                     (0, 0, self._width + 2 * self._x_border, self._height + 2 * self._y_border))
        py.draw.rect(self._screen, Board.FOREGROUND, (self._x_border + scaling / 2,
                     self._y_border + scaling / 2, self._width - scaling, self._height - scaling))

        # draw the board lines and the board notations
        dist = self._width / 10
        for vert in range(0, 10):
            # draw the line
            x = self._x_border + vert * dist + scaling / 2
            py.draw.line(self._screen, Board.LINES, (x, self._y_border + scaling / 2),
                         (x, self._y_border + self._height - scaling / 2))

            # draw the text A-Z above and below the board
            text = self._font.render(
                Board.VERT_NAMES[vert], False, Board.FONT_COLOR)
            self._screen.blit(text, (x - Board.FONT_SIZE / 2,
                         self._y_border - Board.FONT_SIZE / 2))
            self._screen.blit(text, (x - Board.FONT_SIZE / 2, self._y_border + self._height))

        for horin in range(0, 10):
            # draw the horizontal lines
            y = self._y_border + horin * dist + scaling / 2
            py.draw.line(self._screen, Board.LINES, (self._x_border + scaling / 2, y),
                         (self._x_border + self._width - scaling / 2, y))

            # draw the text 1-10 next to the board
            text = self._font.render(
                Board.HORIN_NAMES[horin], False, Board.FONT_COLOR)
            self._screen.blit(text, (self._x_border - Board.FONT_SIZE /
                         2, y - Board.FONT_SIZE / 2))
            self._screen.blit(text, (self._x_border + self._width, y - Board.FONT_SIZE / 2))
