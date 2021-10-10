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

windowed_size = (700, 700)
windowed_flags = py.SCALED

if FULLSCREEN:
    app = Application(window_size=fullscreen_size, theme=Theme.DEFAULT, flags=fullscreen_flags)
else:
    app = Application(window_size=windowed_size, theme=Theme.DEFAULT, flags=windowed_flags)

# weights are defined by the following features
# finish, soldiders defending town, shoot, kill, retreat, army size difference
light = lambda p, c: AlphaBeta(
    player=p, 
    cannon=c, 
    alpha=-math.inf, 
    beta=math.inf, 
    depth=2, 
    time_limit=15, 
    weights=[100, 5, 2, 1, 2, 1], 
    refresh_tt=True)
dark = lambda p, c: AlphaBeta(
    player=p, 
    cannon=c, 
    alpha=-math.inf, 
    beta=math.inf, 
    depth=2, 
    time_limit=15, 
    weights=[100, 5, 2, 1, 2, 1], 
    refresh_tt=True)

app.set_player(PlayerType.LIGHT, light) # plys: 8.22 # winner
app.set_player(PlayerType.DARK, Human) # plys: 7.98

# without search window: 6.1-6.2 plys. 9 plys in the end.

app.start_game()