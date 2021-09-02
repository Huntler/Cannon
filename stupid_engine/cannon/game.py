from stupid_engine.cannon.entities.cannon import CannonGame
from stupid_engine.backend.visuals.soldier import Soldier
from stupid_engine.backend.visuals.movement import Movement
from stupid_engine.backend.visuals.sprite import Sprite
from stupid_engine.backend.visuals.board import Board
from typing import Dict, List, Tuple
import pygame as py


class Game:

    SOLDIER_CLICKED = Soldier.CLICKED
    MOVE_TO_CLICKED = Movement.CLICKED

    EVENTS = [SOLDIER_CLICKED, MOVE_TO_CLICKED]

    def __init__(self, draw_size: Tuple[int, int] = (500, 500), border_size: Tuple[int, int] = (100, 100)) -> None:
        """
        This class represents the game GUI and handles the user events.
        """
        py.init()
        Board.init_font()

        self._width, self._height = draw_size
        self._x_border, self._y_border = border_size
        self._window_size = (2 * self._x_border + self._width,
                             2 * self._y_border + self._height)

        self._screen = py.display.set_mode(self._window_size)
        self._board_state = None
        self._sprites = dict()

        self._callbacks = dict()

        self._running = True

    def game_loop(self):
        """
        This method contains the GUI loop. Here the events will be checked 
        and screen elements drawn.
        """
        while self._running:
            for event in py.event.get():
                if event.type == py.QUIT:
                    self._running = False
                    quit()

            # draw the board
            Board.draw(self._screen, self._width, self._height,
                       self._x_border, self._y_border)

            # draw the current game state
            for name in ["soldiers", "moves"]:
                if name in self._sprites.keys():
                    for sprite in self._sprites[name]:
                        sprite.draw()

            # print the screens background and update
            py.display.flip()

    def set_board_state(self, board_state: Dict) -> None:
        """
        This method sets the board initially and creates all basic sprites like soldiers.
        """
        self._board_state = board_state

        self._set_soldiers()
        self._set_moves()        

    def _set_soldiers(self):
        self._sprites["soldiers"] = []

        # get the initial positions
        light = self._board_state["light"]
        dark = self._board_state["dark"]

        border = (self._x_border, self._y_border)
        board = (self._width, self._height)

        # for each position of each soldier, create the object and add
        # it to the sprites
        for pos in light:
            s = Soldier(self._screen, board, border, pos, Soldier.LIGHT)
            s.active(CannonGame.LIGHT == self._board_state["active"])
            s.callback(Game.SOLDIER_CLICKED, self._sprite_clicked)
            self._sprites["soldiers"].append(s)

        for pos in dark:
            s = Soldier(self._screen, board, border, pos, Soldier.DARK)
            s.active(CannonGame.DARK == self._board_state["active"])
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
        if  event_type not in self._callbacks.keys():
            return

        if event_type in Game.EVENTS:
            for func in self._callbacks[event_type]:
                state = func(sprite.get_position())
                self.set_board_state(state)

    def register_callback(self, event_type, func) -> None:
        """
        This method registers a callback outside the GUI which is executed if the 
        given event occurs.
        """
        if event_type not in self._callbacks.keys():
            self._callbacks[event_type] = []

        self._callbacks[event_type].append(func)
