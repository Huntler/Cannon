from visuals.soldier import Soldier
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

    @staticmethod
    def init_font():
        py.font.init()
        # e.g. Comic Sans MS
        Board.FONT = py.font.SysFont('Arial', Board.FONT_SIZE)

    @staticmethod
    def draw(surface, width, height, x_border, y_border, scaling):
        py.draw.rect(surface, Board.BACKGROUND,
                     (0, 0, width + 2 * x_border, height + 2 * y_border))
        py.draw.rect(surface, Board.FOREGROUND, (x_border + scaling / 2,
                     y_border + scaling / 2, width - scaling, height - scaling))

        # draw the board lines and the board notations
        dist = width / 10
        for vert in range(0, 10):
            # draw the line
            x = x_border + vert * dist + scaling / 2
            py.draw.line(surface, Board.LINES, (x, y_border + scaling / 2),
                         (x, y_border + height - scaling / 2))

            # draw the text A-Z above and below the board
            text = Board.FONT.render(
                Board.VERT_NAMES[vert], False, Board.FONT_COLOR)
            surface.blit(text, (x - Board.FONT_SIZE / 2,
                         y_border - Board.FONT_SIZE / 2))
            surface.blit(text, (x - Board.FONT_SIZE / 2, y_border + height))

        for horin in range(0, 10):
            # draw the horizontal lines
            y = y_border + horin * dist + scaling / 2
            py.draw.line(surface, Board.LINES, (x_border + scaling / 2, y),
                         (x_border + width - scaling / 2, y))

            # draw the text 1-10 next to the board
            text = Board.FONT.render(
                Board.HORIN_NAMES[horin], False, Board.FONT_COLOR)
            surface.blit(text, (x_border - Board.FONT_SIZE /
                         2, y - Board.FONT_SIZE / 2))
            surface.blit(text, (x_border + width, y - Board.FONT_SIZE / 2))
