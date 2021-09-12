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
    
    def moves(self, player: Player, soldier: CannonSoldier) -> List[Move]:
        """
        This method calulated possible moves of the given soldier.
        """
        # check if player owns a town
        if not player.is_town_placed():
            print("CannonGame.moves: The town was not placed yet.")
            quit()

        # get the opponent player
        enemy = self._p_dark if player == self._p_light else self._p_light

        # determine the direction in which the current player is playing
        x, y = soldier.get_pos()
        dir = -1 if player.get_type() == PlayerType.LIGHT else +1
        
        # create the basic movement moves: front_left, front, front_right
        # this includes checking if a enemy soldier or the enemy town is placed 
        # in this position. This move is then marked as kill / finishing move.
        moves = []
        for move in [(x - 1, y + dir), (x, y + dir), (x + 1, y + dir)]:
            if not Move.out_of_bounds(move) and not player.soldier_at(move):
                # is a killing move
                kill_move = enemy.soldier_at(move)

                # is a finishing move
                finish_move = enemy.is_town_placed() and move == enemy.get_town_position()
                moves.append(Move(pos=move, finish_move=finish_move, kill_move=kill_move))
        
        # create the capture / kill moves
        for move in [(x - 1, y), (x + 1, y)]:
            if not Move.out_of_bounds(move) and not player.soldier_at(move):
                # is a killing move
                kill_move = enemy.soldier_at(move)

                # is a finishing move
                finish_move = enemy.is_town_placed() and move == enemy.get_town_position()
                if kill_move or finish_move:
                    moves.append(Move(pos=move, finish_move=finish_move, kill_move=kill_move))

        # retreat move if the soldier is threatened
        # the possible moves are 2 places behind the soldier and two places left/right of that position
        for threat in [(x - 1, y + dir), (x, y + dir), (x + 1, y + dir), (x - 1, y), (x + 1, y)]:
            if enemy.soldier_at(threat):
                for move in [(x - 2, y - 2 * dir), (x, y - 2 * dir), (x + 2, y - 2 * dir)]:
                    if not Move.out_of_bounds(move) and not player.soldier_at(move) and not enemy.soldier_at(move):
                        moves.append(Move(pos=move, retreat=True))
        
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
            if not Move.out_of_bounds(slide) and not enemy.soldier_at(slide) and not player.soldier_at(slide):
                moves.append(Move(pos=slide))
            
            # check if there is the free position in front available so the cannon can shoot
            if Move.out_of_bounds(free) or enemy.soldier_at(free) or player.soldier_at(free):
                continue

            # add possible shot positions
            no_hit = True
            for move in shots:
                if not Move.out_of_bounds(move) and no_hit:
                    # if the shoot will hit a town, then mark this as finishing move
                    if enemy.get_town_position() == move:
                        moves.append(Move(pos=move, finish_move=True, shoot=True))

                    # if the shoot does not hit an enemy or a town, then skip this move
                    no_hit = not enemy.soldier_at(move)
                    if no_hit:
                        continue
                    moves.append(Move(pos=move, kill_move=True, shoot=True))
        
        return moves

    def execute(self, player: Player, soldier: CannonSoldier, move: Move) -> None:
        """
        This method executes the move of a given soldier.
        """
        # get the opponent player
        enemy = self._p_dark if player == self._p_light else self._p_light

        # remove the enemy soldier if the move is a shoot
        if move.is_shoot():
            if enemy.soldier_at(move.get_pos()):
                enemy.remove_at(move.get_pos())
                print(f"{player.get_type()}: {soldier.get_pos()} -> {move.get_pos()} and hits an enemy!")

        # remove an enemy if this is a kill move
        elif move.is_kill_move():
            enemy.remove_at(move.get_pos())
            player.move_soldier(soldier, move)
            print(f"{player.get_type()}: {soldier.get_pos()} -> {move.get_pos()}, swordfight won!")
        
        # if the player won the game, then quit
        elif move.is_finish_move():
            self.end_game(player.get_type())
            print(f"{player.get_type()}: {soldier.get_pos()} -> {move.get_pos()}, climbed the town's walls!")
        
        # just move the soldier
        else:
            player.move_soldier(soldier, move)

            msg = "what a rough ground"
            if move.is_retreat_move():
                msg = "what a coward"
            
            if move.is_sliding_move():
                msg = "those cannons are heavy"

            print(f"{player.get_type()}: {soldier.get_pos()} -> {move.get_pos()}, {msg}.")

    def get_town_positions(self, turn: PlayerType) -> List[Move]:
        """
        This method gets all possible positions to place a town for the given player.
        """
        towns = []
        # get all possible positions for a town
        y = 9 if turn == PlayerType.LIGHT else 0
        for x in range(0, 10):
            towns.append(Move((x, y)))

        return towns

    def end_game(self, player_type: PlayerType):
        """
        This method should be called if the game ends. The given type 
        determines the winner.
        """
        self._on_finish_callback(player_type)

    def get_state(self) -> Dict:
        """
        This method summarizes the current game state.
        """
        state = {}

        state[PlayerType.LIGHT] = self._p_light.get_state()
        state[PlayerType.DARK] = self._p_dark.get_state()

        return state