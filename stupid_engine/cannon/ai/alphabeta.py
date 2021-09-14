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


# table: history_table[player white|dark][x][y]
history_table = [[[None for _ in range(10)] for _ in range(10)] for player in range(2)]

class AlphaBeta(BaseAI):
    def __init__(self, player: Player, cannon: CannonGame) -> None:
        super().__init__(player, cannon)

        self._moves = None

    def play_turn(self, state: Dict) -> bool:
        _, move = self._algorithm(-10_000, 10_000, 5, self._player, None)
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
                value = self._cannon.eval(player, m)
                m._value = value

        # sort the moves using the evaluation value
        moves.sort(key=lambda m: m._value, reverse=True)
        return moves

    def _algorithm(self, alpha: int, beta: int, depth: int, player: Player, move: Move) -> Tuple[int, Move]:
        # execute the given move to search deeper
        if move:
            # print(f"{player.get_type()} executing:")
            self._cannon.execute(player, move, testing_only=True)
            player = self._cannon._get_enemy_player(player)
            # print(f"currently at depth {depth} and alpha {alpha}, beta {beta}. Score is {move._value}")
            # print(f"player changed to {player.get_type()}\n")

        # if the maximum depth is reached, then return the best move
        if(depth == 0) :
            moves = self._get_all_moves(player)
            max_eval, max_move = 0, None
            for move in moves:
                eval = move._value
                if eval > max_eval:
                    max_eval = eval
                    max_move = move

            return max_eval, max_move
        
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
    
    def _quiesce(self, alpha: int, beta: int, move: Move) -> int:
        stand_pat = self._cannon.eval(self._player, move)
        return stand_pat, move
