from visuals.soldier import Soldier
from game import Game
from cannon.cannon import CannonGame

# Setup Model
cannon = CannonGame()

# Setup View
game = Game(draw_size=(300, 300))

# Update View
state = cannon.get_state()
game.set_board_state(state)

# - if the user clicked on a Soldier, then the possible moves are 
#   calculated and put into the state
# - all callback methods have to return the occured state
game.register_callback(Soldier.CLICKED, cannon.possible_moves)

# Run the game loop
game.game_loop()