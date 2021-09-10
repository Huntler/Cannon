from typing import Tuple


class Move:
    def __init__(self, pos: Tuple[int, int], finish_move: bool = False, kill_move: bool = False, shoot: bool = False, retreat: bool = False) -> None:
        self._pos = pos
        self._finish_move = finish_move
        self._kill_move = kill_move
        self._retreat = retreat
        self._shoot = shoot
    
    def is_finish_move(self) -> bool:
        return self._finish_move
    
    def is_kill_move(self) -> bool:
        return self._kill_move
    
    def is_retreat_move(self) -> bool:
        return self._retreat
    
    def is_shoot(self) -> bool:
        return self._shoot

    def get_pos(self) -> Tuple[int, int]:
        return self._pos
    
    def out_of_bounds(pos: Tuple[int, int]) -> bool:
        """
        This method checks if a given point is out of board bounds.
        """
        x, y = pos
        return x < 0 or 9 < x or y < 0 or 9 < y