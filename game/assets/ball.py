import pygame

class Ball(object):
    """
    ball object used in game.

    instance attributes:

    self.x: int
        x in pixels

    self.y: int
        y in pixels

    self.speed: int
        speed in pixels

    self.x_vel: int
        x velocity in pixels per frame

    self.y_vel: int = 0
        y velocity in pixels per frame

    self.radius: int = 0.02
        radius in pixels
    """
    _MIN_SPEED = 1
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self._speed: int = 5
        self.x_vel: int = -self.speed
        self.y_vel: int = 0
        self.radius: int = 10
        self.image = pygame.image.load("game/assets/images/embryo.py")

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

    
    def get_coords(self):
        return (self.x, self.y)
