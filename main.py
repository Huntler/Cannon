from game import Game
from cannon.cannon import CannonGame

# Setup Model
cannon = CannonGame()

# Setup View
game = Game(draw_size=(300, 300))

# Update View
state = cannon.get_state()

#state[0][2] = (1, 5)
game.set_board_state(state)

# Run the game loop
game.game_loop()