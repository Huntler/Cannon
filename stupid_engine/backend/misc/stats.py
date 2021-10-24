from os import stat
import numpy as np

from stupid_engine.cannon.entities.player import PlayerType


class Statistics:

    ROOT_PRUNING = "roopru"
    AVERAGE_SUBROOT_PRUNING = "avesub"
    MIN_SUBROOT_PRUNING = "minsub"
    MAX_SUBROOT_PRUNING = "maxsub"
    AVERAGE_PRUNING = "avepru"

    AMOUNT_OF_MOVES = "amomov"
    TOTAL_SCORE = "totsco"
    TOTAL_SCORE_NORMALIZED = "totnor"

    MIN_PLY = "minply"
    MAX_PLY = "maxply"
    AVERAGE_PLYS = "aveply"
    AVERAGE_TIME_PER_PLY = "avgtim"

    MOVES_STORED = "movsto"
    MOVES_LOADED = "movload"

    def __init__(self, player_type: PlayerType) -> None:
        self._player_type = player_type
        self._index = 0

        # create variables for the amount of pruning
        self._root_pruning = []
        self._sub_root_pruning = []
        self._pruning = []

        # create variables for the amount of moves calculated
        self._moves = []

        # create variables for the amount of time for each ply
        # and how many plys were calculated
        self._plys = []
        self._time_plys = []

        # statistics for iterative deepening / transposition table
        self._moves_in_tt = []
        self._moves_restored_tt = []

    def add_pruning(self, root_node) -> None:
        if len(self._root_pruning) <= self._index:
            self._root_pruning.append(0)
            self._sub_root_pruning.append(0)

        if root_node:
            self._root_pruning[self._index] += 1
        else:
            self._sub_root_pruning[self._index] += 1
    
    def add_move(self, score: int) -> None:
        if np.inf == np.abs(score):
            return

        self._moves.append(score)
    
    def add_ply(self, depth_searched: int, time_needed: int) -> None:
        self._plys.append(depth_searched)
        self._time_plys.append(time_needed)
    
    def add_move_stored(self, score) -> None:
        self._moves_in_tt.append(score)

    def add_move_loaded(self, score) -> None:
        self._moves_restored_tt.append(score)

    def get(self, key: str = None):
        stats = dict()

        # pruning stats
        min_sub = max_sub = avg_sub = avg_root = avg_pru = 0

        if len(self._sub_root_pruning) > 0:
            min_sub = np.min(self._sub_root_pruning)
            max_sub = np.max(self._sub_root_pruning)
            avg_sub = np.average(self._sub_root_pruning)

        if len(self._root_pruning) > 0:
            avg_root = np.average(self._root_pruning)
        
        if len(self._pruning) > 0:
            avg_pru = np.average(self._pruning)

        stats[Statistics.ROOT_PRUNING] = avg_root
        stats[Statistics.MIN_SUBROOT_PRUNING] = min_sub
        stats[Statistics.MAX_SUBROOT_PRUNING] = max_sub
        stats[Statistics.AVERAGE_SUBROOT_PRUNING] = avg_sub
        stats[Statistics.AVERAGE_PRUNING] = avg_pru

        # moves stats
        amount_mov = total_score = total_score_norm = 0
        if len(self._moves) > 0:
            amount_mov = len(self._moves)
            total_score = np.sum(self._moves)
            total_score_norm = total_score / amount_mov

        stats[Statistics.AMOUNT_OF_MOVES] = amount_mov
        stats[Statistics.TOTAL_SCORE] = total_score
        stats[Statistics.TOTAL_SCORE_NORMALIZED] = total_score_norm

        # iterative deepening / ply stats
        min_ply = max_ply = avg_ply = avg_time = 0
        if len(self._plys) > 0:
            min_ply = np.min(self._plys)
            max_ply = np.max(self._plys)
            avg_ply = np.average(self._plys)
            avg_time = np.average(np.asarray(self._plys) / np.asarray(self._time_plys))

        stats[Statistics.MIN_PLY] = min_ply
        stats[Statistics.MAX_PLY] = max_ply
        stats[Statistics.AVERAGE_PLYS] = avg_ply
        stats[Statistics.AVERAGE_TIME_PER_PLY] = avg_time

        stored_moves = loaded_moves = 0
        if len(self._moves_in_tt) > 0:
            stored_moves = len(self._moves_in_tt)
        if len(self._moves_restored_tt) > 0:
            loaded_moves = len(self._moves_restored_tt)
        
        stats[Statistics.MOVES_LOADED] = loaded_moves
        stats[Statistics.MOVES_STORED] = stored_moves

        if not key:
            return stats
        
        return stats[key]
    
    def get_printable(self, key: str = None) -> str:
        s = ""
        if not key:
            s = f"Player: {self._player_type}\n" + \
                f"Amount of moves: \t{self.get(Statistics.AMOUNT_OF_MOVES)}\n" + \
                f"Total score: \t\t{self.get(Statistics.TOTAL_SCORE)}\n" + \
                f"Depth for move:\n" + \
                f"\tavg:\t\t{self.get(Statistics.AVERAGE_PLYS)}\n" + \
                f"\tmin:\t\t{self.get(Statistics.MIN_PLY)}\n" + \
                f"\tmax:\t\t{self.get(Statistics.MAX_PLY)}\n" + \
                f"\ttime:\t\t{self.get(Statistics.AVERAGE_TIME_PER_PLY)}\n" + \
                f"Transposition Table: \n" + \
                f"\tStored moves:\t{self.get(Statistics.MOVES_STORED)}\n" + \
                f"\tLoaded moves:\t{self.get(Statistics.MOVES_LOADED)}\n" + \
                f"Root pruning: \t\t{self.get(Statistics.ROOT_PRUNING)}\n" + \
                f"Subroot pruning:\n" + \
                f"\tavg: \t\t{self.get(Statistics.AVERAGE_SUBROOT_PRUNING)}\n" + \
                f"\tmin: \t\t{self.get(Statistics.MIN_SUBROOT_PRUNING)}\n" + \
                f"\tmax: \t\t{self.get(Statistics.MAX_SUBROOT_PRUNING)}\n" + \
                f"Average pruning: \t{self.get(Statistics.AVERAGE_PRUNING)}\n"
        
        return s

    def update(self) -> None:
        i = self._index

        # calculated the amount of pruning
        if len(self._sub_root_pruning) > i and self._sub_root_pruning[i] != 0:
            self._pruning.append(self._root_pruning[i] / self._sub_root_pruning[i])
        else:
            self._pruning.append(0)

        self._index += 1