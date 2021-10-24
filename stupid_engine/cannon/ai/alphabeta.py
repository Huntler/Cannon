"""
 - Move ordering implemented in _get_all_moves()

- Iterative depth -> dynamic depth depending on time left
- store 2 killer moves
- transition table TT
- random moves at the beginning

- 2D container to keep track of the good moves (history heuristic)


"""
import math
from stupid_engine.backend.misc.stats import Statistics
from stupid_engine.cannon.ai.move_generator import MoveGenerator
from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.entities.cannon import CannonGame
from stupid_engine.cannon.entities.player import Player
from typing import Dict, List, Tuple
from stupid_engine.cannon.ai.ai import BaseAI
import pstats, cProfile
import random
import time
from copy import deepcopy
import numpy as np


# statistics for nerds:
VERBOSE = True
PRUNING = (0, 0, 0)

def pruning_statistics(root_node: bool) -> None:
    if root_node:
        PRUNING[0] += 1
    else:
        PRUNING[1] += 1


class AlphaBeta(BaseAI):
    def __init__(self, player: Player, cannon: CannonGame, alpha: int, beta: int, depth: int, 
                    time_limit: int, weights: List[int], use_tt: bool = True, always_sort: bool = False,
                    quiesence: bool = True, soft_bounds: bool = True) -> None:
        super().__init__(player, cannon)

        self._moves = None
        self._moves_generator = MoveGenerator()
        
        # get the initial alpha-beta window (-∞, +∞)
        self._alpha = alpha
        self._beta = beta
        self._found_finishing_move = False

        # get the depth and weight values, as well as the configuration for
        # refreshing the transposition table after each move
        # also sorting always can be enabled or be disabled
        self._depth = depth
        self._extra_depth = 0
        self._delta_depth = 2

        self._weights = np.asarray(weights)
        self._use_tt = use_tt
        self._always_sort = always_sort

        # iterative deepening, if not time limit is given, then set a max of 10 minute
        self._time_start = 0
        self._time_limit = time_limit

        self._quiesence_enabled = quiesence
        self._soft_bounds = soft_bounds

        # create the transposition table container
        self._tt = dict()
    
    def statistics_get(self, key: str = None):
        return self._stats.get(key)

    def play_turn(self, state: Dict) -> bool:
        """
        This method lets the agent calculate the best move. If there is no possible 
        move, then this function returns false. Otherwise the move is registered and true 
        returned.
        """

        with cProfile.Profile() as pr:
            best_move, time_needed = self._run_search()

            # pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE).print_stats(10)
            
        # add statistics
        if best_move:
            self._stats.add_move(best_move.get_value())

        self._stats.add_ply(self._extra_depth - self._delta_depth, time_needed)
        self._stats.update()

        if VERBOSE:
            print(self._stats.get_printable())

        # if the best move was not found after the given search time, then check if any moves are available
        # then return the first of those moves. Better doing sth. instead of nothing :)
        if not best_move:
            enemy = self._cannon._get_enemy_player(self._player)
            moves = self._moves_generator.generate_moves(self._player, enemy)
            if len(moves) == 0:
                self._cannon.end_game(enemy.get_type())
                return True
            
            best_move = moves[0]

        # finally execute the move and register it in the game's state
        self._cannon.execute(self._player, best_move)

        # clean up the transposition table
        self._tt = dict()
        
        return True
    
    def _run_search(self) -> Tuple[Move, float]:
         # remember the start time for iterative deepening
        self._time_start = time.time()
        time_exceeded = False
        time_needed = 0

        # set the depth, which will increased if enough time is available
        self._extra_depth = self._depth

        self._found_finishing_move = False
        best_move = move = None
        while not time_exceeded:
            # safe the best move found so far and ingore the "best move" found on the current ply
            # this ply could be interrupted cause the time has exceeded
            best_move = move
            score, move = self._algorithm(self._alpha, self._beta, self._extra_depth, self._player)

            # search deeper if the time has not exceeded yet
            # increasing depth by two, to avoid the odd/even affect
            self._extra_depth += self._delta_depth
            time_needed = time.time() - self._time_start
            time_exceeded = time_needed > self._time_limit if self._time_limit else True

            # if the given move results in finishing the game, but the time is not over, then
            # return this move anyway!
            if self._found_finishing_move:
                best_move = move
                break

        # if the best move is still none, then take the found move even it could be not the best
        # but this is still better than nothing
        if not best_move:
            best_move = move
        
        return best_move, time_needed

    def set_town_position(self, positions: List[Move]) -> Move:
        """
        This method places a position for the town randomly
        """
        position = random.choice(positions)
        return position

    def _get_moves(self, player) -> List[Move]: 
        """
        Generates all moves for each soldier of the current player given as an argument.
        """
        if self._always_sort:
            return self._get_moves_sorted(player)

        return self._moves_generator.generate_moves(player, self._cannon._get_enemy_player(player))

    def _get_moves_sorted(self, player) -> List[Move]:
        """
        Generates all moves for each soldier of the current player given as an argument.
        Also each move is evaluated and afterwards the list of moves is sorted by their values.
        """
        moves = self._moves_generator.generate_moves(player, self._cannon._get_enemy_player(player))

        for m in moves:
            score = self._eval(player, m)
            m.set_value(score)

        self._sort_moves(moves)
        return moves

    def _sort_moves(self, moves: List[Move]):
        """
        Simple method for sorting a list of moves. This single line is put into an extra 
        method so profiling the code is easier.
        """
        moves.sort(key=lambda m: m._value, reverse=True)
    
    def _eval(self, player: Player, move: Move) -> int:
        return self._cannon.eval(player, move, self._weights)

    def _algorithm(self, alpha: int, beta: int, depth: int, player: Player) -> Tuple[int, Move]:
        """
        The algorithm calcualtes the best move using the Alpha Beta algorithm combined with Iterative Deepening
        and a Transposition Table.
        """
        time_exceeded = time.time() - self._time_start > self._time_limit if self._time_limit else False
        # if time_exceeded:
        #     return math.inf, None

        # if the maximum depth is reached, then return the best move
        # also, get the current time to check if the search should end
        if(depth == 0 or time_exceeded):
            if self._quiesence_enabled:
                score = self._quiesence(alpha, beta, player)
            else:
                score = self._get_moves_sorted(player)[0].get_value()
            return score, None

        # create a best score for a fail soft
        best_score = -math.inf if self._soft_bounds else alpha
        moves = None

        # check if there is already a best move known, before running the search
        # this optimization uses the "transposition table" and the "zobrist hashing"
        best_move = None
        if self._use_tt:
            tt_hash = self._cannon.hash(player.get_type())
            best_move = self._tt.get(tt_hash, None)

        if best_move:
            # loading the best move known and set it to the beginning of the list of
            # avialable moves
            self._stats.add_move_loaded(best_move.get_value())
            moves = [best_move] + self._get_moves(player)
        else:
            moves = self._get_moves(player)

        for move in moves:
            # if there is a fnishing move, do a hard break
            # and force the AI to play into this direction
            if move.is_finish_move() and player.get_type() == self._player.get_type():
                best_score = move.get_value() # move.get_score
                if not best_score:
                    score = self._eval(player, move)
                    move.set_value(score)
                    best_score = score

                best_move = move
                self._found_finishing_move = True
                break

            self._cannon.execute(player, move, testing_only=True)
            enemy = self._cannon._get_enemy_player(player)
            # do the recursion step
            score, _ = self._algorithm(-1 * beta, -1 * alpha, depth - 1, enemy)
            score *= -1

            # undo the recursion step
            self._cannon.undo(player, move)

            if score >= beta:
                # fail soft -> beta cut off
                # this is the pruning part
                self._stats.add_pruning(depth == self._extra_depth)
                return score, move

            if self._soft_bounds:
                if score > best_score:
                    best_score = score
                    if score > alpha:
                        alpha = score

                    # save the best move so far
                    best_move = move
            else:
                if score > alpha:
                    alpha = best_score = score
                    best_move = move
        
        if self._use_tt and best_move:
            stored = self._tt.get(best_move, None)
            if stored is not None:
                raise ValueError("Multiple hashes are not valid!")

            self._stats.add_move_stored(best_move.get_value())
            self._tt[tt_hash] = deepcopy(best_move)

        return best_score, best_move
    
    def _quiesence(self, alpha: int, beta: int, player: Player) -> int:
        """
        A variable depth search approach, that searches for a quiete move and then evaluates.
        """
        moves = self._get_moves(player)
        for move in moves:
            # if the move is a finishing one, then defenitly use this one!
            if move.is_finish_move():
                self._found_finishing_move = player.get_type() == self._player.get_type()
                # score = -100_000 if player.get_type() != self._player.get_type() else 100_000
                # factor = -1 if player.get_type() != self._player.get_type() else 1
                return move.get_value() # * factor
            
            # if the move is quiet, the evaluate it
            if not move.is_kill_move():
                # get the scores value, or evaluate it
                score = move.get_value()
                if not score:
                    score = self._eval(player, move)
                    move.set_value(score)
                
                # score = -score if player.get_type() != self._player.get_type() else score
                # factor = -1 if player.get_type() != self._player.get_type() else 1
                return score # * factor

            # search deeper if the move was not quiete
            self._cannon.execute(player, move, testing_only=True)
            enemy = self._cannon._get_enemy_player(player)
            score = -self._quiesence(-alpha, -beta, enemy)
            self._cannon.undo(player, move)
                        
            if score >= beta:
                return beta
            if alpha < score:
                alpha = score
        
        return alpha
    
    def to_dict(self) -> dict:
        d = dict()
        d["ai_type"] = "ab"
        d["p"] = self._player.get_type()
        d["a"] = self._alpha
        d["b"] = self._beta
        d["d"] = self._depth
        d["t"] = self._time_limit
        d["w"] = self._weights
        d["r"] = self._use_tt
        d["s"] = self._always_sort
        return d
    
    def from_dict(d: dict, player: Player, cannon: CannonGame):
        return AlphaBeta(player, cannon, d["a"], d["b"], d["d"], d["t"], d["w"], d["r"], d["s"])