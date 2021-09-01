from typing import Tuple
from visuals.sprite import Sprite, to_pixel
from cannon.cannon import CannonGame
from visuals.soldier import Soldier
import pygame as py


SIZE = 8
COLOR = (255, 255, 255)


class Movement(Sprite):
    
    CLICKED = py.event.custom_type()

    def __init__(self, surface, board_dim, border_dim, pos) -> None:
        """
        This class represents a soldier visually. Given on the position, the actual 
        pixel position on screen is calulated. The type determines the drawn color.
        """
        self._callbacks = dict()

        # set the correct type and color
        self._color = COLOR

        # set position
        self._x_pos, self._y_pos = pos
        self._board_dim = board_dim
        self._border_dim = border_dim
        self._x, self._y = to_pixel((self._x_pos, self._y_pos), self._board_dim, self._border_dim)

        self._surface = surface
        super().__init__()

    def draw(self):
        """
        This method draws this sprite on the screen at the calulated position. If 
        the sprite is active, then the hover and click events will be handled in here.
        """
        super().draw()

        pos = (self._x, self._y)
        size = SIZE

        if self.collidepoint(py.mouse.get_pos()):
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
        This method executes, if the movement point was clicked. A click is defined 
        as button down and up, while hovering the sprite.
        """
        # if the movement point is active and a callback for the click event was defined, t
        # hen execute it
        if Movement.CLICKED in self._callbacks.keys():
            for func in self._callbacks[Movement.CLICKED]:
                self._board_state = func(Movement.CLICKED, self)


