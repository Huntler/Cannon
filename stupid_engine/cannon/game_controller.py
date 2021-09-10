import stupid_engine
from stupid_engine.backend.controller import GameController
from stupid_engine.cannon.theme import Theme
from typing import Tuple
from stupid_engine.cannon.visuals.game import Game
from stupid_engine.cannon.entities.cannon import CannonGame
from stupid_engine.cannon.entities.player import Player, PlayerType


class Application(GameController):
    def __init__(self, window_size: Tuple[int, int] = (300, 300), theme: Theme = Theme.DEFAULT) -> None:
        """
        This application handles the cannon game backend and frontend. Here
        the events and callbacks are connected, so the user can interact with 
        the backend using the fronted GUI.
        """
        # create the players and the CannonGame that handles rules and logic
        # the first player is always 'light'
        self._p_light = Player(PlayerType.LIGHT)
        self._p_dark = Player(PlayerType.DARK)
        self._cannon = CannonGame(self._p_light, self._p_dark)
        self._active = self._p_light

        # set the visual settings
        self._window_size = window_size
        self._theme = theme

        super().__init__()

    def set_player(self, type: PlayerType, ai) -> None:
        """
        This method maps the given ai to the specified player.
        """
        if type == PlayerType.LIGHT:
            self._p_light.set_controller(ai(self._p_light, self._cannon))

        else:
            self._p_dark.set_controller(ai(self._p_dark, self._cannon))

    def _init_game_visuals(self) -> None:
        """
        This method is called right after the initialization and should configure 
        the game visuals object.
        """
        self._game = Game(draw_size=self._window_size, theme=self._theme)
        self._game.set_board_state(
            self._cannon.get_state(), self._active.get_type())
        self._game.on_callback(Game.QUIT, self.stop)

        self._game.on_callback(Game.PLACE_TOWN, self._on_town_place)
        self._game.on_callback(Game.SOLDIER_CLICKED, self._on_soldier_clicked)
        self._game.on_callback(Game.MOVE_TO_CLICKED, self._on_move_clicked)

    def _switch_player(self) -> None:
        """
        This method switches the active player.
        """
        self._active = self._p_dark if self._active == self._p_light else self._p_light

    def _on_soldier_clicked(self, pos: Tuple[int, int]) -> None:
        """
        This method is called if a soldier was clicked and handles the needed 
        actions in this case.
        """
        # get all possible moves available and put those hints into the state
        soldier = self._active.soldier_at(pos)
        self._active.select_soldier(soldier)
        moves = self._cannon.moves(self._active, soldier)

        state = self._cannon.get_state()
        state["moves"] = moves

        # set the gained state to the board to show possible moves
        self._game.set_board_state(
            board_state=state, active_player=self._active.get_type())

    def _on_move_clicked(self, pos: Tuple[int, int]) -> None:
        """
        This method is called if a position for movement was clicked. Then a
        previous selected soldier is moved to the provided position.
        """
        soldier = self._active.get_selected_soldier()
        moves = self._cannon.moves(self._active, soldier)

        for move in moves:
            if move.get_pos() == pos:
                self._cannon.execute(self._active, soldier, move)
                self._game.set_board_state(
                    board_state=self._cannon.get_state(), active_player=self._active.get_type())
                self._switch_player()
                return

    def _on_town_place(self, pos: Tuple[int, int]) -> None:
        """
        This method is called if a town gets placed.
        """
        # place the town to the given position
        self._active.place_town(pos)

    def loop(self) -> None:
        """
        This is executed in a while this thread is alive loop. Here the logic of the game 
        can be handled.
        """
        state_changed = False
        # check if a town has to be placed
        if not self._active.is_town_placed():
            # get possible town locations
            positions = self._cannon.get_town_positions(self._active.get_type())
            # update the state by extending it using the town positions
            state = self._cannon.get_state()
            state["towns"] = positions
            self._game.set_board_state(board_state=state, active_player=self._active.get_type())
            # let the user / ai choose a town location
            while not self._active.is_town_placed():
                self._active.place_town(positions)

            state_changed = True

        # let the player or ai play a turn, if there was a change made, then return true
        else:
            state = self._cannon.get_state()
            state_changed = self._active.play_turn(state)

        # if the state has changed, then a move was made and the board has to be updated
        if state_changed:
            self._switch_player()
            self._game.set_board_state(
                self._cannon.get_state(), self._active.get_type())
