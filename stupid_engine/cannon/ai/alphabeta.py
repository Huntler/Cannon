"""
 - Move ordering implemented in _get_all_moves()

- Iterative depth -> dynamic depth depending on time left
- store 2 killer moves
- transition table TT
- random moves at the beginning

- 2D container to keep track of the good moves (history heuristic)


"""
from stupid_engine.cannon.ai.move_generator import MoveGenerator
from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.entities.cannon import CannonGame
from stupid_engine.cannon.entities.player import Player, PlayerType
from typing import Dict, List, Tuple
from stupid_engine.cannon.ai.ai import BaseAI
import random
import time
from copy import deepcopy, copy
import cProfile, pstats


VERBOSE = False


class AlphaBeta(BaseAI):
    def __init__(self, player: Player, cannon: CannonGame, alpha: int, beta: int, max_depth: int, time_limit: int, weights: List[int], refresh_tt: bool = True) -> None:
        super().__init__(player, cannon)

        self._moves = None
        self._moves_generator = MoveGenerator()
        
        # get the initial alpha-beta window
        self._alpha = alpha
        self._beta = beta

        # get the depth and weight values
        self._depth = max_depth
        self._weights = weights
        self._refresh_tt = refresh_tt

        # iterative deepening
        self._time_start = 0
        self._time_limit = time_limit

        # create the transposition table container
        self._tt = dict()

    def play_turn(self, state: Dict) -> bool:
        """
        This method lets the agent calculate the best move. If there is no possible 
        move, then this function returns false. Otherwise the move is registered and true 
        returned.
        """
        # if less soldiers are available, then the algorithm can search deeper
        # also it is clever to switch the focus by changing the evaluation function's weights

        with cProfile.Profile() as pr:
            # remember the start time for iterative deepening
            self._time_start = time.time()
            _, move = self._algorithm(self._alpha, self._beta, self._depth, self._player, None)
            if not move:
                enemy = self._cannon._get_enemy_player(self._player)
                self._cannon.end_game(enemy.get_type())
                pr.print_stats()
                return False

            self._cannon.execute(self._player, move)

            # clean up the transposition table
            if self._refresh_tt:
                self._tt = dict()
        
        pstats.Stats(pr).sort_stats(pstats.SortKey.TIME).print_stats(10)
        return True

    def set_town_position(self, positions: List[Move]) -> Move:
        """
        This method places a position for the town randomly
        """
        position = random.choice(positions)
        return position

    def _get_moves(self, player) -> List[Move]:        
        return self._moves_generator.generate_moves(player, self._cannon._get_enemy_player(player))

    def _get_moves_sorted(self, player) -> List[Move]:
        moves = self._get_moves(player)

        for m in moves:
            self._cannon.eval(player, m, self._weights)

        self._sort_moves(moves)
        return moves

    def _sort_moves(self, moves: List[Move]):
        moves.sort(key=lambda m: m._value, reverse=True)

    def _algorithm(self, alpha: int, beta: int, depth: int, player: Player, move: Move) -> Tuple[int, Move]:
        # get the current time to check if the search should end
        if self._time_limit:
            time_exceeded = time.time() - self._time_start > self._time_limit
        else:
            time_exceeded = False

        # execute the given move to search deeper
        if move is not None:
            self._cannon.execute(player, move, testing_only=True)
            player = self._cannon._get_enemy_player(player)

        # if the maximum depth is reached, then return the best move
        if(depth == 0 or time_exceeded) :
            if depth != 0:
                print("\tReached depth: ", self._depth - depth)
                
            moves = self._get_moves_sorted(player)

            if len(moves) == 0:
                return 0, None

            # because of move ordering, the first move is the best one
            best_move = moves[0]
            return best_move._value, best_move

        # check if there is already a best move known, before running the search
        # this optimization uses the "transposition table" and the "zobrist hashing"
        tt_hash = self._cannon.hash(player.get_type())
        best_move = self._tt.get(tt_hash, None)
        if best_move is not None:
            score, _ = self._algorithm(-1 * beta, -1 * alpha, depth - 1, player, best_move)
            score *= -1
            self._cannon.undo(player, best_move)

            return score, best_move

        for move in self._get_moves(player):
            move._value = self._cannon.eval(player, move, self._weights)
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
        
        if best_move is not None:
            stored = self._tt.get(best_move, None)
            if stored is not None:
                raise ValueError("Multiple hashes are not valid!")

            self._tt[tt_hash] = deepcopy(best_move)

        return alpha, best_move