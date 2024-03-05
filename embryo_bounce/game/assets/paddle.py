"""
This module contains the Paddle class which is the paddle object used in
the game.
"""

import pygame

from utils import constants


class Paddle(object):
    """
    paddle object used in game.

    x: int
        x position in pixels

    y: int
        y position in pixels

    height: int
        height in pixels

    width: int:
        width in pixels

    self.image_path: str
        path of image to be used as paddle texture

    self.image: pygame.Surface
        image to be used as paddle texture
    """
    def __init__(self):
        self.x: int = 0
        self._y: int = constants.GAME_Y_SIZE/2
        self.height = 80
        self.width = 20
        self.image = pygame.image.load(constants.FISH_IMAGE_PATH)


    @property
    def y(self):
        return self._y
    
    #so that paddle position can't be outside of game boundary
    @y.setter
    def y(self, value):
        if value <= self.min_y:
            self._y = self.min_y
        elif self.max_y <= value:
            self._y = self.max_y
        else:
            self._y = value
            
    @property
    def max_y(self):
        return constants.GAME_Y_SIZE - self.height
    
    @property
    def min_y(self):
        return 0
    
    #coords of top right corner
    @property
    def top_coords(self):
        return (self.width+self.x, self.y)
    
    #coords of center right
    @property
    def cent_coords(self):
        return (self.width+self.x, self.height/2+self.y)
    
    #coords of bottom right corner
    @property
    def bot_coords(self):
        return (self.width+self.x, self.height+self.y)
    
    @property
    def image_path(self):
        return self._image_path
    
    #so that image is updated to match path
    @image_path.setter
    def image_path(self, value):
        self.image = pygame.image.load(value)
        self._image_path = value

    def set_pos_from_norm_coords(self, coords: tuple[float, float]):
        """
        arguments:

        coords: tuple[float, float]
            normalized coords (x,y)
        """
        if coords:
            x = int(constants.GAME_X_SIZE*coords[0])
            y = int(constants.GAME_Y_SIZE*coords[1])
            self.x = x
            self.y = y

    def set_pos_from_coords(self, coords: tuple[float, float]):
        """
        arguments:

        coords: tuple[float, float]
            normalized coords (x,y)
        """
        if coords:
            self.x, self.y = coords

    def get_coords(self):
        return (self.x, self.y)
