from stupid_engine.cannon.ai import human
from stupid_engine.cannon.ai.alphabeta import AlphaBeta
from stupid_engine.cannon.ai.human import Human
from stupid_engine.cannon.ai.random import RandomAI
from stupid_engine.cannon.theme import Theme
from stupid_engine.cannon.entities.player import PlayerType
from stupid_engine.cannon.game_controller import Application
import pygame as py
import math
import sys


FULLSCREEN = "-f" in sys.argv
LOAD_SAVED = "-l" in sys.argv
TIME_LIMIT = 5


# create and start the Cannon game application
fullscreen_size = (2560, 1600)
fullscreen_flags = py.FULLSCREEN | py.HWSURFACE | py.DOUBLEBUF

windowed_size = (700, 700)
windowed_flags = py.SCALED

if FULLSCREEN:
    app = Application(window_size=fullscreen_size, theme=Theme.DEFAULT, flags=fullscreen_flags)
else:
    app = Application(window_size=windowed_size, theme=Theme.DEFAULT, flags=windowed_flags)

if not LOAD_SAVED:
    # weights are defined by the following features
    # 0 distance of soldier to enemy town
    # 1 delta distance of soldier to enemy town
    # 2 captur enemy town
    # 3 defense wall infront of own town
    # 4 retreat if threatened
    # 5 shoot at something
    # 6 difference in army size
    # 7 kill a soldier

    light = lambda p, c: AlphaBeta(
        player=p, 
        cannon=c, 
        alpha=-math.inf, 
        beta=math.inf, 
        depth=4, 
        time_limit=TIME_LIMIT, 
        weights=[0, 1, 5, 3, 2, 3, 2, 0],
        refresh_tt=True,
        always_sort=True)

    dark = lambda p, c: AlphaBeta(
        player=p, 
        cannon=c, 
        alpha=-math.inf, 
        beta=math.inf, 
        depth=4, 
        time_limit=TIME_LIMIT, 
        weights=[0, 1, 5, 3, 2, 3, 2, 0], 
        refresh_tt=True,
        always_sort=True)

    app.set_player(PlayerType.LIGHT, light)
    app.set_player(PlayerType.DARK, Human)

else:
    app.load_game()

app.start_game()