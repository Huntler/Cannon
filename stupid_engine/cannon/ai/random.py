from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.entities.player import Player, PlayerType
from stupid_engine.cannon.entities.cannon import CannonGame
from typing import Dict, List, Tuple
import random
import time


class RandomAI:

    DELAY = 0.01

    def __init__(self, player: Player, cannon: CannonGame) -> None:
        """
        This is a random AI which acts greedy if it can.
        """
        self._type = player.get_type()
        self._player = player
        self._cannon = cannon

    def set_town_position(self, positions: List[Move]) -> Move:
        """
        This method places a position for the town randomly
        """
        position = random.choice(positions)
        return position

    def play_turn(self, state: Dict) -> bool:
        """
        This method lets this AI play a turn. The soldier and move 
        is selected randomly if the moves do not contain killing or 
        finishing moves.
        """
        soldiers, town = state[self._type]

        all_moves = []
        for soldier in soldiers:
            moves = self._cannon.moves(self._player, soldier)

            if moves != []:
                # defense first
                for move in moves:
                    if move.is_retreat_move():
                        self._cannon.execute(self._player, soldier, move)
                        time.sleep(RandomAI.DELAY)
                        return True

                # attack second
                for move in moves:
                    if move.is_kill_move() or move.is_finish_move():
                        self._cannon.execute(self._player, soldier, move)
                        time.sleep(RandomAI.DELAY)
                        return True
                
                # otherwise choose randomly
                all_moves.append((soldier, random.choice(moves)))
        
        # this only occurs if there are no moves
        # in this case the opponent wins the game
        if len(all_moves) == 0:
            enemy_type = PlayerType.DARK if self._player.get_type() == PlayerType.LIGHT else PlayerType.LIGHT
            self._cannon.end_game(enemy_type)
            return False

        soldier, move = random.choice(all_moves)
        self._player.move_soldier(soldier, move)

        time.sleep(RandomAI.DELAY)
        return True