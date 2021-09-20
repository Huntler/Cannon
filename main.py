from stupid_engine.cannon.ai.alphabeta import AlphaBeta
from stupid_engine.cannon.ai.human import Human
from stupid_engine.cannon.ai.random import RandomAI
from stupid_engine.cannon.theme import Theme
from stupid_engine.cannon.entities.player import PlayerType
from stupid_engine.cannon.game_controller import Application
import pygame as py


# create and start the Cannon game application
flags = py.FULLSCREEN, py.HWSURFACE, py.DOUBLEBUF
app = Application(window_size=(400, 400), theme=Theme.DEFAULT, flags=0)

# finish, shoot, kill, retreat, army size
ab1 = lambda p, c: AlphaBeta(p, c, -50, 50, 4, [5, 3, 1, 2, 1])

app.set_player(PlayerType.LIGHT, ab1)
app.set_player(PlayerType.DARK, RandomAI)

app.start_game()