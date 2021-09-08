from typing import Dict, List, Tuple
from stupid_engine.cannon.entities.player import Player, PlayerType


class CannonGame:
    def __init__(self, p_light: Player, p_dark: Player) -> None:
        self._p_light = p_light
        self._p_dark = p_dark
    
    def get_town_positions(self, turn: PlayerType) -> Dict:
        """
        This method gets all possible positions to place a town for the given player.
        """
        state = self.get_state()
        state["towns"] = []

        # get all possible positions for a town
        y = 9 if turn == PlayerType.LIGHT else 0
        for x in range(0, 10):
            state["towns"].append((x, y))

        return state

    def possible_moves(self, turn: PlayerType, pos: Tuple[int, int]) -> Dict:
        """
        This method collects all possible moves for the given soldier and adds 
        the list of moves to the game state.
        """
        # this is invoked by a callback of the UI or an AI
        state = self.get_state()

        self._possible_movement(turn, pos, state)

        return state

    def _possible_movement(self, turn: PlayerType, pos: Tuple[int, int], state: Dict) -> None:
        # set the game direction, so in which direction the soldiers are moving
        dir = -1 if turn == PlayerType.LIGHT else +1
        
        x, y = pos
        moves = []

        # get all moves first
        # the basic forward move
        positions = []
        positions.append((x - 1, y + dir))
        positions.append((x, y + dir))
        positions.append((x + 1, y + dir))

        # delete moves that are invalid
        for pos in positions:
            x, y = pos
            # check x for out of bounds
            if x < 0 or 9 < x or y < 0 or 9 < y:
                continue

            # check if there is an object
            if pos in state[PlayerType.LIGHT]["soldiers"] or pos in state[PlayerType.DARK]["soldiers"]:
                continue

            moves.append(pos)

        state["moves"] = moves

    def get_state(self) -> Dict:
        state = {}

        state[PlayerType.LIGHT] = self._p_light.get_state()
        state[PlayerType.DARK] = self._p_dark.get_state()

        return state