from stupid_engine.cannon.entities.cannon import CannonGame
from stupid_engine.backend.visuals.sprite import Sprite, to_pixel
from stupid_engine.backend.visuals.board import Board
from typing import Tuple
import pygame as py


SIZE = Board.GRID_SIZE


class Soldier(Sprite):

    DARK = (100, 150, 0)
    LIGHT = (240, 50, 0)
    CLICKED = py.event.custom_type()

    def __init__(self, surface, board_dim, border_dim, pos, color) -> None:
        """
        This class represents a soldier visually. Given on the position, the actual 
        pixel position on screen is calulated. The type determines the drawn color.
        """
        self._callbacks = dict()

        # set color
        self._color = color

        # set position
        self._x_pos, self._y_pos = pos
        self._board_dim = board_dim
        self._border_dim = border_dim
        self._x, self._y = to_pixel(
            (self._x_pos, self._y_pos), self._board_dim, self._border_dim)

        self._surface = surface
        super().__init__()

    def active(self, val: bool) -> None:
        """
        Only active sprites can call the hover and click event.
        """
        self._active = val

    def draw(self):
        """
        This method draws this sprite on the screen at the calulated position. If 
        the sprite is active, then the hover and click events will be handled in here.
        """
        super().draw()

        pos = (self._x, self._y)
        size = SIZE

        if self._active and self.collidepoint(py.mouse.get_pos()):
            size *= 1.2

        py.draw.circle(self._surface, self._color, pos, size)

    def set_position(self, pos: Tuple[int, int]) -> None:
        """
        This method sets the new position and calculates the pixel position on screen.
        """
        self._x_pos, self._y_pos = pos
        self._x, self._y = to_pixel(
            (self._x_pos, self._y_pos), self._board_dim, self._border_dim)

    def get_position(self) -> Tuple[int, int]:
        """
        This method returns the position for the game to work.
        """
        return (self._x_pos, self._y_pos)

    def callback(self, event_type, func) -> None:
        """
        Callbacks for events can be registered using this method.
        """
        if event_type not in self._callbacks.keys():
            self._callbacks[event_type] = []

        self._callbacks[event_type].append(func)

    def collidepoint(self, point: Tuple[int, int]) -> bool:
        """
        This method checks if a given point collides with the sprite.
        """
        _x, _y = point

        if _x > self._x - SIZE and _x < self._x + SIZE:
            if _y > self._y - SIZE and _y < self._y + SIZE:
                return True

        return False

    def _clicked(self) -> None:
        """
        This method executes, if the soldier was clicked. A click is defined as button down 
        and up, while hovering the sprite.
        """
        # if the soldier is active and a callback for the click event was defined, then execute it
        if self._active and Soldier.CLICKED in self._callbacks.keys():
            for func in self._callbacks[Soldier.CLICKED]:
                self._board_state = func(Soldier.CLICKED, self)
