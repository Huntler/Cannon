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
from stupid_engine.cannon.entities.player import Player, PlayerType
from typing import Dict, List, Tuple
from stupid_engine.cannon.ai.ai import BaseAI
import random
from copy import copy, deepcopy


VERBOSE = False


class AlphaBeta(BaseAI):
    def __init__(self, player: Player, cannon: CannonGame, alpha: int, beta: int, depth: int, weights: List[int], refresh_tt: bool = True) -> None:
        super().__init__(player, cannon)

        self._moves = None
        
        # get the initial alpha-beta window
        self._alpha = alpha
        self._beta = beta

        # get the depth and weight values
        self._depth = depth
        self._weights = weights
        self._refresh_tt = refresh_tt

        # create the transposition table container
        self._tt = dict()

    def play_turn(self, state: Dict) -> bool:
        """
        This method lets the agent calculate the best move. If there is no possible 
        move, then this function returns false. Otherwise the move is registered and true 
        returned.
        """
        _, move = self._algorithm(self._alpha, self._beta, self._depth, self._player, None)
        if not move:
            enemy = self._cannon._get_enemy_player(self._player)
            self._cannon.end_game(enemy.get_type())
            return False

        self._cannon.execute(self._player, move)

        # clean up the transposition table
        if self._refresh_tt:
            self._tt = dict()
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
        # this optimization is called "move-ordering"
        moves.sort(key=lambda m: m._value, reverse=True)
        return moves

    def _algorithm(self, alpha: int, beta: int, depth: int, player: Player, move: Move) -> Tuple[int, Move]:
        # execute the given move to search deeper
        if move is not None:
            self._cannon.execute(player, move, testing_only=True)
            player = self._cannon._get_enemy_player(player)

        # if the maximum depth is reached, then return the best move
        if(depth == 0) :
            moves = self._get_all_moves(player)
            if len(moves) == 0:
                return 0, None
            # because of move ordering, the first move is the best one
            best_move = moves[0]

            if VERBOSE:
                print(f"{player.get_type()} in leaf node")
                print(f"The values are alpha={alpha}, beta={beta}, score={best_move._value}")
                print(f"Move is {best_move.get_original_pos()} -> {best_move.get_pos()}")
                print()

            return best_move._value, best_move

        # check if there is already a best move known, before running the search
        # this optimization uses the "transposition table" and the "zobrist hashing"
        tt_hash = self._cannon.hash(player.get_type())
        best_move = self._tt.get(tt_hash, None)
        if best_move is not None:

            # s1 = self._cannon.get_state()
            if VERBOSE:
                print(f"Load a move from the transposition table. Entries in table {len(self._tt)}")
                print(f"{player.get_type()}'s move is {best_move.get_original_pos()} -> {best_move.get_pos()}")

            score, _ = self._algorithm(-1 * beta, -1 * alpha, depth - 1, player, best_move)
            score *= -1
            self._cannon.undo(player, best_move)

            return score, best_move

        moves = self._get_all_moves(player)
        for move in moves:
            s1 = self._cannon.get_state()
            # do the recursion step
            score, _ = self._algorithm(-1 * beta, -1 * alpha, depth - 1, player, move)
            score *= -1

            # undo the recursion step
            self._cannon.undo(player, move)
            s2 = self._cannon.get_state()
            assert s1 == s2

            if score >= beta:
                # fail hard -> beta cut off
                # this is the pruning part
                return beta, move

            if score > alpha:
                alpha = score
                # save the best move so far
                best_move = move
        
        if best_move is not None:
            stored = self._tt.get(best_move, None)
            if stored is not None:
                raise ValueError("Multiple hashes are not valid!")

            self._tt[tt_hash] = deepcopy(best_move)

        return alpha, best_move