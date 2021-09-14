from stupid_engine.backend.visuals.font import Font
import pygame as py
from typing import Tuple
from stupid_engine.backend.visuals.sprite import Sprite, to_pixel


class Text(Sprite):
    def __init__(self, text: str, screen, draw_area: Tuple[int, int, int, int], pos: Tuple[int, int], font: str = Font.ARIAL) -> None:
        super().__init__()

        self._screen = screen
        self._draw_area = draw_area
        self._pos = pos

        py.font.init()
        self._font_size = 24
        self._font_color = (255, 255, 255)
        self._font = py.font.SysFont(font, self._font_size)

        self._text = text
        self.set_position(pos)
    
    def set_text(self, text: str) -> None:
        self._text = text
    
    def set_position(self, pos: Tuple[int, int]) -> None:
        x, y = self._pos = pos
        x, y = to_pixel((x, y), self._draw_area)
        self._x = x - self._font_size / 2
        self._y = y - self._font_size / 2
    
    def get_position(self) -> Tuple[int, int]:
        return self._pos
    
    def collidepoint(self, point: Tuple[int, int]) -> bool:
        return False
    
    def draw(self) -> None:
        super().draw()

        # draw the text
        text = self._font.render(self._text, False, self._font_color)
        self._screen.blit(text, (self._x, self._y))
        