"""
This module contains the SoundManager class, which controls sound in the game
"""

import pygame

from game.mode import Mode
from utils import constants


class SoundManager(object):
    """
    Class used to control sounds in game.

    Constructor Parameters:

    mode: Mode
        current mode of game
    """
    def __init__(self, mode: Mode):
        self.paddle_sound = pygame.mixer.Sound(constants.PADDLE_SOUND_PATH)
        self.mistake_sound = pygame.mixer.Sound(constants.MISTAKE_SOUND_PATH)
        self.mode = mode
    
    def update_music(self, mode: Mode):
        #don't want to restart song if mode isn't changed
        if mode != self.mode:
            self.mode = mode
            if self.mode == Mode.GAME:
                self.play_game_song()
            elif self.mode == Mode.MAIN_MENU:
                self.play_menu_song()
    
    def play_game_song(self):
        """
        plays game song on infinite loop
        """
        pygame.mixer.music.load(constants.GAME_SONG_PATH)
        #-1 causes song to loop
        pygame.mixer.music.play(-1)

    def play_menu_song(self):
        """
        plays menu song on infinite loop
        """
        pygame.mixer.music.load(constants.MENU_SONG_PATH)
        pygame.mixer.music.play(-1)

    def play_paddle_sound(self):
        """
        plays paddle sound
        """
        self.paddle_sound.play()

    def play_mistake_sound(self):
        """
        plays paddle sound
        """
        self.mistake_sound.play()
