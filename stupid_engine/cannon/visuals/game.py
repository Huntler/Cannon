from stupid_engine.cannon.theme import Theme
from stupid_engine.cannon.entities.player import PlayerType
from stupid_engine.backend.visuals.font import Font
from stupid_engine.cannon.visuals.game_board import Board
from stupid_engine.cannon.entities.cannon import CannonGame
from stupid_engine.backend.visuals.figure import Figure
from stupid_engine.backend.visuals.movement import Movement
from stupid_engine.backend.visuals.sprite import Sprite
from typing import Dict, List, Tuple
import pygame as py


class Game:

    SOLDIER_CLICKED = Sprite.CLICKED
    MOVE_TO_CLICKED = Movement.CLICKED

    EVENTS = [SOLDIER_CLICKED, MOVE_TO_CLICKED]

    def __init__(self, draw_size: Tuple[int, int] = (500, 500), border_size: Tuple[int, int] = (100, 100), theme: Theme = Theme.DEFAULT) -> None:
        """
        This class represents the game GUI and handles the user events.
        """
        py.init()

        self._theme = Theme(theme)

        self._width, self._height = draw_size
        self._x_border, self._y_border = border_size
        self._window_size = (2 * self._x_border + self._width,
                             2 * self._y_border + self._height)

        self._screen = py.display.set_mode(self._window_size)

        self._board_state = None
        self._board = Board(self._screen, draw_size + border_size, Font.ARIAL)

        self._sprites = dict()
        self._callbacks = dict()

        self._running = False

    def game_loop(self):
        """
        This method contains the GUI loop. Here the events will be checked 
        and screen elements drawn.
        """
        self._running = True
        while self._running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    self._running = False
                    quit()

            # draw the board
            self._board.draw()

            # draw the current game state
            for name in ["soldiers", "moves"]:
                if name in self._sprites.keys():
                    for sprite in self._sprites[name]:
                        sprite.draw()

            # print the screens background and update
            py.display.flip()

    def set_board_state(self, board_state: Dict, active_player: PlayerType) -> None:
        """
        This method sets the board initially and creates all basic sprites like soldiers.
        """
        self._board_state = board_state

        self._set_soldiers(active_player=active_player)
        self._set_moves()

    def _set_soldiers(self, active_player: PlayerType):
        self._sprites["soldiers"] = []

        # get the initial positions
        light = self._board_state["light"]
        dark = self._board_state["dark"]

        border = (self._x_border, self._y_border)
        board = (self._width, self._height)

        # for each position of each soldier, create the object and add
        # it to the sprites
        for pos in light:
            # get and configure the themed figure
            figure = self._theme.get_soldier(PlayerType.LIGHT)
            s = figure(surface=self._screen, board_dim=board,
                       border_dim=border, pos=pos)

            s.active(active_player == PlayerType.LIGHT)
            s.callback(Game.SOLDIER_CLICKED, self._sprite_clicked)

            self._sprites["soldiers"].append(s)

        for pos in dark:
            figure = self._theme.get_soldier(PlayerType.DARK)
            s = figure(surface=self._screen, board_dim=board,
                       border_dim=border, pos=pos)

            s.active(active_player == PlayerType.DARK)
            s.callback(Game.SOLDIER_CLICKED, self._sprite_clicked)

            self._sprites["soldiers"].append(s)

    def _set_moves(self):
        self._sprites["moves"] = []
        border = (self._x_border, self._y_border)
        board = (self._width, self._height)

        if "moves" in self._board_state.keys():
            moves = self._board_state["moves"]
            for move in moves:
                s = Movement(self._screen, board, border, move)
                s.callback(Game.MOVE_TO_CLICKED, self._sprite_clicked)
                self._sprites["moves"].append(s)

    def _sprite_clicked(self, event_type, sprite: Sprite) -> None:
        """
        This is a callback function which is executed, if a registered event run. The sprite 
        that was used in the event context is given.
        """
        if event_type not in self._callbacks.keys():
            return

        if event_type in Game.EVENTS:
            for func in self._callbacks[event_type]:
                func(sprite.get_position())

    def register_callback(self, event_type, func) -> None:
        """
        This method registers a callback outside the GUI which is executed if the 
        given event occurs.
        """
        if event_type not in self._callbacks.keys():
            self._callbacks[event_type] = []

        self._callbacks[event_type].append(func)
