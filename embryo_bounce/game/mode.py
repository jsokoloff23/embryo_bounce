"""
This module contains the Mode enum which is used to control which
mode game is in.
"""

from enum import Enum


class Mode(Enum):
    """
    enum class to track which mode game is in.
    """
    GAMEPLAY = 0
    HIGH_SCORES = 1
    EXIT = 2
    MAIN_MENU = 3
    HIGH_SCORE_ENTRY = 4
    PLAY_AGAIN = 5
