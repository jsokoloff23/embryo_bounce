import pygame

from utils.hand_detection import HandDetector
from utils.camera import HandCam
from game.display_manager import DisplayManager
from game.position_manager import PositionManager
from game.assets.ball import Ball
from game.assets.paddle import Paddle
from game.assets.border import Borders


class Game(object):
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
        self.position_manager = PositionManager(
            self.hand_detector, self.paddle, self.ball, self.borders)
        self.clock = pygame.time.Clock()
        self.frame_rate = 60

    def main(self):
        """
        game loop. First has to initial webcam and hand detection and then
        enters game loop.
        """
        self.hand_detector.set_landmarker()
        self.hand_cam.start()
        while True:
            self.display_manager.update()
            self.position_manager.update()
            self.clock.tick(self.frame_rate)
