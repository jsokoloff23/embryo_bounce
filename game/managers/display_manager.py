import cv2
import numpy as np
import pygame

from game.managers.draw_manager import DrawManager
from game.assets.paddle import Paddle
from game.assets.ball import Ball
from utils.hand_detection import HandDetector
from utils.camera import HandCam
from utils import constants


class DisplayManager():
    def __init__(self, 
                 hand_detector: HandDetector,
                 hand_cam: HandCam,
                 paddle: Paddle, 
                 ball: Ball):
        self.hand_detector = hand_detector
        self.hand_cam = hand_cam
        self.paddle = paddle
        self.ball = ball
        self.draw_manager = DrawManager()
        self.size = (800, 720)
        self.cam_size = self._init_cam_size()
        self.cam_coords = (0, 0)
        self.bg_coords = (0, 0)
        self.bg_size = (800, 600)
        self.game_coords = (0, self.cam_size[1])
        self.display = pygame.display.set_mode(self.size)

    def update(self):
        self._init_bg_surface()
        self._set_cam_surface()
        self._blit_bg_surface()
        self._blit_cam_surface()
        self._blit_game_surface()
        pygame.display.update()

    def _init_cam_size(self):
        aspect_ratio = self.hand_cam.aspect_ratio
        return (int(constants.CAM_H*aspect_ratio), constants.CAM_H)

    def _set_cam_surface(self):
        if self.hand_detector.image is not None:
            frame = self.hand_detector.image
            #resize webcam image to standardized size
            frame = cv2.resize(frame, self.cam_size)
            #frame requires rotation to match pygame orientation
            frame = np.rot90(frame)
            #cv2 cap uses BGR instead of RGB, but pygame uses RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.cam_surface = pygame.surfarray.make_surface(frame)
        else:
            #Only occurs before webcam stream initializes
            #3 for number of color channels
            shape = (self.cam_size[0], self.cam_size[1], 3)
            frame = np.ones(shape)*constants.WHITE
            self.cam_surface = pygame.surfarray.make_surface(frame)

    def _blit_bg_surface(self):
        self.display.blit(self.bg_surface, self.bg_coords)

    def _blit_cam_surface(self):
        self.display.blit(self.cam_surface, self.cam_coords)
    
    def _blit_cam_surface(self):
        self.display.blit(self.game_surface, self.game_coords)

    def _draw_game(self):
        self.draw_manager.draw_border(self.game_surface, self.borders.top)
        self.draw_manager.draw_border(self.game_surface, self.borders.back)
        self.draw_manager.draw_border(self.game_surface, self.borders.bot)
        self.draw_manager.draw_ball(self.bg_surface, self.ball)
        self.draw_manager.draw_paddle(self.bg_surface, self.paddle)

    def _init_bg_surface(self):
        #3 for number of color channels
        bg_shape = (self.size[0], self.size[1], 3)
        bg_array = np.ones(bg_shape)*constants.LIGHT_BLUE
        self.bg_surface = pygame.surfarray.make_surface(bg_array)

    def _init_game_surface(self):
        game_surface = pygame.image.load("game/assets/images/background.jpg")
        self.game_surface = pygame.transform.scale(game_surface, self.bg_size)
    