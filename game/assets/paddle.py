class Paddle(object):
    """
    paddle object used in game.

    x: int
        normalized x

    y: int
        normalized y

    height: int
        normalized height

    width: int:
        normalized width
    """
    def __init__(self):
        self.x: int = 0
        self._y: int = 0.5
        self.height = 0.02
        self.width = 0.005

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
    
