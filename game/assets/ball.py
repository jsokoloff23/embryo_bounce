class Ball(object):
    """
    ball object used in game.

    instance attributes:

    self.x: int
        normalized x

    self.y: int
        normalized y

    self.speed: int
        normalized speed

    self.x_vel: int
        normalzed x velocity

    self.y_vel: int = 0
        normalized y velocity

    self.radius: int = 0.02
        normalized radius
    """
    _MIN_SPEED = 1
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self._speed: int = -0.05
        self.x_vel: int = -self.speed
        self.y_vel: int = 0
        self.radius: int = 0.02

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
    
    def set_from_coords(self, coords):
        selfx, self.y = coords
