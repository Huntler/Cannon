from stupid_engine.cannon.entities.player import Player
from stupid_engine.cannon.entities.cannon import CannonGame
from typing import Dict
import random
import time


class RandomAI:

    DELAY = 0.005

    def __init__(self, player: Player, cannon: CannonGame) -> None:
        self._type = player.get_type()
        self._player = player
        self._cannon = cannon

    def play_turn(self, state: Dict) -> bool:
        if "towns" in state.keys():
            position = random.choice(state["towns"])
            self._player.place_town(position)            

        soldiers = state[self._type]["soldiers"]
        moves = []
        while moves == [] and len(soldiers) != 0:

            soldier = random.choice(soldiers)
            moves = self._cannon.possible_moves(self._type, soldier)["moves"]

            if moves == []:
                soldiers.remove(soldier)
        
        # this only occurs if there are no moves
        if len(soldiers) == 0:
            quit()
            return False
        
        move = random.choice(moves)

        self._player.select_soldier(soldier)
        self._player.move_soldier(move)

        time.sleep(RandomAI.DELAY)

        return True