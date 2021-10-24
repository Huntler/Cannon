from typing import Tuple
import pygame as py


class Game:

    QUIT = py.QUIT

    def __init__(self, window_size: Tuple[int, int], draw_area: Tuple[int, int] = None, frame_rate: int = 60, flags: int = 0) -> None:
        """
        This class structurizes a game and the corresponding GUI for 
        it. The main loop will block the main thread, so be sure to 
        specify all callbacks before.
        """
        py.init()

        # set the screen size and draw area
        self._width, self._height = self._window_size = window_size
        self._draw_area = draw_area
        if not self._draw_area:
            self._draw_area = self._window_size

        # define the screen on which all sprites are rendered
        self._flags = flags#py.FULLSCREEN | py.HWSURFACE | py.DOUBLEBUF# | py.SCALED 
        self._screen = py.display.set_mode(self._window_size, self._flags)

        # define a clock to limit the frames per second
        self._clock = py.time.Clock()
        self._frame_rate = frame_rate

        # set up everything else
        self._running = False
        self._callbacks = dict()
    
    def get_window_size(self) -> Tuple[int, int]:
        return self._window_size
  
    def get_flags(self):
        return self._flags

    @property
    def frame_rate(self) -> int:
        return self._frame_rate
    
    @frame_rate.setter
    def frame_rate(self, frame_rate) -> None:
        if frame_rate < 1 or frame_rate > 60:
            raise ValueError("The frame rate has to be between 1 and 60.")
        self._frame_rate = frame_rate
    
    def on_callback(self, type, func) -> None:
        """
        Using this method, callbacks can be registered. If the 
        defined event occurs, then the given function is executed.
        """
        self._callbacks[type] = func

    def start(self) -> None:
        """
        This method holds the main loop that updates the GUI. Be 
        aware that this blocks the main thread.
        """
        self._running = True
        while self._running:
            for event in py.event.get():
                self.event(event)
            
            self.draw()
        
            # cap at the given frame rate
            self._clock.tick(self._frame_rate)
            py.display.flip()

        print("Graphics has stopped.")
    
    def event(self, event) -> None:
        """
        This method is used to handle GUI events.
        """
        if event.type == py.QUIT:
            self._running = False
            if Game.QUIT in self._callbacks.keys():
                self._callbacks[Game.QUIT]()
    
    def draw(self) -> None:
        """
        This method can be used to draw elements on the GUI.
        """
        pass
