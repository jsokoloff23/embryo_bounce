"""
This module contains the Game class which is the main class created to start
game
"""

import pygame

from game.assets.ball import Ball
from game.assets.border import Borders
from game.assets.paddle import Paddle
from game.managers import DisplayManager, PositionManager, CollisionManager, HighScoreManager, SoundManager
from game.managers.mode_managers import Gameplay, HighScores, Exit, MainMenu, HighScoreEntry, PlayAgain
from game.mode import Mode
from utils.camera import HandCam
from utils.hand_detection import HandDetector


class Game(object):
    """
    Main class of the program.

    On initialization, initializes pygame, initializes webcame and hand
    detection, initializes game objects, and initializes managers.

    Methods:
    
    main()
        Initializes webcam and hand detection, and then starts game loop
    """
    def __init__(self):
        #pygame.init() must be called
        pygame.init()
        self.mode = Mode.MAIN_MENU
        #initialize utils
        self.hand_detector = HandDetector()
        self.hand_cam = HandCam(self.hand_detector)
        #initialize objects
        self.paddle = Paddle()
        self.ball = Ball()
        self.borders = Borders()
        #initialize managers
        self.sound_manager = SoundManager(self.mode)
        self.display_manager = DisplayManager(
            self.hand_detector, self.hand_cam, self.paddle, self.ball, 
            self.borders)
        self.collision_manager = CollisionManager(
            self.ball, self.paddle, self.borders, self.sound_manager)
        self.position_manager = PositionManager(
            self.hand_detector, self.paddle, self.ball, self.borders, 
            self.collision_manager)
        self.high_score_manager = HighScoreManager()

    def main(self):
        """
        game loop. First has to initial webcam and hand detection and then
        enters game loop.
        """
        self.hand_detector.set_landmarker()
        self.hand_cam.start()
        self.sound_manager.play_menu_song()
        while True:
            #Depending on mode of game, selects display and event management.
            if self.mode == Mode.GAMEPLAY:
                gameplay = Gameplay(ball=self.ball,
                                    paddle=self.paddle,
                                    borders=self.borders,
                                    position_manager=self.position_manager,
                                    display_manager=self.display_manager,
                                    sound_manager=self.sound_manager,
                                    collision_manager=self.collision_manager,
                                    high_score_manager=self.high_score_manager)
                mode = gameplay.manage_events()
                score = gameplay.score
            elif self.mode == Mode.HIGH_SCORES:
                high_scores = HighScores(display_manager=self.display_manager,
                                         high_score_manager=self.high_score_manager)
                high_scores.manage_events()
                mode = Mode.MAIN_MENU
            elif self.mode == Mode.EXIT:
                #named exit manager to avoid exit keyword
                exit_manager = Exit(self.hand_cam)
                exit_manager.manage_events()
            elif self.mode == Mode.MAIN_MENU:
                main_menu = MainMenu(self.display_manager)
                mode = main_menu.manage_events()
            elif self.mode == Mode.HIGH_SCORE_ENTRY:
                try:
                    hs_entry = HighScoreEntry(display_manager=self.display_manager,
                                              high_score_manager=self.high_score_manager,
                                              score=score)
                    hs_entry.manage_events()
                #if score hasn't been initialized
                except AttributeError:
                    pass
                mode = Mode.PLAY_AGAIN
            elif self.mode == Mode.PLAY_AGAIN:
                play_again = PlayAgain(self.display_manager)
                mode = play_again.manage_events()
            self._change_mode(mode)
            #clock tick is to increment variables and run game at consistent
            #frame rate

    def _change_mode(self, mode):
        """
        changes current mode to mode.
        """
        #This condition is to avoid switching music when switching between
        #high scores and menu
        if self.mode == Mode.HIGH_SCORES:
            pass
        elif mode == Mode.GAMEPLAY or mode == Mode.MAIN_MENU:
            self.sound_manager.update_music(mode)
        self.mode = mode
    
