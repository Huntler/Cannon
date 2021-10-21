import math
from stupid_engine.cannon.ai.move_generator import MoveGenerator
from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.entities.figures import CannonFigure, CannonSoldier
from stupid_engine.cannon.entities.player import Player, PlayerType
from typing import Dict, List, Tuple
import random
import functools
from copy import copy
from multiprocessing import Pool


class CannonGame:
    def __init__(self, p_light: Player, p_dark: Player) -> None:
        self._p_light = p_light
        self._p_dark = p_dark

        self._on_finish_callback = None

        # initialize random values for the zobrist hashing
        # one entry for each piece at eache square and one entry for the player playing
        self._zobrist_player = (random.randint(0, 2**64 - 1), random.randint(0, 2**64 - 1))
        self._zobrist = [[[random.randint(0, 2**64 - 1) for _ in range(4)] for _ in range(10)] for _ in range(10)]
    
    def set_on_finish(self, callback) -> None:
        self._on_finish_callback = callback
    
    def _get_enemy_player(self, player: Player) -> Player:
        return self._p_dark if player == self._p_light else self._p_light
    
    def hash(self, player_type: PlayerType, state: Dict = None):
        """
        Uses Zobrist hash function to calulate the hash of the current board state.
        """
        if state is None:
            state = self.get_state()

        hash = 0

        # iterate over every piece and get its random value
        # then store the random value into the has container using XOR
        for soldier in state[PlayerType.LIGHT][0]:
            x, y = soldier
            hash ^= self._zobrist[x][y][0]
        
        if state[PlayerType.LIGHT][1]:
            x, y = self._p_light.get_town().get_pos()
            hash ^= self._zobrist[x][y][1]
        
        for soldier in state[PlayerType.DARK][0]:
            x, y = soldier
            hash ^= self._zobrist[x][y][2]
        
        if state[PlayerType.DARK][1]:
            x, y = self._p_dark.get_town().get_pos()
            hash ^= self._zobrist[x][y][3]

        player_index = 0 if player_type == PlayerType.LIGHT else 1
        hash ^= self._zobrist_player[player_index]

        return hash     

    def eval(self, player: Player, move: Move, weights: List[int]) -> int:
        """
        This method is used to evaluate a move made by the given player. Features 
        considerd in this function are:
            - if the move is a finish move
            - if the move is a shooting move
            - if the move is killing a soldier
            - if the move saves a soldier
            - the difference of army size
        """
        enemy = self._get_enemy_player(player)

        value = 0
        if move.is_finish_move():
            value += weights[2]
        
        if move.is_shoot():
            value += weights[5]
        
        if move.is_kill_move():
            value += weights[7]
        
        if move.is_retreat_move():
            value += weights[4]
        
        if move.is_sliding_move():
            value += 1
        
        # check if the move adds a soldier to the defense wall
        # .....
        # .sss.
        # .sts.
        #--------
        tx, ty = player.get_town().get_pos()
        d = 1 if player.get_type() == PlayerType.DARK else -1
        for denfense_pos in [(tx - 1, ty + d), (tx, ty + d), (tx + 1, ty + d), (tx - 1, ty), (tx + 1, ty)]:
            if denfense_pos == move.get_pos() or player.soldier_at(denfense_pos):
                value += 1 * weights[3]
        
        # moving an enemy that is closer to the town should reward
        # closer to a town is more rewarded
        # check if the soldier is able to reach the enemies town
        # otherwise, the soldier should not be rewarded to be close to the enemies town
        enemy_town_x, enemy_town_y = enemy.get_town().get_pos()
        move_x, move_y = move.get_pos()
        
        dir_x = 1 if enemy_town_x > move_x else -1
        vec_x = abs(enemy_town_y - move_y) * dir_x
        if move_x + vec_x - enemy_town_x > -2:
            enemy_town_distance_func = lambda x, y: math.pow(enemy_town_x - x, 2) + math.pow(enemy_town_y - y, 2)
            enemy_town_distance = math.sqrt(enemy_town_distance_func(move_x, move_y))
            enemy_town_distance = round(enemy_town_distance)
            value += (10 - enemy_town_distance) * weights[0]

            # the move that results in a closer distance to the enmies town should be rewarded as well
            # but reatreating or sliding backwards should not be punished!
            origin_x, origin_y = move.get_original_pos()
            delta_enemy_town_distance = math.sqrt(enemy_town_distance_func(origin_x, origin_y))
            delta_enemy_town_distance = max(round(delta_enemy_town_distance) - enemy_town_distance, 0)
            value += delta_enemy_town_distance * weights[1]

        # more soldiers is better 
        kill = 1 if move.is_kill_move() else 0
        value += (player.army_size() - (enemy.army_size() - kill)) * weights[6]

        return value

    def execute(self, player: Player, move: Move, testing_only=False) -> None:
        """
        This method executes the move of a given soldier.
        """
        # get the opponent player
        enemy = self._get_enemy_player(player)
        soldier = player.soldier_at(move.get_original_pos())

        # if the player won the game, then quit
        if move.is_finish_move():
            msg = "climbed the town's walls"
            
            if move.is_shoot():
                msg = "bombed the town down"

            if not testing_only:
                print(f"{player.get_type()}: {soldier.get_pos()} -> {move.get_pos()}, {msg}!")
                player.move_soldier(move)  
                self.end_game(player.get_type())

        # remove the enemy soldier if the move is a shoot
        elif move.is_shoot():
            if enemy.soldier_at(move.get_pos()):
                if not testing_only:
                    print(f"{player.get_type()}: {soldier.get_pos()} -> {move.get_pos()} and hits an enemy!")
                enemy.remove_at(move.get_pos())

        # remove an enemy if this is a kill move
        elif move.is_kill_move():
            if not testing_only:
                print(f"{player.get_type()}: {soldier.get_pos()} -> {move.get_pos()}, swordfight won!")
            enemy.remove_at(move.get_pos())
            player.move_soldier(move)
        
        # just move the soldier
        else:
            msg = "what a rough ground"
            if move.is_retreat_move():
                msg = "what a coward"
            
            if move.is_sliding_move():
                msg = "those cannons are heavy"

            if not testing_only:
                print(f"{player.get_type()}: {soldier.get_pos()} -> {move.get_pos()}, {msg}.")
            player.move_soldier(move)  

    def undo(self, player: Player, move: Move):
        enemy = self._get_enemy_player(player)

        # get the soldier and move it back to its original position
        soldier = player.soldier_at(move.get_pos())
        if soldier:
            # remove the soldier from the army
            player.remove_at(move.get_pos())

            # set the soldier to its original position in the army
            player_army = player.get_soldiers()
            player_army[move.get_original_pos()] = soldier
            soldier.set_pos(move.get_original_pos())

        # restore a killed enemy
        killed = move.get_killed_pos()
        if killed:
            enemies_army = enemy.get_soldiers()
            enemies_army[killed] = CannonSoldier(killed)
        
        if not soldier and not killed and not move.is_finish_move():
            raise ValueError("The move is invalid!")

    def get_town_positions(self, turn: PlayerType) -> List[Move]:
        """
        This method gets all possible positions to place a town for the given player.
        """
        towns = []
        # get all possible positions for a town
        y = 9 if turn == PlayerType.LIGHT else 0
        for x in range(1, 9):
            towns.append(Move((x, y), None))

        return towns

    def end_game(self, player_type: PlayerType):
        """
        This method should be called if the game ends. The given type 
        determines the winner.
        """
        self._on_finish_callback(player_type)
    
    def get_player(self, type: PlayerType) -> Player:
        if type == PlayerType.LIGHT:
            return self._p_light
        
        return self._p_dark

    def get_state(self) -> Dict:
        """
        This method summarizes the current game state.
        """
        state = {}

        state[PlayerType.LIGHT] = self._p_light.get_state()
        state[PlayerType.DARK] = self._p_dark.get_state()

        return state