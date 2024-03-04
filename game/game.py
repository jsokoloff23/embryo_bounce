import pygame

from utils import constants
from utils.hand_detection import HandDetector
from utils.camera import HandCam
from game.managers.display_manager import DisplayManager
from game.managers.position_manager import PositionManager
from game.managers.collision_manager import CollisionManager
from game.managers.sound_manager import SoundManager
from game.managers.high_score_manager import HighScoreManager
from game.assets.ball import Ball
from game.assets.paddle import Paddle
from game.assets.border import Borders
from game.mode import Mode


class Game(object):
    FRAMERATE = 60
    INIT_LIVES = 3
    INITIAL_WAIT_FRAMES = 2*FRAMERATE
    def __init__(self):
        #pygame.init() must be called
        pygame.init()
        self.hand_detector = HandDetector()
        self.hand_cam = HandCam(self.hand_detector)
        self.paddle = Paddle()
        self.ball = Ball()
        self.borders = Borders()
        self.sound_manager = SoundManager()
        self.display_manager = DisplayManager(
            self.hand_detector, self.hand_cam, self.paddle, self.ball, 
            self.borders)
        self.collision_manager = CollisionManager(
            self.ball, self.paddle, self.borders, self.sound_manager)
        self.position_manager = PositionManager(
            self.hand_detector, self.paddle, self.ball, self.borders, 
            self.collision_manager)
        self.high_score_manager = HighScoreManager()
        self.clock = pygame.time.Clock()
        self._reset_game_variables()
        self.button_num = 0

    def main(self):
        """
        game loop. First has to initial webcam and hand detection and then
        enters game loop.
        """
        self.hand_detector.set_landmarker()
        self.hand_cam.start()
        while True:
            if self.mode == Mode.GAME:
                self._manage_game_mode()
            elif self.mode == Mode.HIGH_SCORE_ENTRY:
                self._manage_hs_entry_mode()
            elif self.mode == Mode.PLAY_AGAIN:
                self._manage_play_again_mode()
            elif self.mode == Mode.MAIN_MENU:
                self._manage_menu_mode()
            
            self._tick_clock()

    def _change_mode(self, mode):
        #This condition is to avoid switching music when switching between
        #high scores and menu
        if self.mode == Mode.HIGH_SCORES:
            pass
        elif mode == Mode.GAME or mode == Mode.MAIN_MENU:
            self._reset_game_variables()
            self.sound_manager.update_music(mode)
        self.mode = mode

    def _get_key_events(self):
        """
        returns pygame events that are key presses
        """
        return [event for event in pygame.event.get() if event.type == pygame.KEYDOWN]

    def _increase_ball_speed(self):
        if self.frames_since_speed > self.framerate*5:
            self.ball.speed += constants.SPEED_INCREMENT
            self.frames_since_speed = 0

    def _is_ball_gone_update(self):
        self.is_ball_gone = self.position_manager.is_ball_gone()
        if self.is_ball_gone:
            self.sound_manager.play_mistake_sound()

    def _manage_ball_gone(self):
        self.position_manager.update()
        self.display_manager.game_update(self.lives, self.score)
        if self.position_manager.is_ball_gone():
            self.lives -= 1
            self._spawn_new_ball()
            self.is_ball_gone = False

    def _manage_game_mode(self):
        if self.lives:
            if self.frame_num < Game.INITIAL_WAIT_FRAMES:
                self.display_manager.game_update(self.lives, self.score)
            else:
                if not self.is_ball_gone:
                    self.position_manager.update()
                    self.display_manager.game_update(self.lives, self.score)
                    self._increase_ball_speed()
                    self.frames_no_ball = 0
                    self._is_ball_gone_update()
                else:
                    self._manage_ball_gone()
        else:
            if self.high_score_manager.is_high_score(self.score):
                self._change_mode(Mode.HIGH_SCORE_ENTRY)

    def _manage_hs_entry_mode(self):
        self.display_manager.high_score_entry_update(self.name)
        for event in self._get_key_events():
            if event.key == pygame.K_RETURN:
                #submits score and switches to play again.
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
                self.try_again = self.try_again[:-1]
            else:
                self.try_again += event.unicode

    def _manage_menu_mode(self):
        self.display_manager.menu_update(self.button_num)
        for event in self._get_key_events():
            if event.key == pygame.K_DOWN:
                #make sure user can only select button that exists
                if not self.button_num >= Game.NUM_MENU_BUTTONS - 1:
                    self.button_num += 1
            elif event.key == pygame.K_UP:
                #make sure user can only select button that exists
                if not self.button_num == 0:
                    self.button_num -= 1
            elif event.key == pygame.K_RETURN:
                self._change_mode(Mode(self.button_num))

    def _reset_game_variables(self):
        self.framerate = Game.FRAMERATE
        self.lives = Game.INIT_LIVES
        self.frame_num = 0
        self.frames_since_speed = 0
        self.frames_no_ball = 0
        self.is_ball_gone = False
        self.score = 0
        self.name = ""
        self.try_again = ""

    def _spawn_new_ball(self):
        self.ball = Ball()
        self.display_manager.ball = self.ball
        self.position_manager.ball = self.ball
        self.collision_manager.ball = self.ball

    def _tick_clock(self):
        self.clock.tick(self.framerate)
        self.frame_num += 1
        self.frames_since_speed += 1
        self.frames_no_ball += 1
        self.score += 1
        