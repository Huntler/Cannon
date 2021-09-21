"""
 - Move ordering implemented in _get_all_moves()

- Iterative depth -> dynamic depth depending on time left
- store 2 killer moves
- transition table TT
- random moves at the beginning

- 2D container to keep track of the good moves (history heuristic)


"""
from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.entities.cannon import CannonGame
from stupid_engine.cannon.entities.player import Player
from typing import Dict, List, Tuple
from stupid_engine.cannon.ai.ai import BaseAI
import random


class AlphaBeta(BaseAI):
    def __init__(self, player: Player, cannon: CannonGame, alpha: int, beta: int, depth: int, weights: List[int]) -> None:
        super().__init__(player, cannon)

        self._moves = None
        
        self._alpha = alpha
        self._beta = beta

        self._depth = depth
        self._weights = weights

    def play_turn(self, state: Dict) -> bool:
        _, move = self._algorithm(self._alpha, self._beta, self._depth, self._player, None)
        if not move:
            return False

        self._cannon.execute(self._player, move)
        return True

    def set_town_position(self, positions: List[Move]) -> Move:
        """
        This method places a position for the town randomly
        """
        position = random.choice(positions)
        return position
    
    def _get_all_moves(self, player: Player) -> List[Move]:
        """
        This helper method gets all moves for all soldiers available.
        """
        moves = []
        for s in player.get_soldiers():
            for m in self._cannon.moves(player, s):
                moves.append(m)
                # evaluate all moves (even some unnecessary ones)
                value = self._cannon.eval(player, m, self._weights)
                m._value = value

        # sort the moves using the evaluation value
        moves.sort(key=lambda m: m._value, reverse=True)
        return moves

    def _algorithm(self, alpha: int, beta: int, depth: int, player: Player, move: Move) -> Tuple[int, Move]:
        # execute the given move to search deeper
        if move:
            self._cannon.execute(player, move, testing_only=True)
            player = self._cannon._get_enemy_player(player)

        # if the maximum depth is reached, then return the best move
        if(depth == 0) :
            moves = self._get_all_moves(player)
            # because of move ordering, the first move is the best one
            best_move = moves[0]

            print(f"{player.get_type()} in leaf node")
            print(f"The values are alpha={alpha}, beta={beta}, score={best_move._value}")
            print(f"Move is {best_move.get_original_pos()} -> {best_move.get_pos()}")
            print()

            return best_move._value, best_move
        
        best_move = None
        moves = self._get_all_moves(player)
        for move in moves:
            # do the recursion step
            score, _ = self._algorithm(-1 * beta, -1 * alpha, depth - 1, player, move)
            score *= -1

            # undo the recursion step
            self._cannon.undo(player, move)

            if score >= beta:
                # fail hard -> beta cut off
                # this is the pruning part
                return beta, move

            if score > alpha:
                alpha = score
                # save the best move so far
                best_move = move
        
        return alpha, best_move