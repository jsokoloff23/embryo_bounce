import cv2

from threading import Thread

from utils.hand_detection import HandDetector


class HandCam(Thread):
    """
    Handcam streams images from the webcam and sends them to the hand detector
    to be processed by hand tracking.

    Constructor Parameters:

    hand_detector: utils.HandDetector
        hand_detector that images are streamed to

    index: int = 0
        index of webcam to be used
    """
    def __init__(self, hand_detector: HandDetector, index: int = 0):
        #Thread init() must be called or else exception is raised
        super().__init__()
        self.cap = cv2.VideoCapture(index)
        self.is_stopped = False
        self.hand_detector = hand_detector

    def start_stream(self):
        """
        Starts capturing of images and sends stream to hand_detection.
        """
        while not self.is_stopped:
            captured, image = self.cap.read()
            if captured:
                self.hand_detector.detect_async(image)
        #release when feed is stopped by is_stopped flag
        self.cap.release()
        
    def stop_stream(self):
        self.is_stopped = True
        
    def run(self):
        """
        starts stream. Should be called by Thread.start() method to run in
        separate thread.
        """
        self.start_stream()

