"""
This module contains classes that manage events based on the mode
set within the main game loop. There's one for each enum in the mode
Enum class.
"""

import sys

import pygame

from game.assets.ball import Ball
from game.assets.border import Borders
from game.assets.paddle import Paddle
from game.managers import DisplayManager, PositionManager, CollisionManager, HighScoreManager, SoundManager
from game.mode import Mode
from utils import constants
from utils.camera import HandCam


class Gameplay():
    """
    manages events while in GAMEPLAY mode
    """
    FRAMERATE = 60
    INIT_LIVES = 3
    #number of frames before ball moves at the beginning
    INITIAL_WAIT_FRAMES = FRAMERATE*2
    #number of frames before ball respawns
    NO_BALL_FRAMES = FRAMERATE*2
    #frames before ball speed increases
    FRAMES_NO_SPEED = FRAMERATE*5
    def __init__(self, 
                 ball: Ball, 
                 paddle: Paddle, 
                 borders: Borders, 
                 position_manager: PositionManager, 
                 display_manager: DisplayManager, 
                 sound_manager: SoundManager, 
                 collision_manager: CollisionManager):
        self.ball = ball
        self.paddle = paddle
        self.borders = borders
        self.position_manager = position_manager
        self.display_manager = display_manager
        self.sound_manager = sound_manager
        self.collision_manager = collision_manager
        #initialize game settings and variables
        self.clock = pygame.time.Clock()
        self.framerate = Gameplay.FRAMERATE
        self.lives = Gameplay.INIT_LIVES
        self.frame_num = 0
        self.frames_since_speed = 0
        self.frames_no_ball = 0
        self.is_ball_gone = False
        self.score = 0
    
    def manage_events(self):
        while self.lives != 0:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    #escape returns to main menu
                    if event.key == pygame.K_ESCAPE:
                        return None
                    #waits at the beginning of the game for ball to start moving
            if self.frame_num < Gameplay.INITIAL_WAIT_FRAMES:
                self.score = 0
                self.position_manager.update(False)
                self.display_manager.game_update(self.lives, self.score)
            #normal game loop with ball moving
            else:
                if not self.is_ball_gone:
                    self.position_manager.update()
                    self.display_manager.game_update(self.lives, self.score)
                    self._increase_ball_speed()
                    self.frames_no_ball = 0
                    self._is_ball_gone_update()
                #when ball disappears, use manage_ball_gone() to manage events
                else:
                    self._manage_ball_gone()
            self._tick_clock()
        return self.score

    def _increase_ball_speed(self):
        """
        increase ball speed by constants.SPEED_INCREMENT
        """
        if self.frames_since_speed > Gameplay.FRAMES_NO_SPEED:
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
        self.display_manager.game_update(self.lives, self.score)
        if self.frames_no_ball > Gameplay.NO_BALL_FRAMES:
            self.lives -= 1
            self._spawn_new_ball()
            self.is_ball_gone = False

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


class HighScores():
    """
    manages events while in HIGH_SCORES mode
    """
    def __init__(self, 
                 display_manager: DisplayManager, 
                 high_score_manager: HighScoreManager):
        self.display_manager = display_manager
        self.high_score_manager = high_score_manager

    def manage_events(self):
        entries = self.high_score_manager.get_entries()
        #just a still image since it's only updated once!
        self.display_manager.high_score_update(entries)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return Mode.MAIN_MENU


class Exit():
    def __init__(self, hand_cam: HandCam):
        self.hand_cam = hand_cam

    def manage_events(self):
        self.hand_cam.stop_stream()
        pygame.quit()
        sys.exit()


class MainMenu():
    """
    manages events while in MAIN_MENU mode
    """
    NUM_MENU_BUTTONS = 3
    def __init__(self, display_manager: DisplayManager):
        self.display_manager = display_manager
        self.button_num = 0

    def manage_events(self):
        while True:
            self.display_manager.menu_update(self.button_num)
            for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_DOWN:
                            #make sure user can only select button that exists
                            if self.button_num < MainMenu.NUM_MENU_BUTTONS:
                                self.button_num += 1
                        elif event.key == pygame.K_UP:
                            #make sure user can only select button that exists
                            if self.button_num != 0:
                                self.button_num -= 1
                        elif event.key == pygame.K_RETURN:
                            #menu mode selection lines up with Mode enums, so 
                            #button_numselects correct mode
                            return Mode(self.button_num)
                        
class HighScoreEntry():
    """
    manages events while in HIGH_SCORE_ENTRY mode
    """
    def __init__(self, display_manager:DisplayManager, 
                 high_score_manager: HighScoreManager,
                 score: int):
        self.display_manager = display_manager
        self.high_score_manager = high_score_manager
        self.score = score
        self.name = ""

    def manage_events(self):
        while True:
            self.display_manager.high_score_entry_update(self.name)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        #on RETURN press, submits score
                        self.high_score_manager.write_new_high_score(
                            self.name, self.score)
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        #removes character on backspace
                        self.name = self.name[:-1]
                    else:
                        #adds character
                        if len(self.name) <= constants.NAME_CHARACTER_LIMIT:
                            self.name += event.unicode

class PlayAgain():
    """
    manages events while in PLAY_AGAIN mode
    """
    def __init__(self, display_manager: DisplayManager):
        self.display_manager = display_manager
        self.try_again = ""

    def manage_events(self):
        while True:
            self.display_manager.play_again_update(self.try_again)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        #on enter press, if y or Y is entered, start new game
                        if self.try_again in ["y", "Y"]:
                            return Mode.GAMEPLAY
                        #on enter press, if y or Y is entered, start new game
                        elif self.try_again in ["n", "N"]:
                            return Mode.MAIN_MENU
                        #if neither y nor were entered, reset prompt
                        else:
                            self.try_again = ""
                    elif event.key == pygame.K_BACKSPACE:
                        #removes character on backspace
                        self.try_again = self.try_again[:-1]
                    else:
                        #addes character
                        self.try_again += event.unicode
                        