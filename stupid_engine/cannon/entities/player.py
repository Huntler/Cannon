from stupid_engine.cannon.entities.figures import CannonSoldier, CannonTown
from typing import Dict, List, Tuple


class PlayerType:
    LIGHT = 0
    DARK = 1


class Player:

    def __init__(self, type: PlayerType) -> None:
        """
        The player is sets the Town initially and controlls the Soldiers afterwards. The 
        GameBoard has control over the players to manage who is allowd to play and who not.
        """
        self._type = type
        self._town = None
        self._soldiers = None
        self._selected = None

        if self._type == PlayerType.LIGHT:
            self._init_positions(start_pos=(1, 8), end_pos=(9, 5))
        elif self._type == PlayerType.DARK:
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
    
    def select_soldier(self, position) -> None:
        """
        This method selects a soldier owned by this player.
        """
        for s in self._soldiers:
            if s.pos() == position:
                self._selected = s

    def get_type(self) -> PlayerType:
        return self._type

    def move_soldier(self, position) -> None:
        """
        This method moves the selected soldier to a given position. Make 
        sure, that a soldier was selected before exectuing this.
        """
        if not self._selected:
            print("Tried to move a soldier, but none was selected.")
            quit()
            
        self._selected.set_pos(position)
        self._selected = None

    def get_state(self) -> Dict:
        """
        This method returns the current positions of all Soliders.
        """
        state = dict()
        state["soldiers"] = [s.pos() for s in self._soldiers]
        if self._town is not None:
            state["town"] = self._town.pos()
        return state
