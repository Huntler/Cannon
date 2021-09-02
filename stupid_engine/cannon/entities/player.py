from stupid_engine.cannon.entities.figures import CannonSoldier, CannonTown
from typing import List, Tuple


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
