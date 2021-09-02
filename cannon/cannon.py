from typing import Dict, List, Tuple


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


class CannonFigure:
    def __init__(self, init_pos: Tuple[int, int]) -> None:
        self._pos = init_pos

    def pos(self) -> Tuple[int, int]:
        return self._pos
    
    def set_pos(self, pos) -> None:
        self._pos = pos


class CannonTown(CannonFigure):
    def __init__(self, init_pos: Tuple[int, int]) -> None:
        super().__init__(init_pos)


class CannonSoldier(CannonFigure):
    def __init__(self, init_pos: Tuple[int, int]) -> None:
        super().__init__(init_pos)


class Player:
    def __init__(self) -> None:
        """
        The player is sets the Town initially and controlls the Soldiers afterwards. The 
        GameBoard has control over the players to manage who is allowd to play and who not.
        """
        self._town = None
        self._soldiers = None

    def init_light(self) -> None:
        self._init_positions(start_pos=(1, 8), end_pos=(9, 5))

    def init_dark(self) -> None:
        self._init_positions(start_pos=(0, 3), end_pos=(8, 0))

    def _init_positions(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> None:
        """
        This method initializes all Soldiers in a given range defined by two positions.
        :param start_pos: (column, row)
        :param end_pos: (column, row)
        """
        # this method only can be executed, if the soldiers were not initialized yet
        if self._soldiers:
            return

        self._soldiers = []
        for column in range(start_pos[0], end_pos[0] + 1, 2):
            for row in range(start_pos[1], end_pos[1], -1):
                self._soldiers.append(CannonSoldier(init_pos=(column, row)))

    def place_town(self, town_pos: Tuple[int, int]) -> None:
        self._town = CannonTown(init_pos=town_pos)

    def get_town_position(self) -> Tuple[int, int]:
        return self._town.pos()
    
    def move_soldier(self, current_position, final_position) -> None:
        """
        This method moves a soldier at position 'current_position' to the 'final_position'.
        """
        for s in self._soldiers:
            if s.pos() == current_position:
                s.set_pos(final_position)

    def get_state(self) -> List:
        """
        This method returns the current positions of all Soliders.
        """
        return [s.pos() for s in self._soldiers]
