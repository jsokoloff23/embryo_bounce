from enum import Enum

class Mode(Enum):
    """
    enum class to track which mode game is in.
    """
    GAME = 0
    HIGH_SCORES = 1
    EXIT = 2
    MAIN_MENU = 3
    HIGH_SCORE_ENTRY = 4
    PLAY_AGAIN = 5