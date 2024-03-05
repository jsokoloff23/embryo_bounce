"""
This module contains the Border and Borders classes which are used in the
game the borders that the ball cannot pass through.
"""

from utils import constants


class Border(object):
    """
    border object used in game.

    x: int
        x position in pixels

    y: int
        y position in pixels

    height: int
        height in pixels

    width: int:
        width in pixels

    color: tuple[int, int, int]
        color of border
    """
    DEF_SHORT = 20
    def __init__(self, x: int, y: int, height: int, width: int, color: tuple[int, int, int]):
        self.x: int = x
        self.y: int = y
        self.height: int = height
        self.width: int = width
        self.color: tuple[int, int, int] = color


class Borders(object):
    """
    Class that contains all three borders used in game
    """
    def __init__(self):
        self.top = Border(x=0, 
                          y=0, 
                          height=Border.DEF_SHORT, 
                          width=constants.GAME_X_SIZE, 
                          color=constants.RED)
        self.back = Border(x=constants.GAME_X_SIZE-Border.DEF_SHORT, 
                           y=0, 
                           height=constants.GAME_Y_SIZE, 
                           width=Border.DEF_SHORT, 
                           color=constants.BLUE)
        self.bot = Border(x=0, 
                          y=constants.GAME_Y_SIZE-Border.DEF_SHORT, 
                          height=Border.DEF_SHORT, 
                          width=constants.GAME_X_SIZE, 
                          color=constants.GREEN)
        