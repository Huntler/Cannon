from typing import Tuple
import pygame as py
from stupid_engine.backend.visuals.sprite import Sprite, to_pixel


# a custom to_pixel function so the center of a block is used for positioning
def _to_pixel(pos: Tuple[int, int], board_dim: Tuple[int, int], border_dim: Tuple[int, int], size: Tuple[int, int]) -> Tuple[int, int]:
    x, y = to_pixel(pos, board_dim, border_dim)
    w, h = size
    return x - w / 2, y - h / 2


class Block(Sprite):
    def __init__(self, surface, board_dim, border_dim, pos, color) -> None:
        """
        This class represents a rectangle visually. Given on the position, the actual 
        pixel position on screen is calulated.
        """
        self._callbacks = dict()

        self._active = False

        # set color
        self._color = color
        self._size = (20, 20)

        # set position
        self._x_pos, self._y_pos = pos
        self._board_dim = board_dim
        self._border_dim = border_dim
        self._x, self._y = _to_pixel(
            (self._x_pos, self._y_pos), self._board_dim, self._border_dim, self._size)

        self._surface = surface
        super().__init__()
    
    def draw(self):
        """
        This method draws this sprite on the screen at the calulated position. If 
        the sprite is active, then the hover and click events will be handled in here.
        """
        super().draw()

        x, y = (self._x, self._y)
        w, h = self._size

        if self._active and self.collidepoint(py.mouse.get_pos()):
            w, h = (w * 1.2, h * 1.2)

        py.draw.rect(self._surface, self._color, (x, y, w, h))
    
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
        w, h = self._size

        if _x > self._x - w and _x < self._x + w:
            if _y > self._y - h and _y < self._y + h:
                return True

        return False

    def _clicked(self) -> None:
        """
        This method executes, if the soldier was clicked. A click is defined as button down 
        and up, while hovering the sprite.
        """
        if self._active:
            for event_type in self._callbacks.keys():
                for func in self._callbacks[event_type]:
                    self._board_state = func(event_type, self)
