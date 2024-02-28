import mediapipe as mp
import cv2
import numpy as np
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import HandLandmarkerResult
from mediapipe.tasks.python.vision import RunningMode
from threading import Thread


#For some reason, callback as a class attribute causes program to crash
#without an excption call or error, so define the callback separately. 
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    hand_world_landmarks = result.hand_world_landmarks
    if hand_world_landmarks:
        for landmark in hand_world_landmarks:
            print(landmark[9])

class HandDetection(Thread):
    def __init__(self):
        super().__init__()
        self.capture = cv2.VideoCapture(0)
        self.model_path = r"C:\Users\marim\Desktop\hand_pong\hand_landmarker.task"
        self.base_options = BaseOptions(model_asset_path=self.model_path)
        self.running_mode = RunningMode.LIVE_STREAM
        self.options = vision.HandLandmarkerOptions(
            base_options=self.base_options, running_mode=self.running_mode, result_callback=print_result)

    def start_stream(self):
        with vision.HandLandmarker.create_from_options(self.options) as landmarker:
            cap = cv2.VideoCapture(0)
            frame_num = 0
            while True:
                img = cap.read()[1]
                flipped = np.array(np.flip(img, 1))
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=flipped)
                landmarker.detect_async(mp_image, frame_num)
                cv2.imshow('frame', flipped)
                frame_num += 1

    def stop_stream(self):
        self.cap.release()
        cv2.destroyAllWindows()


    def run(self):
        self.start_stream()
