from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.ai.ai import BaseAI
from stupid_engine.cannon.entities.cannon import CannonGame
from stupid_engine.cannon.entities.player import Player
from typing import Dict, List, Tuple


class Human(BaseAI):
    def __init__(self, player: Player, cannon: CannonGame) -> None:
        super().__init__(player, cannon)

        self._temp_state = None

    def set_town_position(self, positions: List[Move]) -> Move:
        """
        This method sets the move to place the players town
        """
        # a bit hacky -.-
        if type(positions) == tuple:
            return Move(positions)
            
        return None
    
    def play_turn(self, state: Dict) -> bool:
        """
        This method returns true, if the given state has changed.
        """
        if self._temp_state is None:
            self._temp_state = state
        
        # if the states differ, then the human made a turn so reset the 
        # temp variable and return true
        if state != self._temp_state:
            self._temp_state = None
            return True
        
        return False