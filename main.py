from stupid_engine.cannon.theme import Theme
from stupid_engine.cannon.ai.random import RandomAI
from stupid_engine.cannon.entities.player import PlayerType
from stupid_engine.cannon.game_controller import Application


# create and start the Cannon game application
app = Application(window_size=(400, 400), theme=Theme.DEFAULT)

app.configure_ai(RandomAI, PlayerType.LIGHT)
app.human_controls(PlayerType.DARK)

app.start()