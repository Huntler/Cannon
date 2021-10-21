from stupid_engine.cannon.entities.figures import CannonSoldier
from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.entities.player import Player, PlayerType
from typing import List
from copy import copy
import functools


class MoveGenerator:
    def __init__(self) -> None:
        self._moves = []

    def generate_moves(self, player, enemy, soldier=None) -> List[Move]:
        self.refresh()
        if soldier:
            self._generate_moves(player, enemy, soldier, for_ai=False)
            return self._moves

        for soldier in player.get_soldiers().values():
            self._generate_moves(player, enemy, soldier)

            # force a end move
            if len(self._moves) == 1 and self._moves[0].is_finish_move():
                return self._moves
        
        return self._moves
       
    def _generate_moves(self, player, enemy, soldier, for_ai=True) -> Move:
        # determine the direction in which the current player is playing
        d = -1 if player.get_type() == PlayerType.LIGHT else +1
        x, y = soldier.get_pos()
        
        #
        #   STANDARD MOVES
        #

        # create the basic movement moves: front_left, front, front_right
        # this includes checking if a enemy soldier or the enemy town is placed 
        # in this position. This move is then marked as kill / finishing move.
        for move in [(x, y + d), (x - 1, y + d), (x + 1, y + d)]:
            if Move.out_of_bounds(move) or player.soldier_at(move):
                continue

            # other moves are not interesting if the player can finish the game
            town = enemy.get_town().get_pos() == move
            if town:
                town_move = Move(pos=move, soldier=soldier.get_pos(), finish=town)
                if for_ai:
                    self._moves = [town_move]
                    return
                else:
                    self._moves.append[town_move]
                    continue


            kill = enemy.soldier_at(move)
            if kill:
                kill = kill.get_pos()
                self._moves.insert(0, Move(pos=move, soldier=soldier.get_pos(), kill=kill))

            else:
                self._moves.append(Move(pos=move, soldier=soldier.get_pos()))
        
        # create the capture / kill moves
        for move in [(x - 1, y), (x + 1, y)]:
            # other moves are not interesting if the player can finish the game
            town = enemy.get_town().get_pos() == move
            if town:
                town_move = Move(pos=move, soldier=soldier.get_pos(), finish=town)
                if for_ai:
                    # moves.insert(0, Move(pos=move, soldier=soldier.get_pos(), finish=town))
                    self._moves = [town_move]
                    return
                else:
                    self._moves.append[town_move]
                    continue

            kill = enemy.soldier_at(move)
            if kill:
                kill = kill.get_pos()
                self._moves.insert(0, Move(pos=move, soldier=soldier.get_pos(), kill=kill))

        #
        #   CANNON MOVES
        #

        # recognize a cannon and find possible moves for it
        # check for 3 adjacent soldiers
        # structure of the lists: 
        # [soldiers needed for cannon; possible positions for shoots; 
        #   free position for shoot; slide position]
        cannon_cases = [

            # orthogonal row, given soldier front
            [[(x, y), (x, y - 2)], [(x, y + 2), (x, y + 3)], (x, y + 1), (x, y - 3)],
            # 3 in a orthogonal row, given soldier back
            [[(x, y), (x, y + 2)], [(x, y - 2), (x, y - 3)], (x, y - 1), (x, y + 3)],

            # 3 in a diagonal row, given soldier front (right)
            [[(x - 1, y - 1), (x - 2, y - 2)], [(x + 2, y + 2), (x + 3, y + 3)], (x + 1, y + 1), (x - 3, y - 3)],
            # 3 in a diagonal row bottom-left to top-right
            [[(x + 1, y + 1), (x + 2, y + 2)], [(x - 2, y - 2), (x - 3, y - 3)], (x - 1, y - 1), (x + 3, y + 3)],
            # 3 in a diagonal row, given soldier back (left)
            [[(x - 1, y + 1), (x - 2, y + 2)], [(x + 2, y - 2), (x + 3, y - 3)], (x + 1, y - 1), (x - 3, y + 3 )],
            # 3 in a diagonal row, given soldier front (left)
            [[(x + 1, y - 1), (x + 2, y - 2)], [(x - 2, y + 2), (x - 3, y + 3)], (x - 1, y + 1), (x + 3, y - 3)]
        ]

        for structure, shots, free, slide in cannon_cases:
            # check if there is a cannon structure
            structure_exists = True
            for pos in structure:
                if Move.out_of_bounds(pos) or not player.soldier_at(pos):
                    structure_exists = False
                    break
            
            if not structure_exists:
                continue

            # if the given place is empty
            if not Move.out_of_bounds(slide) and not enemy.soldier_at(slide) and not player.soldier_at(slide) and player.get_town().get_pos() != slide and enemy.get_town().get_pos() != slide:
                self._moves.append(Move(pos=slide, soldier=soldier.get_pos(), slide=True))
            
            # check if there is the free position in front available so the cannon can shoot
            if Move.out_of_bounds(free) or enemy.soldier_at(free) or player.soldier_at(free):
                continue

            # check shot positions first, maybe the player can end the game. In this case other 
            # moves are not interesting!
            # add possible shot positions
            for shot in shots:
                # if the shoot will hit a solider of this player, than skip
                if Move.out_of_bounds(shot) or player.soldier_at(shot):
                    break
            
                # if the shoot will hit a town, then mark this as finishing move and return just this move
                # other moves are not interesting if the player is able to end the game
                town = enemy.get_town().get_pos()
                if town == shot:
                    town_move = Move(pos=move, soldier=soldier.get_pos(), finish=town, shoot=True)
                    if for_ai:
                        # moves.insert(0, Move(pos=move, soldier=soldier.get_pos(), finish=town))
                        self._moves = [town_move]
                        return
                    else:
                        self._moves.append[town_move]
                        continue
                
                # if the shoot wil hit an enemy soldier, then mark this move as 
                # shoot/kill and break
                kill = enemy.soldier_at(shot)
                if kill:
                    self._moves.append(Move(pos=shot, soldier=soldier.get_pos(), kill=kill.get_pos(), shoot=True))
                    break

        #
        #   RETREAT MOVES
        #

        # retreat move if the soldier is threatened
        # the possible moves are 2 places behind the soldier and two places left/right of that position
        retreat_pos = [
            [(x - 2, y - 2 * d), (x - 1, y - d)], 
            [(x, y - 2 * d), (x, y - d)], 
            [(x + 2, y - 2 * d), (x + 1, y - d)]
        ]
        for threat in [(x - 1, y + d), (x, y + d), (x + 1, y + d), (x - 1, y), (x + 1, y)]:
            if enemy.soldier_at(threat):
                for move, free in retreat_pos:
                    if Move.out_of_bounds(move) or player.get_town().get_pos() == move or player.soldier_at(free) or enemy.soldier_at(free):
                        continue

                    if not player.soldier_at(move) and not enemy.soldier_at(move):
                        self._moves.append(Move(pos=move, soldier=soldier.get_pos(), retreat=True))

    def refresh(self) -> None:
        self._moves = []

