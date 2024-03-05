import numpy as np
import pygame
from utils import constants

class Ball(object):
    """
    ball object used in game.

    instance attributes:

    self.x: int
        x position in pixels

    self.y: int
        y position in pixels

    self.speed: int
        ball speed, in pixels/frame

    self.x_vel: int
        x velocity, in pixels/frame

    self.y_vel: int = 0
        y velocity, in pixels/frame

    self.radius: int = 20
        radius of ball in pixels

    self.area_density: int
        area density of ball

    self.image_path: str
        path of image to be used as ball texture

    self.image: pygame.Surface
        image to be used as ball texture
    """
    _MIN_SPEED = 1
    def __init__(self):
        self.x: int = 400
        self.y: int = 300
        self._speed: int = 5
        self.x_vel: int = -self.speed
        self.y_vel: int = 0
        self.radius: int = 20
        self.area_density = 1
        self.image = pygame.image.load(constants.EMBRYO_IMAGE_PATH)
    
    @property
    def mass(self):
        return np.pi*self.radius**2*self.area_density

    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        x_fact = self.x_vel/self.speed
        y_fact = self.y_vel/self.speed
        self.x_vel = int(x_fact*value)
        self.y_vel = int(y_fact*value)
        self._speed = value

    @property
    def image_path(self):
        return self._image_path
    
    #so that image is updated to match path
    @image_path.setter
    def image_path(self, value):
        self.image = pygame.image.load(value)
        self._image_path = value
    
    def get_coords(self):
        return (self.x, self.y)

    def set_pos_from_coords(self, coords: tuple[float, float]):
        """
        arguments:

        coords: tuple[float, float]
            normalized coords (x,y)
        """
        if coords:
            self.x , self.y = coords
