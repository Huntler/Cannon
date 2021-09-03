# Setup Model
from stupid_engine.cannon.theme import Theme
from typing import Tuple
from stupid_engine.cannon.visuals.game import Game
from stupid_engine.cannon.entities.cannon import CannonGame
from stupid_engine.cannon.entities.player import Player, PlayerType


class Application:
    def __init__(self, window_size: Tuple[int, int] = (300, 300), theme: Theme = Theme.DEFAULT):
        """
        This application handles the cannon game backend and frontend. Here
        the events and callbacks are connected, so the user can interact with 
        the backend using the fronted GUI.
        """

        # create the players
        self._p_light = Player(PlayerType.LIGHT)
        self._p_dark = Player(PlayerType.DARK)
        self._boomer = None
        self._ai = None

        self._cannon = CannonGame(self._p_light, self._p_dark)

        # Setup View
        self._game = Game(draw_size=(300, 300), theme=theme)

        # - if the user clicked on a Soldier, then the possible moves are
        #   calculated and put into the state
        # - all callback methods have to return the occured state
        self._game.register_callback(
            Game.SOLDIER_CLICKED, self._possible_moves)
        self._game.register_callback(Game.MOVE_TO_CLICKED, self._make_move)

    def _possible_moves(self, position):
        # select the figure which should move / fire
        self._boomer.select_soldier(position)

        # get all possible moves of this figure owned by the current player
        state = self._cannon.possible_moves(self._boomer.get_type(), position)

        # set the gained state to the board to show possible moves
        self._game.set_board_state(
            board_state=state, active_player=self._boomer.get_type())

    def _make_move(self, position):
        # move the selected figure
        self._boomer.move_soldier(position)

        # update the GUI
        state = self._cannon.get_state()
        self._game.set_board_state(
            board_state=state, active_player=self._boomer.get_type())

        # let the AI play its turn
        self._ai.play_turn()
        state = self._cannon.get_state()
        self._game.set_board_state(
            board_state=state, active_player=self._boomer.get_type())

    def configure_ai(self, ai, player_type: PlayerType) -> None:
        player = self._p_light if player_type == PlayerType.LIGHT else self._p_dark
        self._ai = ai(self._cannon, player)

    def human_controls(self, player_type: PlayerType) -> None:
        """
        This sets the player controlled by a human
        """
        if self._ai and self._ai.get_player_type() == player_type:
            print("The AI and human should select different players.")
            quit()

        self._boomer = self._p_light if player_type == PlayerType.LIGHT else self._p_dark

    def start(self):
        """
        This method starts the application loop.
        """
        # Update View
        state = self._cannon.get_state()
        self._game.set_board_state(
            board_state=state, active_player=PlayerType.LIGHT)
        
        # if the ai is player light, then make the move
        if self._ai.get_player_type() == PlayerType.LIGHT:
            self._ai.play_turn()
            state = self._cannon.get_state()
            self._game.set_board_state(
                board_state=state, active_player=self._boomer.get_type())


        # Run the game loop
        self._game.game_loop()
