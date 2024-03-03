from enum import Enum

class Mode(Enum):
    """
    enum class to track which mode game is in.
    """
    MAIN_MENU = 0
    HIGH_SCORES = 1
    EXIT = 2
    GAME = 3
    HIGH_SCORE_ENTRY = 4