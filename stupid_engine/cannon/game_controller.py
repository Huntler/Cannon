# Setup Model
from typing import Tuple
from stupid_engine.cannon.visuals.game import Game
from stupid_engine.cannon.entities.cannon import CannonGame


class Application:
    def __init__(self, window_size: Tuple[int, int] = (300, 300)):
        """
        This application handles the cannon game backend and frontend. Here
        the events and callbacks are connected, so the user can interact with 
        the backend using the fronted GUI.
        """
        self._cannon = CannonGame()

        # Setup View
        self._game = Game(draw_size=(300, 300))

        # Update View
        state = self._cannon.get_state()
        self._game.set_board_state(state)

        # - if the user clicked on a Soldier, then the possible moves are 
        #   calculated and put into the state
        # - all callback methods have to return the occured state
        self._game.register_callback(Game.SOLDIER_CLICKED, self._cannon.possible_moves)
        self._game.register_callback(Game.MOVE_TO_CLICKED, self._cannon.make_move)

    def start(self):
        """
        This method starts the application loop.
        """
        # Run the game loop
        self._game.game_loop()