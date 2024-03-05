import copy
import time

import mediapipe as mp
import numpy as np

from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import HandLandmarkerResult, RunningMode
from mediapipe.framework.formats import landmark_pb2

from utils import constants


class HandDetector(object):
    """
    Creates and manages hand_landmarker which receives images from HandCam
    and processes the images to get a HandLandmarkerResult. Result and 
    received image for result are then accessed via result and image
    properties.

    With results, calculates current hand position with normalized coordinates.
    """
    #hand landmarks to be used in tracking
    LM_1 = 5
    LM_2 = 9
    LM_3 = 13
    def __init__(self):
        self._result = None
        self._image = None
        self.model_asset_path = constants.HAND_MODEL_PATH
        self.num_hands = 1
        self.min_hand_detection_confidence=0.2
        self.min_hand_presence_confidence=0.2
        self.min_tracking_confidence=0.2
        self.running_mode = RunningMode.LIVE_STREAM
        self.start_time = time.time()

    #@property to make them read-only
    @property
    def result(self):
        return self._result
    
    @property
    def image(self):
        return self._image

    def set_landmarker(self):
        #Making this function a class attribute crashes mediapipe without
        #a logged error or exception, so define it here instead.
        def set_result(result: HandLandmarkerResult, 
                       output_image: mp.Image, 
                       timestamp_ms: int):
            #output image can't be modofied so make modifiable copy
            self._image = copy.deepcopy(output_image.numpy_view())
            self._result = result
        
        options = self._get_options(result_callback=set_result)
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def detect_async(self, image):
        #multiply by 1000 to get ms
        time_ms = int((time.time() - self.start_time)*1000)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        self.landmarker.detect_async(mp_image, time_ms)

    def draw_landmarks_on_image(self) -> np.ndarray:
        #This method should go somewhere else. Perhaps just in testing.
        """Adapted from https://github.com/googlesamples/mediapipe/blob/main/examples/hand_landmarker/python/hand_landmarker.ipynb
        
        returns rgb_image with hand landmarks overlayed.

        parameters:

        rgb_image: np.ndarray
            rgb ndarray to be overlayed.

        returns:

        overlayed_image: np.ndarray | None
            rgb_image with hand landmarks overlayed on it.
            Or, if self.result is None, returns None.
        """
        if self.result is None:
            return None
        annotated_image = np.copy(self.image)
        for hand_landmarks in self.result.hand_landmarks:
            proto = self._get_normalized_proto(hand_landmarks)
            mp.solutions.drawing_utils.draw_landmarks(
            annotated_image,
            proto,
            mp.solutions.hands.HAND_CONNECTIONS,
            mp.solutions.drawing_styles.get_default_hand_landmarks_style(),
            mp.solutions.drawing_styles.get_default_hand_connections_style())
        return annotated_image
        
    def get_norm_coords(self) -> tuple[float, float]:
        """
        if self.result is None, returns None. Else, returns normalized coords of 
        hand and returns it as (x,y) tuple.

        """
        for lmarks in self.result.hand_landmarks:
            #Index 9 is MIDDLE_FINGER_MCP landmark. see https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
            return(lmarks[9].x, lmarks[9].y)
            
    def _get_normalized_proto(self, hand_landmarks) -> landmark_pb2.NormalizedLandmarkList:
        proto = landmark_pb2.NormalizedLandmarkList()
        proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(
                x=l.x, y=l.y, z=l.z) for l in hand_landmarks
        ])
        return proto
    
    def _get_options(self, result_callback) -> vision.HandLandmarkerOptions:
        """
        returns HandLandmarkerOptions instance using instance attributes as 
        arguments.

        parameters:
        
        result_callback: Callable
            function to be used as callback for landmarker results
        
        returns:

        options: HandLandmarkerOptions
            returns HandLandmarkerOptions object using instance attributes and
            result_callback as arguments.
        """
        options = vision.HandLandmarkerOptions(
            base_options = BaseOptions(model_asset_path=self.model_asset_path),
            num_hands=self.num_hands,
            min_hand_detection_confidence=self.min_hand_detection_confidence,
            min_hand_presence_confidence=self.min_hand_presence_confidence, 
            min_tracking_confidence=self.min_tracking_confidence,
            running_mode=self.running_mode,
            result_callback=result_callback)
        return options
    