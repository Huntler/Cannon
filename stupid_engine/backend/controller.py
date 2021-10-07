from multiprocessing.spawn import freeze_support
from stupid_engine.cannon.entities.player import PlayerType
from threading import Thread
from stupid_engine.backend.game import Game


class GameController(Thread):
    def __init__(self) -> None:
        """
        This class represents a controller that connects the game logic to the GUI object.
        This runs in a separate thread so it is next to the GUI one.
        """
        super(GameController, self).__init__(group=None, target=None, name="ControllerThread")
        
        self._running = False
        self._game = None
        self._init_game_visuals()
    
    def _init_game_visuals(self) -> None:
        """
        This method defines the game in this controller and sets the pygame quit event. 
        """
        raise NotImplemented
    
    def set_player(self, type: PlayerType, player) -> None:
        """
        This method defines the player which have to be organized by this controller.
        """
        raise NotImplemented
    
    def start_game(self) -> None:
        """
        This method is important, because with this, the controller and GUI will be started.
        """
        self.start()
        self._game.start()
    
    def is_alive(self) -> bool:
        """
        This method checks if the controller thread is still alive.
        """
        return self._running

    def run(self) -> None:
        """
        This is the main loop which is started by the thread parent class.
        """
        self._running = True
        while self._running:
            self.loop()
        
        self._running = False
        print("Controller has stopped.")
    
    def loop(self) -> None:
        """
        In here the logic can be implemented. This will be executed in a while 
        thread alive loop.
        """
        pass
    
    def stop(self) -> None:
        """
        This method gently stops the thread be ending its loop.
        """
        self._running = False


if __name__ == '__main__':
    freeze_support()