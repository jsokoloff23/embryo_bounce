import cv2
import mediapipe as mp
from camera import Cam
from hand_functions import HandDetection
import mediapipe
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import HandLandmarkerResult
from mediapipe.tasks.python.vision import RunningMode

hand_detection = HandDetection()
hand_detection.start()
