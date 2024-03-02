import pygame

from utils import constants
from utils.hand_detection import HandDetector
from utils.camera import HandCam
from game.managers.display_manager import DisplayManager
from game.managers.position_manager import PositionManager
from game.managers.collision_manager import CollisionManager
from game.assets.ball import Ball
from game.assets.paddle import Paddle
from game.assets.border import Borders


class Game(object):
    FRAMERATE = 60
    INITIAL_WAIT_FRAMES = 2*FRAMERATE
    def __init__(self):
        #pygame.init() must be called
        pygame.init()
        self.hand_detector = HandDetector()
        self.hand_cam = HandCam(self.hand_detector)
        self.paddle = Paddle()
        self.ball = Ball()
        self.borders = Borders()
        self.display_manager = DisplayManager(
            self.hand_detector, self.hand_cam, self.paddle, self.ball, 
            self.borders)
        self.collision_manager = CollisionManager(self.ball, self.paddle, self.borders)
        self.position_manager = PositionManager(
            self.hand_detector, self.paddle, self.ball, self.borders, 
            self.collision_manager)
        self.clock = pygame.time.Clock()
        self.framerate = 60
        self.frame_num = 0
        self.lives = 3

    def main(self):
        """
        game loop. First has to initial webcam and hand detection and then
        enters game loop.
        """
        self.hand_detector.set_landmarker()
        self.hand_cam.start()
        while True:
            if self.lives:
                if self.frame_num < Game.INITIAL_WAIT_FRAMES:
                    self.display_manager.game_update()
                else:
                    if not self.is_ball_gone:
                        self.position_manager.update()
                        self.display_manager.game_update()
                        self._increase_ball_speed()
                        self.frames_no_ball = 0
                        self._is_ball_gone_update()
                    else:
                        self._manage_ball_gone()
            self._tick_clock()

    def _increase_ball_speed(self):
        if self.frames_since_speed > self.framerate*5:
            self.ball.speed += constants.SPEED_INCREMENT
            self.frames_since_speed = 0

    def _is_ball_gone_update(self):
        self.is_ball_gone = self.position_manager.is_ball_gone()

    def _manage_ball_gone(self):
        if self.position_manager.is_ball_gone():
            self.lives -= 1
            self._spawn_new_ball()
            self.is_ball_gone = False

    def _spawn_new_ball(self):
        self.ball = Ball()
        self.display_manager.ball = self.ball
        self.position_manager.ball = self.ball
        self.collision_manager.ball = self.ball

    def _tick_clock(self):
        self.clock.tick(self.framerate)
        self.frame_num += 1
        
