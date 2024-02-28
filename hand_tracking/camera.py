import cv2
import numpy as np
import mediapipe as mp
import time

class Cam(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
    
    def start_stream(self, landmarker):
        i = 0
        while True:
            succes, img = self.cap.read()
            i += 1
            flipped = np.array(np.flip(img, 1))
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=flipped)
            landmarker.detect_async(mp_image, i)
            cv2.imshow('frame', flipped)
            if cv2.waitKey(1) == ord('q'):
                break

    def stop_stream(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def not_found(self):
        return not self.cap.isOpened()

