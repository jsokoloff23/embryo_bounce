import pygame
import cv2
from hand_tracking.hand_detector import HandDetector
from hand_tracking.camera import HandCam


class Game(object):
    def __init__(self):
        #pygame.init() must be called
        pygame.init()
        self.hand_detector = HandDetector()
        self.hand_cam = HandCam(self.hand_detector)

    def main(self):
        """
        game loop. First has to initial webcam and hand detection and then
        enters game loop.
        """
        self.hand_detector.set_landmarker()
        self.hand_cam.start()
        while True:
            image = self.hand_detector.image
            if image is not None:
                cv2.imshow("frame", image)
