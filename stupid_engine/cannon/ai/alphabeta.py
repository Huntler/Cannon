"""
 - Move ordering implemented in _get_all_moves()

- Iterative depth -> dynamic depth depending on time left
- store 2 killer moves
- transition table TT
- random moves at the beginning

- 2D container to keep track of the good moves (history heuristic)


"""
import math
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


VERBOSE = True


class AlphaBeta(BaseAI):
    def __init__(self, player: Player, cannon: CannonGame, alpha: int, beta: int, depth: int, time_limit: int, weights: List[int], refresh_tt: bool = True) -> None:
        super().__init__(player, cannon)

        self._moves = None
        self._moves_generator = MoveGenerator()
        
        # get the initial alpha-beta window
        self._alpha = alpha
        self._beta = beta

        # get the depth and weight values
        self._depth = depth
        self._weights = weights
        self._refresh_tt = refresh_tt

        # iterative deepening, if not time limit is given, then set a max of 10 minute
        self._time_start = 0
        self._time_limit = time_limit if time_limit else 10*60

        # create the transposition table container
        self._tt = dict()

        # create some statistics <3
        self._moves_searched = 0
        self._depth_per_search = []
        self._mean_depth = lambda: sum(self._depth_per_search) / self._moves_searched

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
            time_exceeded = time.time() - self._time_start > self._time_limit
            extra_depth = 0
            best_move = move = None
            while not time_exceeded:
                # safe the best move found so far and ingore the "best move" found on the current ply
                # this ply could be interrupted cause the time has exceeded
                best_move = move
                _, move = self._algorithm(self._alpha, self._beta, self._depth + extra_depth, self._player, None)

                # search deeper if the time has not exceeded yet
                extra_depth += 1

                time_exceeded = time.time() - self._time_start > self._time_limit

            # if the best move is still none, then take the found move even it could be not the best
            # but this is still better than nothing
            if not best_move:
                best_move = move
                
            # add statistics
            self._moves_searched += 1
            self._depth_per_search.append(self._depth + extra_depth -1)

            if VERBOSE:
                # the ply self._depth + extra_depth -1 contains the best_move the player will take
                # -1 because we interrupt the search if the time exceeds
                print()
                print(self._player.get_type().upper())
                print(f"\tThe player has searched {self._moves_searched} move so far")
                print(f"\tThe average search depth was {self._mean_depth()} plys")
                diff = self._depth_per_search[0] if self._moves_searched == 1 else self._depth_per_search[-1] - self._depth_per_search[-2]
                print(f"\tThe player searched {self._depth + extra_depth -1} plys, {diff} plys deeper than before")
                print(f"\tThe move's score is {_}")

            if not best_move:
                enemy = self._cannon._get_enemy_player(self._player)
                self._cannon.end_game(enemy.get_type())
                pr.print_stats()
                return False

            self._cannon.execute(self._player, best_move)

            # clean up the transposition table
            if self._refresh_tt:
                self._tt = dict()
        
        # pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE).print_stats(10)
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
        # execute the given move to search deeper
        if move is not None:
            self._cannon.execute(player, move, testing_only=True)
            player = self._cannon._get_enemy_player(player)

        # if the maximum depth is reached, then return the best move
        # also, get the current time to check if the search should end
        time_exceeded = time.time() - self._time_start > self._time_limit
        if(depth == 0 or time_exceeded):
            self._cannon.eval(player, move, self._weights)        
            return move._value, move

        moves = None

        # check if there is already a best move known, before running the search
        # this optimization uses the "transposition table" and the "zobrist hashing"
        tt_hash = self._cannon.hash(player.get_type())
        best_move = self._tt.get(tt_hash, None)
        if best_move is not None:
            # loading the best move known and set it to the beginning of the list of
            # avialable moves
            moves = [best_move] + self._get_moves_sorted(player)
        else:
            moves = self._get_moves(player)

        for move in moves:
            # do the recursion step
            score, _ = self._algorithm(-1 * beta, -1 * alpha, depth - 1, player, move)
            score *= -1

            # undo the recursion step
            self._cannon.undo(player, move)

            if score >= beta:
                # fail hard -> beta cut off
                # this is the pruning part
                return score, move

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