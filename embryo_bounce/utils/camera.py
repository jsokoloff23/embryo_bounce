"""
This module contains all implementation of the webcam interface.
"""

from threading import Thread

import cv2

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

    Implements:
    
    thread.Thread
    """
    def __init__(self, hand_detector: HandDetector, index: int = 0):
        #Thread init() must be called or else exception is raised
        super().__init__()
        self.cap = cv2.VideoCapture(index)
        self._fps = self._init_fps()
        self._shape = self._init_shape()
        self._dtype = self._init_dtype()
        self._aspect_ratio = self._init_aspect_ratio()
        self.is_stopped = False
        self.hand_detector = hand_detector
    
    #@property to make them read-only
    @property
    def fps(self):
        return self._fps
    
    @property
    def shape(self):
        return self._shape
    
    @property
    def dtype(self):
        return self._dtype 
    
    @property
    def aspect_ratio(self):
        return self._aspect_ratio 

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

    def _init_fps(self):
        """
        returns frames per second of camera
        """
        return self.cap.get(cv2.CAP_PROP_FPS)
    
    def _init_shape(self):
        """
        returns shape of image returned by cam as tuple 
        (height, width, num_channels)
        """
        captured, image = self.cap.read()
        if captured:
            return image.shape
        
    def _init_aspect_ratio(self):
        return self.shape[1]/self.shape[0]
    
    def _init_dtype(self):
        captured, image = self.cap.read()
        if captured:
            return image.dtype
        
    def stop_stream(self):
        """
        Sets self.is_stopped to True to stop image stream.
        """
        self.is_stopped = True
        
    def run(self):
        """
        starts stream. Should be called by Thread.start() method to run in
        separate thread.
        """
        self.start_stream()
