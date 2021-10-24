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

THEME = Theme.APPLE
FULLSCREEN = "-f" in sys.argv
LOAD_SAVED = "-l" in sys.argv
TIME_LIMIT = 5
TT = True
DEPTH = 2
QUIESENCE = True
SOFT_BOUNDS = True


# create and start the Cannon game application
fullscreen_size = (1920, 1080)
fullscreen_flags = py.FULLSCREEN | py.HWSURFACE | py.DOUBLEBUF

windowed_size = (700, 700)
windowed_flags = py.SCALED

if FULLSCREEN:
    app = Application(window_size=fullscreen_size, theme=THEME, flags=fullscreen_flags)
else:
    app = Application(window_size=windowed_size, theme=THEME, flags=windowed_flags)

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
        depth=DEPTH, 
        time_limit=TIME_LIMIT, 
        weights=[1, 1, 5, 3, 2, 3, 2, 0],
        use_tt=TT,
        always_sort=True,
        quiesence=QUIESENCE,
        soft_bounds=SOFT_BOUNDS)

    dark = lambda p, c: AlphaBeta(
        player=p, 
        cannon=c, 
        alpha=-math.inf, 
        beta=math.inf, 
        depth=DEPTH, 
        time_limit=TIME_LIMIT, 
        weights=[1, 1, 5, 3, 2, 1, 1, 0], 
        use_tt=True,
        always_sort=True,
        quiesence=True,
        soft_bounds=True)

    app.set_player(PlayerType.LIGHT, light)
    app.set_player(PlayerType.DARK, dark)

else:
    app.load_game()

app.start_game()

print("Program exit.")