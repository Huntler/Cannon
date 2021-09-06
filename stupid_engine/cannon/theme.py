from stupid_engine.cannon.visuals.game_board import Board
from stupid_engine.backend.visuals.font import Font
from stupid_engine.cannon.entities.player import Player, PlayerType
from stupid_engine.backend.visuals.image import Image
from stupid_engine.backend.visuals.sprite import Sprite
from stupid_engine.backend.visuals.figure import Figure


class Theme:
    DEFAULT = 0
    STAR_WARS = 1

    def __init__(self, theme) -> None:
        """
        This class is used to load a specific theme. The GUI elements are 
        defined in here and can be used by the game.
        """
        self._theme = theme

        if theme == Theme.DEFAULT:
            self.font = Font.ARIAL
            self.font_size = 12

        if theme == Theme.STAR_WARS:
            self.font = Font.STAR_WARS
            self.font_size = 24

    def get_board(self, screen, size) -> Board:
        board = Board(screen, size, 10, self.font, self.font_size)

        if self._theme == Theme.STAR_WARS:
            bc = (30, 22, 79)
            fc = (173, 193, 194)
            lc = (30, 22, 79)
            tc = (173, 193, 194)
            board.set_color(bc, fc, lc, tc)

        return board

    def get_soldier(self, type: PlayerType) -> Sprite:
        """
        This method loads the visual of a soldier and returns the prepared sprite 
        object. Care, this object is not initialized yet.

        The parameters: [surface, board_dim, border_dim, pos] are not set.
        """
        # load the default theme
        if self._theme == Theme.DEFAULT:
            color = None
            if type == PlayerType.LIGHT:
                color = (240, 50, 0)
            else:
                color = (100, 150, 0)

            figure = lambda **kwargs: Figure(**kwargs, color=color)
            return figure

        # load the star wars theme
        if self._theme == Theme.STAR_WARS:
            soldier_path = None
            if type == PlayerType.LIGHT:
                soldier_path = "stupid_engine/resources/star_wars/clone_75x75_01.png"
            else:
                soldier_path = "stupid_engine/resources/star_wars/droid_75x75_01.png"

            figure = lambda **kwargs: Image(**kwargs,
                                            img_path=soldier_path, size=(30, 30))
            return figure

    def get_town(self) -> None:
        pass

    def get_move_point(self) -> None:
        pass

    def get_hit_mark(self) -> None:
        pass
