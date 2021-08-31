from typing import Tuple


class Sprite:
    def set_position(self, pos: Tuple[int, int]) -> None:
        raise NotImplemented
    
    def get_position(self) -> Tuple[int, int]:
        raise NotImplemented
    
    def draw(self) -> None:
        raise NotImplemented        