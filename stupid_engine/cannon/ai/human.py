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
            return Move(positions, None)
            
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
    
    def to_dict(self) -> dict:
        """
        This method is used to transform the most valuable information 
        into a dictonary which can be written to disk later on. This is 
        useful, if the game should be safed and restored.
        """
        d = dict()
        d["ai_type"] = "human"
        d["p"] = self._player.get_type()
        return d
    
    def from_dict(d: Dict, cannon: CannonGame):
        """
        This creates the Human AI object which can be configured in order 
        to use manual inputs.
        """
        return Human(d["p"], cannon)