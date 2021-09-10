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
        for move in [(x - 1, y), (x + 1, dir)]:
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
        cannon_cases = [
            # orthogonal row, given soldier front
            [[(x, y - dir), (x, y - 2 * dir)], [(x, y + 2 * dir), (x, y + 3 * dir)]],
            # 3 in a orthogonal row, given soldier back
            [[(x, y + dir), (x, y + 2 * dir)], [(x, y - 2 * dir), (x, y - 3 * dir)]],
            # 3 in a diagonal row, given soldier front (right)
            [[(x - 1, y - dir), (x - 2, y - 2 * dir)], [(x + 2, y + 2 * dir), (x + 3, y + 3 * dir)]],
            # 3 in a diagonal row, given soldier back (right)
            [[(x + 1, y + dir), (x + 2, y + 2 * dir)], [(x - 2, y - 2 * dir), (x - 3, y - 3 * dir)]],
            # 3 in a diagonal row, given soldier front (left)
            [[(x + 1, y - dir), (x + 2, y - 2 * dir)], [(x - 2, y + 2 * dir), (x - 3, y + 3 * dir)]],
            # 3 in a diagonal row, given soldier back (left)
            [[(x - 1, y + dir), (x - 2, y + 2 * dir)], [(x + 2, y - 2 * dir), (x + 3, y - 3 * dir)]]
        ]

        # FIXME: Debug this
        for structure, shots in cannon_cases:
            # check if there is a cannon structure
            structure_exists = True
            for pos in structure:
                if Move.out_of_bounds(pos) or not player.soldier_at(pos):
                    structure_exists = False
            
            if not structure_exists:
                continue
        
            # add possible shot positions
            no_hit = True
            for move in shots:
                if not Move.out_of_bounds(move) and no_hit:
                    no_hit = not enemy.soldier_at(move)
                    kill_move = not no_hit
                    moves.append(Move(pos=move, kill_move=kill_move, shoot=True))
        
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

        # remove an enemy if this is a kill move
        elif move.is_kill_move():
            enemy.remove_at(move.get_pos())
            player.move_soldier(soldier, move)
        
        # if the player won the game, then quit
        elif move.is_finish_move():
            self.end_game(player.get_type())
        
        # just move the soldier
        else:
            player.move_soldier(soldier, move)

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