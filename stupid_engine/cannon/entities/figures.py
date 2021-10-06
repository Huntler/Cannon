from typing import Tuple
import random


class CannonFigure:
    def __init__(self, init_pos: Tuple[int, int]) -> None:
        self._pos = init_pos

    def get_pos(self) -> Tuple[int, int]:
        return self._pos
    
    def set_pos(self, pos) -> None:
        self._pos = pos


class CannonTown(CannonFigure):
    def __init__(self, init_pos: Tuple[int, int]) -> None:
        super().__init__(init_pos)


class CannonSoldier(CannonFigure):
    def __init__(self, init_pos: Tuple[int, int]) -> None:
        super().__init__(init_pos)


class OutOfBounds(CannonFigure):
    pass