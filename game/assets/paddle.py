import pygame

class Paddle(object):
    """
    paddle object used in game.

    x: int
        x in pixels

    y: int
        y in pixels

    height: int
        height in pixels

    width: int:
        width in pixels
    """
    def __init__(self):
        self.x: int = 0
        self._y: int = 400
        self.height = 100
        self.width = 30
        self.image = pygame.image.load("game/assets/images/zebrafish.py")

    def set_pos_from_coords(self, coords: tuple[float, float]):
        """
        arguments:

        coords: tuple[float, float]
            normalized coords (x,y)
        """
        if coords:
            x = 800*coords[0]
            y = 600*coords[1]
            self.x = x
            self.y = y

    def get_coords(self):
        return (self.x, self.y)
    
