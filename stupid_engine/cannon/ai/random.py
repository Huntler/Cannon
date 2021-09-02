from stupid_engine.cannon.entities.player import Player, PlayerType
from stupid_engine.cannon.entities.cannon import CannonGame
from typing import SupportsFloat, Tuple
import random


class RandomAI:
    def __init__(self, cannon: CannonGame, player: Player) -> None:
        self._cannon = cannon
        self._player = player
    
    def get_player_type(self) -> PlayerType:
        return self._player.get_type()

    def play_turn(self) -> Tuple[int, int]:
        soldiers = self._player._soldiers
        moves = []
        while moves == [] and len(soldiers) != 0:

            soldier = random.choice(soldiers)
            moves = self._cannon.possible_moves(self.get_player_type(), soldier.pos())["moves"]

            if moves == []:
                soldiers.remove(soldier)
        
        if len(soldiers) == 0:
            return
        
        move = random.choice(moves)

        self._player.select_soldier(soldier.pos())
        self._player.move_soldier(move)