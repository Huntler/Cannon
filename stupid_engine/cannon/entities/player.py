from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.entities.figures import CannonSoldier, CannonTown
from typing import Dict, List, Tuple


class PlayerType:
    LIGHT = "light"
    DARK = "dark"


class Player:
    def __init__(self, type: PlayerType) -> None:
        """
        The player is sets the Town initially and controlls the Soldiers afterwards. The 
        GameBoard has control over the players to manage who is allowd to play and who not.
        """
        self._type = type
        self._town = None
        self._soldiers = None
        self._selected_soldier = None
        self._ai = None

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

    def is_town_placed(self) -> bool:
        return self._town != None

    def place_town(self, positions: List[Move]) -> None:
        move = self._ai.set_town_position(positions)

        # to wait for a human, humans are slow
        if move is None:
            return

        self._town = CannonTown(init_pos=move.get_pos())

    def get_town(self) -> CannonTown:
        return self._town

    def get_type(self) -> PlayerType:
        return self._type
    
    def get_soldiers(self) -> List[CannonSoldier]:
        return self._soldiers

    def move_soldier(self, move: Move) -> None:
        """
        This method moves the given soldier to a given position.
        """            
        soldier = self.soldier_at(move.get_original_pos())
        soldier.set_pos(move.get_pos())

    def get_state(self) -> Tuple[List[CannonSoldier], CannonTown]:
        """
        This method returns all Soliders and the Town.
        """
        return self._soldiers, self._town

    def set_controller(self, ai) -> None:
        """
        This method sets the ai which controlls this player and makes choices.
        """
        self._ai = ai

    def play_turn(self, state: Dict) -> bool:
        """
        This Method lets the ai or human play a turn. The returning is true if a move was made.
        """
        return self._ai.play_turn(state)
    
    def remove_at(self, pos: Tuple[int, int]) -> None:
        """
        This method removes a soldier at the given position.
        """
        to_remove = self.soldier_at(pos)
        self._soldiers.remove(to_remove)
    
    def select_soldier(self, soldier: CannonSoldier) -> None:
        """
        Selects a soldier.
        """
        self._selected_soldier = soldier
    
    def get_selected_soldier(self) -> CannonSoldier:
        """
        Returns the selected soldier
        """
        return self._selected_soldier

    def soldier_at(self, pos: Tuple[int, int]) -> CannonSoldier:
        """
        This method checks if there is a soldier at the given position.
        """
        soldier = None
        for s in self._soldiers:
            if s.get_pos() == pos:
                soldier = s

        return soldier
    
    def army_size(self) -> int:
        """
        Returns the amount of soliders.
        """
        return len(self._soldiers)

