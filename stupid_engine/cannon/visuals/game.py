from stupid_engine.backend.visuals.text import Text
from stupid_engine.cannon.entities.move import Move
from stupid_engine.cannon.theme import Theme
from stupid_engine.cannon.entities.player import Player, PlayerType
from stupid_engine.backend.visuals.movement import Movement
from stupid_engine.backend.visuals.sprite import Sprite
from stupid_engine.backend.game import Game
from typing import Dict, Tuple
import pygame as py


class Game(Game):

    SOLDIER_CLICKED = py.event.custom_type()
    MOVE_TO_CLICKED = py.event.custom_type()
    PLACE_TOWN = py.event.custom_type()

    # register events here :)
    EVENTS = [SOLDIER_CLICKED, MOVE_TO_CLICKED, PLACE_TOWN]

    def __init__(self, draw_size: Tuple[int, int] = (500, 500), border_size: Tuple[int, int] = (100, 100), theme: Theme = Theme.DEFAULT) -> None:
        # set up the theme, which handles the visuals
        self._theme = Theme(theme)

        # define all needed screen dimension including drawing area and border
        self._width, self._height = draw_size
        self._x_border, self._y_border = border_size
        self._window_size = (2 * self._x_border + self._width,
                             2 * self._y_border + self._height)

        super().__init__(self._window_size)
        self._frame_rate = 30

        # draw the game board using the theme
        self._board_state = None
        self._board = self._theme.get_board(self._screen, draw_size + border_size)

        self._sprites = dict()
        self._callbacks = dict()
        self._running = False

        self._header = Text("StupidEngine: Cannon", self._screen, draw_size, border_size, (0, 11))
        self._sprites["header"] = [self._header]
    
    def show_winner(self, player_type: PlayerType) -> None:
        print(f"Player '{player_type}' has won the game.")
        # print out the winner into the game's header
        self._header.set_text(f"Player {player_type} won the game")
    
    def on_click(self, event_type, sprite: Sprite) -> None:
        """
        This is a callback function which is executed, if a registered event run. The sprite 
        that was used in the event context is given.
        """
        if event_type not in self._callbacks.keys():
            return

        # check if event is part of registered events
        if event_type in Game.EVENTS:
            self._callbacks[event_type](sprite.get_position())

    def draw(self) -> None:
        super().draw()

        # draw the game board as background
        self._board.draw()

        # draw the current game state
        for name in ["soldiers", "moves", "towns", "header"]:
            if name in self._sprites.keys():
                for sprite in self._sprites[name]:
                    sprite.draw()
    
    def set_board_state(self, board_state: Dict, active_player: PlayerType) -> None:
        """
        This method sets the board initially and creates all basic sprites like soldiers.
        """
        self._board_state = board_state

        self._set_soldiers(active_player=active_player)
        self._set_moves()
        self._set_towns()

    def _set_soldiers(self, active_player: PlayerType):
        self._sprites["soldiers"] = []

        border = (self._x_border, self._y_border)
        board = (self._width, self._height)

        # for each position of each soldier, create the object and add
        # it to the sprites
        for player_type in [PlayerType.LIGHT, PlayerType.DARK]:
            soldiers, _ = self._board_state[player_type]
            for soldier in soldiers:
                # get and configure the themed figure
                figure = self._theme.get_soldier(player_type)
                s = figure(surface=self._screen, board_dim=board,
                        border_dim=border, pos=soldier.get_pos())

                s.active(active_player == player_type)
                s.callback(Game.SOLDIER_CLICKED, self.on_click)

                self._sprites["soldiers"].append(s)

    def _set_moves(self):
        self._sprites["moves"] = []
        border = (self._x_border, self._y_border)
        board = (self._width, self._height)

        if "moves" in self._board_state.keys():
            moves = self._board_state["moves"]
            for move in moves:
                s = Movement(self._screen, board, border, move.get_pos())
                s.callback(Game.MOVE_TO_CLICKED, self.on_click)
                self._sprites["moves"].append(s)
    
    def _set_towns(self):
        self._sprites["towns"] = []
        border = (self._x_border, self._y_border)
        board = (self._width, self._height)

        # possible places for a town
        if "towns" in self._board_state.keys():
            towns = self._board_state["towns"]
            for town in towns:
                s = Movement(self._screen, board, border, town.get_pos())
                s.callback(Game.PLACE_TOWN, self.on_click)
                self._sprites["towns"].append(s)
        
        # a town itself
        for player_type in [PlayerType.LIGHT, PlayerType.DARK]:
            soldiers, town = self._board_state[player_type]
            if town and town.get_pos():
                figure = self._theme.get_town(player_type)
                s = figure(surface=self._screen, board_dim=board,
                        border_dim=border, pos=town.get_pos())

                self._sprites["towns"].append(s)
