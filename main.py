from stupid_engine.cannon.ai.alphabeta import AlphaBeta
from stupid_engine.cannon.ai.human import Human
from stupid_engine.cannon.ai.random import RandomAI
from stupid_engine.cannon.theme import Theme
from stupid_engine.cannon.entities.player import PlayerType
from stupid_engine.cannon.game_controller import Application
import pygame as py
import math

FULLSCREEN = False


# create and start the Cannon game application
fullscreen_size = (2560, 1600)
fullscreen_flags = py.FULLSCREEN | py.HWSURFACE | py.DOUBLEBUF

windowed_size = (500, 500)
windowed_flags = 0

if FULLSCREEN:
    app = Application(window_size=fullscreen_size, theme=Theme.DEFAULT, flags=fullscreen_flags)
else:
    app = Application(window_size=windowed_size, theme=Theme.DEFAULT, flags=windowed_flags)


# finish, shoot, kill, retreat, army size (per soldier diff) e.g.: [10, 5, 1, 2, 1]
ab1 = lambda p, c: AlphaBeta(p, c, -math.inf, math.inf, 10, 15, [5, 2, 3, 2, 1], True)
ab2 = lambda p, c: AlphaBeta(p, c, -math.inf, math.inf, 4, None, [5, 2, 3, 2, 1], True)

app.set_player(PlayerType.LIGHT, ab1)
app.set_player(PlayerType.DARK, ab2)

app.start_game()