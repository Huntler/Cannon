from typing import Tuple


class RandomAI:
    def __init__(self, player: Player) -> None:
        self._player = player
    
    def get_move(self, moves) -> Tuple[int, int]:
        pass