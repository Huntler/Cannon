from threading import Thread
import time
from typing import Tuple
import pygame as py


class Game:

    QUIT = py.QUIT

    def __init__(self, window_size: Tuple[int, int]) -> None:
        """
        This class structurizes a game and the corresponding GUI for 
        it. The main loop will block the main thread, so be sure to 
        specify all callbacks before.
        """
        py.init()
        self._running = False
        self._screen = py.display.set_mode((window_size))

        self._callbacks = dict()
        self._clock = py.time.Clock()
        self._frame_rate = 30
    
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
        
        self._clock.tick(self._frame_rate)
    
    def draw(self) -> None:
        """
        This method can be used to draw elements on the GUI.
        """
        pass
