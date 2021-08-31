from visuals.board import Board
from visuals.soldier import Soldier
from cannon.cannon import CannonGame
from typing import Dict, List, Tuple
import pygame as py


class Game:
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

        self._scaling = self._width / Soldier.SIZE
        self._board_state = None

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

                # TODO: give clicked index pair
                if event.type in self._callbacks.keys():
                    for func in self._callbacks[event.type]:
                        func((0, 0))

            # draw the board
            Board.draw(self._screen, self._width, self._height, self._x_border, self._y_border, self._scaling)

            # draw the current game state
            if self._board_state:
                self._draw_board()

            # print the screens background and update
            py.display.flip()

    def set_board_state(self, board_state: Dict) -> None:
        self._board_state = board_state

    def _draw_board(self):
        light = self._board_state["light"]
        dark = self._board_state["dark"]

        for pos in light:
            # draw a light soldier
            p_x, p_y = self._to_pixel(pos)
            active = CannonGame.LIGHT == self._board_state["active"]
            Soldier.draw(self._screen, p_x, p_y, Soldier.LIGHT, active)

        for pos in dark:
            # draw a dark soldier
            p_x, p_y = self._to_pixel(pos)
            active = CannonGame.DARK == self._board_state["active"]
            Soldier.draw(self._screen, p_x, p_y, Soldier.DARK, active)

    def _to_pixel(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = pos
        return x * self._scaling + self._x_border + self._scaling / 2, self._height - y * self._scaling + self._y_border - self._scaling / 2
    
    def register_callback(self, event_type, func) -> None:
        if event_type not in self._callbacks.keys():
            self._callbacks[event_type] = []

        self._callbacks[event_type].append(func)
