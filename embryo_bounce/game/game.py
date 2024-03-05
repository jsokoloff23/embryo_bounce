"""
This module contains the Game class which is the main class created to start
game

TODO This could be split into multiple classes. Each mode could be made 
into its own separate class.
"""

import sys

import pygame

from game.mode import Mode
from game.assets.ball import Ball
from game.assets.border import Borders
from game.assets.paddle import Paddle
from game.managers import DisplayManager, PositionManager, CollisionManager, HighScoreManager, SoundManager
from utils import constants
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
    FRAMERATE = 60
    INIT_LIVES = 3
    #number of frames before ball moves at the beginning
    INITIAL_WAIT_FRAMES = FRAMERATE*2
    #number of frames before ball respawns
    NO_BALL_FRAMES = FRAMERATE*2
    #frames before ball speed increases
    FRAMES_NO_SPEED = FRAMERATE*5
    #number of options on menu
    NUM_MENU_BUTTONS = 3
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
        #initialize game settings and variables
        self.clock = pygame.time.Clock()
        self.framerate = Game.FRAMERATE
        self.lives = Game.INIT_LIVES
        self.frame_num = 0
        self.frames_since_speed = 0
        self.frames_no_ball = 0
        self.is_ball_gone = False
        self.score = 0
        self.name = ""
        self.try_again = ""
        self.button_num = 0

    def main(self):
        """
        game loop. First has to initial webcam and hand detection and then
        enters game loop.
        """
        self.hand_detector.set_landmarker()
        self.hand_cam.start()
        self.sound_manager.play_menu_song()
        self._initialize_game_variables()
        while True:
            #Depending on mode of game, selects display and event management.
            if self.mode == Mode.GAME:
                self._manage_game_mode()
            elif self.mode == Mode.HIGH_SCORES:
                self._manage_hs_mode()
            elif self.mode == Mode.EXIT:
                self._manage_exit_mode()
            elif self.mode == Mode.MAIN_MENU:
                self._manage_menu_mode()
            elif self.mode == Mode.HIGH_SCORE_ENTRY:
                self._manage_hs_entry_mode()
            elif self.mode == Mode.PLAY_AGAIN:
                self._manage_play_again_mode()
            #clock tick is to increment variables and run game at consistent
            #frame rate
            self._tick_clock()

    def _change_mode(self, mode):
        """
        changes current mode to mode.
        """
        #This condition is to avoid switching music when switching between
        #high scores and menu
        if self.mode == Mode.HIGH_SCORES:
            pass
        elif mode == Mode.GAME or mode == Mode.MAIN_MENU:
            self._initialize_game_variables()
            self.sound_manager.update_music(mode)
        self.mode = mode

    def _get_key_events(self):
        """
        returns pygame events that are key presses
        """
        return [event for event in pygame.event.get() if event.type == pygame.KEYDOWN]
                
    def _increase_ball_speed(self):
        """
        increase ball speed by constants.SPEED_INCREMENT
        """
        if self.frames_since_speed > Game.FRAMES_NO_SPEED:
            self.ball.speed += constants.SPEED_INCREMENT
            self.frames_since_speed = 0

    def _is_ball_gone_update(self):
        """
        Updates is_ball_gone flag to position_manager.is_ball_gone().
        If is_ball_gone is True, plays mistake sound.
        """
        self.is_ball_gone = self.position_manager.is_ball_gone()
        if self.is_ball_gone:
            self.sound_manager.play_mistake_sound()

    def _manage_ball_gone(self):
        """
        event manager when ball is gone
        """
        self.position_manager.update(False)
        self.display_manager.game_update(self.score, self.lives)
        if self.frames_no_ball > Game.NO_BALL_FRAMES:
            self.lives -= 1
            self._spawn_new_ball()
            self.is_ball_gone = False

    def _manage_exit_mode(self):
        """
        event manager when mode is EXIT
        """
        #For some reason, cam feed doesn't die on sys.exit(), so stop manually
        self.hand_cam.stop_stream()
        pygame.quit()
        sys.exit()

    def _manage_game_mode(self):
        """
        event manager when mode is GAME
        """
        for event in self._get_key_events():
            #escape returns to main menu
            if event.key == pygame.K_ESCAPE:
                self._change_mode(Mode.MAIN_MENU)
        if self.lives:
            #waits at the beginning of the game for ball to start moving
            if self.frame_num < Game.INITIAL_WAIT_FRAMES:
                self.score = 0
                self.position_manager.update(False)
                self.display_manager.game_update(self.score, self.lives)
            #normal game loop with ball moving
            else:
                if not self.is_ball_gone:
                    self.position_manager.update()
                    self.display_manager.game_update(self.score, self.lives)
                    self._increase_ball_speed()
                    self.frames_no_ball = 0
                    self._is_ball_gone_update()
                #when ball disappears, use manage_ball_gone() to manage events
                else:
                    self._manage_ball_gone()
        #when lives are out, either enter high score or go to play again.
        else:
            if self.high_score_manager.is_high_score(self.score):
                self._change_mode(Mode.HIGH_SCORE_ENTRY)
            else:
                self._change_mode(Mode.PLAY_AGAIN)

    def _manage_hs_entry_mode(self):
        self.display_manager.high_score_entry_update(self.name)
        for event in self._get_key_events():
            if event.key == pygame.K_RETURN:
                #on RETURN press, submits score and changes mode to PLAY_AGAIN.
                self.high_score_manager.write_new_high_score(
                    self.name, self.score)
                self._change_mode(Mode.PLAY_AGAIN)
            elif event.key == pygame.K_BACKSPACE:
                #removes character on backspace
                self.name = self.name[:-1]
            else:
                #adds character
                if len(self.name) <= constants.NAME_CHARACTER_LIMIT:
                    self.name += event.unicode

    def _manage_hs_mode(self):
        entries = self.high_score_manager.get_entries()
        self.display_manager.high_score_update(entries)
        for event in self._get_key_events():
            if event.key == pygame.K_ESCAPE:
                self._change_mode(Mode.MAIN_MENU)

    def _manage_play_again_mode(self):
        self.display_manager.play_again_update(self.try_again)
        for event in self._get_key_events():
            if event.key == pygame.K_RETURN:
                #on enter press, if y or Y is entered, start new game
                if self.try_again in ["y", "Y"]:
                    self._change_mode(Mode.GAME)
                #on enter press, if y or Y is entered, start new game
                elif self.try_again in ["n", "N"]:
                    self._change_mode(Mode.MAIN_MENU)
                #if neither y nor were entered, reset prompt
                else:
                    self.try_again = ""
            elif event.key == pygame.K_BACKSPACE:
                #removes character on backspace
                self.try_again = self.try_again[:-1]
            else:
                #addes character
                self.try_again += event.unicode

    def _manage_menu_mode(self):
        self.display_manager.menu_update(self.button_num)
        for event in self._get_key_events():
            if event.key == pygame.K_DOWN:
                #make sure user can only select button that exists
                if self.button_num < Game.NUM_MENU_BUTTONS:
                    self.button_num += 1
            elif event.key == pygame.K_UP:
                #make sure user can only select button that exists
                if self.button_num != 0:
                    self.button_num -= 1
            elif event.key == pygame.K_RETURN:
                #Menu mode selection lines up with Mode enums, so button_num
                #selects correct mode
                self._change_mode(Mode(self.button_num))

    def _initialize_game_variables(self):
        self.framerate = Game.FRAMERATE
        self.lives = Game.INIT_LIVES
        self.frame_num = 0
        self.frames_since_speed = 0
        self.frames_no_ball = 0
        self.is_ball_gone = False
        self.score = 0
        self.name = ""
        self.try_again = ""
        self.button_num = 0

    def _spawn_new_ball(self):
        self.ball = Ball()
        #TODO make an event that auto updates ball in managers.
        self.display_manager.ball = self.ball
        self.position_manager.ball = self.ball
        self.collision_manager.ball = self.ball
                    
    def _tick_clock(self):
        #tick(framerate) keeps game at consistent framerate.
        self.clock.tick(self.framerate)
        self.frame_num += 1
        self.frames_since_speed += 1
        self.frames_no_ball += 1
        self.score += 1
