import pygame as py


class Soldier:
    SIZE = 10
    DARK = (100, 150, 0)
    LIGHT = (240, 50, 0)

    LIGHTEN = (15, 15, 15)

    @staticmethod
    def draw(surface, x_pos, y_pos, color):
        x = x_pos
        y = y_pos
        size = Soldier.SIZE

        if Soldier.is_hovering(x, y):
            color = (color[0] + Soldier.LIGHTEN[0], color[1] +
                     Soldier.LIGHTEN[1], color[2] + Soldier.LIGHTEN[2])
            size *= 1.2
        py.draw.circle(surface, color, (x, y), size)

    @staticmethod
    def is_hovering(x, y) -> bool:
        x_mouse, y_mouse = py.mouse.get_pos()

        if x_mouse > x - Soldier.SIZE and x_mouse < x + Soldier.SIZE:
            if y_mouse > y - Soldier.SIZE and y_mouse < y + Soldier.SIZE:
                return True

        return False
