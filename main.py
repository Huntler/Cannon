from stupid_engine.cannon.ai.alphabeta import AlphaBeta
from stupid_engine.cannon.ai.human import Human
from stupid_engine.cannon.ai.random import RandomAI
from stupid_engine.cannon.theme import Theme
from stupid_engine.cannon.entities.player import PlayerType
from stupid_engine.cannon.game_controller import Application


# create and start the Cannon game application
app = Application(window_size=(2560, 1600), theme=Theme.DEFAULT)

app.set_player(PlayerType.LIGHT, AlphaBeta)
app.set_player(PlayerType.DARK, AlphaBeta)

app.start_game()