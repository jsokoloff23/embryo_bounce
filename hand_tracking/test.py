import cv2
import mediapipe as mp
from camera import Cam
from hand_functions import HandDetector
import mediapipe
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import HandLandmarkerResult
from mediapipe.tasks.python.vision import RunningMode

hand_detector = HandDetector()
cam = Cam()
with vision.HandLandmarker.create_from_options(hand_detector.options) as landmarker:
    cam.start_stream(landmarker)
