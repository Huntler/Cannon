from stupid_engine.cannon.entities.figures import OutOfBounds
from typing import Tuple


class Move:

    OUT_OF_BOUNDS = OutOfBounds

    def __init__(self, pos: Tuple[int, int], soldier: Tuple[int, int], value: int = -1,
                    finish: Tuple[int, int] = None, kill: Tuple[int, int] = None, shoot: bool = False, 
                    retreat: bool = False, slide: bool = False) -> None:
        self._pos = pos
        
        self._original_pos = soldier
        self._value = value

        self._finish = finish
        self._kill = kill

        self._retreat = retreat
        self._shoot = shoot
        self._slide = slide

    def is_finish_move(self) -> bool:
        return self._finish is not None

    def is_kill_move(self) -> bool:
        return self._kill is not None

    def is_retreat_move(self) -> bool:
        return self._retreat

    def is_shoot(self) -> bool:
        return self._shoot

    def is_sliding_move(self) -> bool:
        return self._slide
    
    def set_value(self, value) -> None:
        self._value = value

    def get_value(self) -> int:
        return self._value
    
    def get_killed_pos(self) -> Tuple[int, int]:
        return self._kill

    def get_town_pos(self) -> Tuple[int, int]:
        return self._finish

    def get_pos(self) -> Tuple[int, int]:
        return self._pos
    
    def get_original_pos(self) -> Tuple[int, int]:
        return self._original_pos

    def out_of_bounds(pos: Tuple[int, int]) -> bool:
        """
        This method checks if a given point is out of board bounds.
        """
        x, y = pos
        return x < 0 or 9 < x or y < 0 or 9 < y
