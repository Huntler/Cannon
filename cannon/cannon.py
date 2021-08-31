from typing import Dict, List, Tuple


class CannonGame:

    LIGHT = 0
    DARK = 1

    def __init__(self) -> None:
        self._player_light = Player()
        self._player_light.init_light()

        self._player_dark = Player()
        self._player_dark.init_dark()

        self._active_player = CannonGame.LIGHT

    def possible_moves(self, pos_selected_soldier) -> Dict:
        print(f"Hello World from Soldier {pos_selected_soldier}!")
        state = self.get_state()
        state["light"][2] = (1, 5)
        # TODO: change the state and give it back to the GUI
        return state

    def get_state(self) -> Dict:
        # TODO: add the current player playing
        # TODO: add the town
        state = {}

        state["light"] = self._player_light.get_state()
        state["dark"] = self._player_dark.get_state()

        state["active"] = self._active_player

        return state


class CannonFigure:
    def __init__(self, init_pos: Tuple[int, int]) -> None:
        self._pos = init_pos

    def pos(self) -> Tuple[int, int]:
        return self._pos


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

    def get_state(self) -> List:
        """
        This method returns the current positions of all Soliders.
        """
        return [s.pos() for s in self._soldiers]
