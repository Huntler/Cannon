from typing import Dict, List, Tuple
from stupid_engine.cannon.entities.player import Player


class CannonGame:

    LIGHT = 0
    DARK = 1

    def __init__(self) -> None:
        self._player_light = Player()
        self._player_light.init_light()

        self._player_dark = Player()
        self._player_dark.init_dark()

        self._active_player = self._player_light
        self._active_soldier_pos = None

    def possible_moves(self, pos_selected_soldier: Tuple[int, int]) -> Dict:
        """
        This method collects all possible moves for the given soldier and adds 
        the list of moves to the game state.
        """
        self._active_soldier_pos = pos_selected_soldier
        state = self.get_state()

        self._possible_movement(pos_selected_soldier, state)

        return state

    def _possible_movement(self, pos_selected_soldier, state):
        # set the game direction, so in which direction the soldiers are moving
        dir = -1 if self._active_player == self._player_light else +1
        moves = []

        # get all moves first
        # the basic forward move
        positions = []
        positions.append((pos_selected_soldier[0] - 1, pos_selected_soldier[1] + dir))
        positions.append((pos_selected_soldier[0], pos_selected_soldier[1] + dir))
        positions.append((pos_selected_soldier[0] + 1, pos_selected_soldier[1] + dir))

        # delete moves that are invalid
        for pos in positions:
            x, y = pos
            # check x for out of bounds
            if x < 0 or 9 < x or y < 0 or 9 < y:
                continue

            # check if there is an object
            if pos in state["light"] or pos in state["dark"]:
                continue

            moves.append(pos)

        state["moves"] = moves

    def make_move(self, position: Tuple[int, int]) -> Dict:
        if not self._active_soldier_pos:
            return
        
        # move the soldier of the current player
        self._active_player.move_soldier(self._active_soldier_pos, position)
        self._switch_active_player()
        
        return self.get_state()

    def _switch_active_player(self) -> None:
        """
        This method switches the current active player
        """
        if self._active_player == self._player_light:
            self._active_player = self._player_dark
        else:
            self._active_player = self._player_light

    def get_state(self) -> Dict:
        # TODO: add the current player playing
        # TODO: add the town
        state = {}

        state["light"] = self._player_light.get_state()
        state["dark"] = self._player_dark.get_state()

        if self._active_player == self._player_light:
            state["active"] = CannonGame.LIGHT
        else:
            state["active"] = CannonGame.DARK


        return state