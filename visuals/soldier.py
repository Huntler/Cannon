from visuals.sprite import Sprite
from cannon.cannon import CannonGame
from typing import Tuple
import pygame as py
from pygame.constants import MOUSEBUTTONUP


class Soldier(Sprite):
    SIZE = 10
    DARK = (100, 150, 0)
    LIGHT = (240, 50, 0)
    CLICKED = py.event.custom_type()

    def __init__(self, surface, board_dim, border_dim, pos, type) -> None:
        self._callbacks = dict()

        # set the correct type and color
        self._type = type
        if CannonGame.LIGHT == self._type:
            self._color = Soldier.LIGHT
        elif CannonGame.DARK == self._type:
            self._color = Soldier.DARK

        # set position
        self._x_pos, self._y_pos = pos
        self._board_dim = board_dim
        self._border_dim = border_dim
        self._x, self._y = Soldier._to_pixel(
            (self._x_pos, self._y_pos), self._board_dim, self._border_dim)

        self._surface = surface
        super().__init__()

    def active(self, val: bool) -> None:
        self._active = val

    def draw(self):
        pos = (self._x, self._y)
        size = Soldier.SIZE

        if self._active and self.collidepoint(py.mouse.get_pos()):
            size *= 1.2

            if py.mouse.get_pressed()[0] and Soldier.CLICKED in self._callbacks.keys():
                for func in self._callbacks[Soldier.CLICKED]:
                        self._board_state = func(Soldier.CLICKED, self)

        py.draw.circle(self._surface, self._color, pos, size)

    def set_position(self, pos: Tuple[int, int]) -> None:
        self._x_pos, self._y_pos = pos
        self._x, self._y = Soldier._to_pixel(
            (self._x_pos, self._y_pos), self._board_dim, self._border_dim)
    
    def get_position(self) -> Tuple[int, int]:
        return (self._x_pos, self._y_pos)
    
    def callback(self, event_type, func) -> None:
        if event_type not in self._callbacks.keys():
            self._callbacks[event_type] = []

        self._callbacks[event_type].append(func)

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        _x, _y = point

        if _x > self._x - Soldier.SIZE and _x < self._x + Soldier.SIZE:
            if _y > self._y - Soldier.SIZE and _y < self._y + Soldier.SIZE:
                return True

        return False

    @staticmethod
    def _to_pixel(pos: Tuple[int, int], board_dim: Tuple[int, int], border_dim: Tuple[int, int]) -> Tuple[int, int]:
        w, h = board_dim
        xb, yb = border_dim
        sc = w / Soldier.SIZE
        x, y = pos
        return x * sc + xb + sc / 2, h - y * sc + yb - sc / 2
