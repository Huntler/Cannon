from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.entities.figures import CannonSoldier
from stupid_engine.cannon.entities.player import Player, PlayerType
from typing import Dict, List, Tuple


class CannonGame:
    def __init__(self, p_light: Player, p_dark: Player) -> None:
        self._p_light = p_light
        self._p_dark = p_dark

        self._on_finish_callback = None
    
    def set_on_finish(self, callback) -> None:
        self._on_finish_callback = callback
    
    def _get_enemy_player(self, player: Player) -> Player:
        return self._p_dark if player == self._p_light else self._p_light
    
    def eval(self, player: Player, move: Move) -> None:
        """
        This method is used to evaluate a move made by the given player. Features 
        considerd in this function are:
            - if the move is a finish move
            - if the move is a shooting move
            - if the move is killing a soldier
            - if the move saves a soldier
            - the difference of army size
            
            - the difference of possible moves  TODO
            - the difference of cannons         TODO
        """
        enemy = self._get_enemy_player(player)
        # finish, shoot, kill, retreat, army size
        weights = [100, 3, 3, 1, 5]

        value = 0
        if move.is_finish_move():
            value += weights[0]
        
        if move.is_shoot():
            value += weights[1]
        
        if move.is_kill_move():
            value += weights[2]
        
        if move.is_retreat_move():
            value += weights[3]

        # more soldiers is better 
        value += (player.army_size() - enemy.army_size()) * weights[4]
        return value
    
    def moves(self, player: Player, soldier: CannonSoldier) -> List[Move]:
        """
        This method calulated possible moves of the given soldier.
        """
        # get the opponent player
        enemy = self._get_enemy_player(player)

        # determine the direction in which the current player is playing
        x, y = soldier.get_pos()
        dir = -1 if player.get_type() == PlayerType.LIGHT else +1
        
        # create the basic movement moves: front_left, front, front_right
        # this includes checking if a enemy soldier or the enemy town is placed 
        # in this position. This move is then marked as kill / finishing move.
        moves = []
        for move in [(x - 1, y + dir), (x, y + dir), (x + 1, y + dir)]:
            if not Move.out_of_bounds(move) and not player.soldier_at(move) and player.get_town().get_pos() != move:
                # is a killing move
                to_kill = enemy.soldier_at(move)

                # is a finishing move
                finish = None
                if enemy.is_town_placed() and move == enemy.get_town().get_pos():
                    finish = enemy.get_town()

                moves.append(Move(pos=move, soldier=soldier, finish=finish, kill=to_kill))
        
        # create the capture / kill moves
        for move in [(x - 1, y), (x + 1, y)]:
            if not Move.out_of_bounds(move) and not player.soldier_at(move):
                # is a killing move
                to_kill = enemy.soldier_at(move)
                if to_kill is None:
                    continue

                # is a finishing move
                finish = None
                if enemy.is_town_placed() and move == enemy.get_town().get_pos():
                    finish = enemy.get_town()

                moves.append(Move(pos=move, soldier=soldier, finish=finish, kill=to_kill))

        # retreat move if the soldier is threatened
        # the possible moves are 2 places behind the soldier and two places left/right of that position
        for threat in [(x - 1, y + dir), (x, y + dir), (x + 1, y + dir), (x - 1, y), (x + 1, y)]:
            if enemy.soldier_at(threat):
                for move in [(x - 2, y - 2 * dir), (x, y - 2 * dir), (x + 2, y - 2 * dir)]:
                    if not Move.out_of_bounds(move) and not player.soldier_at(move) and not enemy.soldier_at(move) and player.get_town().get_pos() != move:
                        moves.append(Move(pos=move, soldier=soldier, retreat=True))
        
        # recognize a cannon and find possible moves for it
        # check for 3 adjacent soldiers
        # structure of the lists: 
        # [soldiers needed for cannon; possible positions for shoots; 
        #   free position for shoot; slide position]
        cannon_cases = [
            # orthogonal row, given soldier front
            [[(x, y - dir), (x, y - 2 * dir)], [(x, y + 2 * dir), (x, y + 3 * dir)], (x, y + dir), (x, y - 3 * dir)],
            # 3 in a orthogonal row, given soldier back
            [[(x, y + dir), (x, y + 2 * dir)], [(x, y - 2 * dir), (x, y - 3 * dir)], (x, y - dir), (x, y + 3 * dir)],
            # 3 in a diagonal row, given soldier front (right)
            [[(x - 1, y - dir), (x - 2, y - 2 * dir)], [(x + 2, y + 2 * dir), (x + 3, y + 3 * dir)], (x + dir, y + dir), (x - 3, y - 3 * dir)],
            # 3 in a diagonal row, given soldier back (right)
            [[(x + 1, y + dir), (x + 2, y + 2 * dir)], [(x - 2, y - 2 * dir), (x - 3, y - 3 * dir)], (x - dir, y - dir), (x + 3, y + 3 * dir)],
            # 3 in a diagonal row, given soldier back (left)
            [[(x - 1, y + dir), (x - 2, y + 2 * dir)], [(x + 2, y - 2 * dir), (x + 3, y - 3 * dir)], (x + dir, y - dir), (x - 3, y + 3 * dir)],
            # 3 in a diagonal row, given soldier front (left)
            [[(x + 1, y - dir), (x + 2, y - 2 * dir)], [(x - 2, y + 2 * dir), (x - 3, y + 3 * dir)], (x - dir, y + dir), (x + 3, y - 3 * dir)]
        ]

        for structure, shots, free, slide in cannon_cases:
            # check if there is a cannon structure
            structure_exists = True
            for pos in structure:
                if Move.out_of_bounds(pos) or not player.soldier_at(pos):
                    structure_exists = False
            
            if not structure_exists:
                continue
            
            # if the given place is empty
            if not Move.out_of_bounds(slide) and not enemy.soldier_at(slide) and not player.soldier_at(slide)  and player.get_town().get_pos() != move and enemy.get_town().get_pos() != move:
                moves.append(Move(pos=slide, soldier=soldier, slide=True))
            
            # check if there is the free position in front available so the cannon can shoot
            if Move.out_of_bounds(free) or enemy.soldier_at(free) or player.soldier_at(free):
                continue

            # add possible shot positions
            for move in shots:
                if not Move.out_of_bounds(move):
                    # if the shoot will hit a town, then mark this as finishing move
                    if enemy.get_town().get_pos() == move:
                        moves.append(Move(pos=move, soldier=soldier, finish=enemy.get_town(), shoot=True))
                        break

                    # if the shoot will hit a solider of this player, than skip
                    if player.soldier_at(move):
                        break

                    # if the shoot wil hit an enemy soldier, then mark this move as 
                    # shoot/kill and break
                    if enemy.soldier_at(move):
                        moves.append(Move(pos=move, soldier=soldier, kill=enemy.soldier_at(move), shoot=True))
                        break
        
        return moves

    def execute(self, player: Player, move: Move, testing_only=False) -> None:
        """
        This method executes the move of a given soldier.
        """
        # get the opponent player
        enemy = self._get_enemy_player(player)
        soldier = move.get_soldier()

        # if the player won the game, then quit
        if move.is_finish_move():
            msg = "climbed the town's walls"
            
            if move.is_shoot():
                msg = "bombed the town down"

            if not testing_only:
                print(f"{player.get_type()}: {soldier.get_pos()} -> {move.get_pos()}, {msg}!")
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

    def get_town_positions(self, turn: PlayerType) -> List[Move]:
        """
        This method gets all possible positions to place a town for the given player.
        """
        towns = []
        # get all possible positions for a town
        y = 9 if turn == PlayerType.LIGHT else 0
        for x in range(0, 10):
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

    def undo(self, player: Player, move: Move):
        enemy = self._get_enemy_player(player)

        # get the soldier and move it back to its original position
        soldier = move.get_soldier()
        soldier.set_pos(move.get_original_pos())

        # restore a killed enemy
        killed = move.get_enemy_killed()
        if killed:
            enemies_army = enemy.get_soldiers()
            enemies_army.append(killed)

    def get_state(self) -> Dict:
        """
        This method summarizes the current game state.
        """
        state = {}

        state[PlayerType.LIGHT] = self._p_light.get_state()
        state[PlayerType.DARK] = self._p_dark.get_state()

        return state