import cv2
import numpy as np
import pygame

from game.assets.paddle import Paddle
from game.assets.ball import Ball
from hand_tracking.hand_detector import HandDetector
from hand_tracking.camera import HandCam


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
        self.size = (800, 720)
        self.cam_size = (160, 120)
        self.cam_coords = (0, 0)
        self.display = pygame.display.set_mode(self.size)

    def update(self):
        self._set_cam_surface()
        pygame.display.update()

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
            frame = np.ones(shape)*(255, 255, 255)
            self.cam_surface = pygame.surfarray.make_surface(frame)
        self.display.blit(self.cam_surface, self.cam_coords)
    