from typing import Tuple
from stupid_engine.backend.visuals.sprite import Sprite
from stupid_engine.backend.visuals.sprite import to_pixel as _to_pixel
import pygame as py


def to_pixel(pos: Tuple[int, int], board_dim: Tuple[int, int], border_dim: Tuple[int, int], size: Tuple[int, int]) -> Tuple[int, int]:
    x, y = _to_pixel(pos, board_dim, border_dim)
    cx, cy = size
    return x - cx / 2, y - cy / 2


class Image(Sprite):
    def __init__(self, surface, board_dim, border_dim, pos, img_path: str, size: Tuple[int, int]) -> None:
        """
        This class represents an image visually. Given on the position, the actual 
        pixel position on screen is calulated.
        """
        self._callbacks = dict()

        # load image
        self._size = size
        self._img = py.image.load(img_path)
        w, h = self._size
        self._img = py.transform.scale(self._img, (w, h))

        # set position
        self._x_pos, self._y_pos = pos
        self._board_dim = board_dim
        self._border_dim = border_dim
        self._x, self._y = to_pixel(
            (self._x_pos, self._y_pos), self._board_dim, self._border_dim, self._size)

        self._surface = surface
        super().__init__()

    def draw(self):
        """
        This method draws this sprite on the screen at the calulated position. If 
        the sprite is active, then the hover and click events will be handled in here.
        """
        super().draw()

        pos = (self._x, self._y)
        w, h = self._size
        img = self._img

        if self._active and self.collidepoint(py.mouse.get_pos()):
            factor = 1.2
            _w, _h = int(w * factor), int(h * factor)
            img = py.transform.scale(self._img, (_w, _h))
            # get new center
            dw, dh = _w - w, _h - h
            pos = (self._x - dw / 2, self._y - dh / 2)


        self._surface.blit(img, pos)
    
    def set_position(self, pos: Tuple[int, int]) -> None:
        """
        This method sets the new position and calculates the pixel position on screen.
        """
        self._x_pos, self._y_pos = pos
        self._x, self._y = to_pixel(
            (self._x_pos, self._y_pos), self._board_dim, self._border_dim, self._size)

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
        sx, sy = self._size

        if _x > self._x and _x < self._x + sx:
            if _y > self._y and _y < self._y + sy:
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