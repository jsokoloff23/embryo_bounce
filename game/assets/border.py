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
    def __init__(self, x: int, y: int, height: int, width: int, color: tuple[int, int, int]):
        self.x: int = x
        self.y: int = y
        self.height: int = height
        self.width: int = width
        self.color: tuple[int, int, int] = color
