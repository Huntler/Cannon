from stupid_engine.cannon.entities.move import Move
from typing import Dict, List, Tuple
from stupid_engine.cannon.entities.player import Player
from stupid_engine.cannon.entities.cannon import CannonGame


class BaseAI:
    def __init__(self, player: Player, cannon: CannonGame) -> None:
        self._type = player.get_type()
        self._player = player
        self._cannon = cannon

    def set_town_position(self, positions: List[Tuple[int, int]]) -> Tuple[int ,int]:
        raise NotImplemented

    def play_turn(self, state: Dict) -> bool:
        raise NotImplemented