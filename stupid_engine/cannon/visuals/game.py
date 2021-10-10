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

    def __init__(self, window_size: Tuple[int, int], draw_area: Tuple[int, int] = (500, 500), theme: Theme = Theme.DEFAULT, flags: int = 0) -> None:
        super().__init__(window_size=window_size, draw_area=draw_area, frame_rate=30, flags=flags)

        # set up the theme, which handles the visuals
        self._theme = Theme(theme, window_size, draw_area, self._screen)
        self._scaling = self._theme.get_scaling()

        # draw the game board using the theme
        self._board_state = None
        self._board = self._theme.get_board()
        self._draw_area = self._board.get_draw_area()

        self._sprites = dict()
        self._callbacks = dict()
        self._running = False

        py.display.set_caption("StupidEngine: Cannon")
    
    def show_winner(self, player_type: PlayerType) -> None:
        """
        This method shows the winner on screen.
        """
        print(f"Player '{player_type}' has won the game.")
        py.display.set_caption("Player '{player_type}' has won the game")
    
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
        for name in ["towns", "soldiers", "moves"]:
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

        board = (self._width, self._height)

        # for each position of each soldier, create the object and add
        # it to the sprites
        for player_type in [PlayerType.LIGHT, PlayerType.DARK]:
            soldiers, _ = self._board_state[player_type]
            for pos in soldiers:
                # get and configure the themed figure
                figure = self._theme.get_soldier(player_type)
                s = figure(pos=pos)
                s.active(active_player == player_type)
                s.callback(Game.SOLDIER_CLICKED, self.on_click)

                self._sprites["soldiers"].append(s)

    def _set_moves(self):
        self._sprites["moves"] = []
        board = (self._width, self._height)

        if "moves" in self._board_state.keys():
            moves = self._board_state["moves"]
            for move in moves:
                s = Movement(self._screen, self._draw_area, move.get_pos(), self._scaling)
                s.callback(Game.MOVE_TO_CLICKED, self.on_click)
                self._sprites["moves"].append(s)
    
    def _set_towns(self):
        self._sprites["towns"] = []
        board = (self._width, self._height)

        # possible places for a town
        if "towns" in self._board_state.keys():
            towns = self._board_state["towns"]
            for town in towns:
                s = Movement(self._screen, self._draw_area, town.get_pos(), self._scaling)
                s.callback(Game.PLACE_TOWN, self.on_click)
                self._sprites["towns"].append(s)
        
        # a town itself
        for player_type in [PlayerType.LIGHT, PlayerType.DARK]:
            soldiers, town = self._board_state[player_type]
            if town and town.get_pos():
                figure = self._theme.get_town(player_type)
                s = figure(pos=town.get_pos())
                self._sprites["towns"].append(s)
