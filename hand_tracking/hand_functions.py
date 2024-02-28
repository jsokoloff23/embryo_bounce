import mediapipe
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import HandLandmarkerResult
from mediapipe.tasks.python.vision import RunningMode


def print_result(result: HandLandmarkerResult, output_image: mediapipe.Image, timestamp_ms: int):
    print('hand landmarker result: {}'.format(result))

class HandDetector(object):
    def __init__(self):
        self.model_path = r"C:\Users\marim\Desktop\hand_pong\hand_landmarker.task"
        self.options = self.get_options()
        
    def get_options(self):
        base_options = BaseOptions(model_asset_path=self.model_path)
        running_mode = RunningMode.LIVE_STREAM
        return vision.HandLandmarkerOptions(base_options=base_options,
                                            running_mode=running_mode,
                                            result_callback=print_result)
    
    def print_result(result: HandLandmarkerResult, output_image: mediapipe.Image, timestamp_ms: int):
        print('hand landmarker result: {}'.format(result))
    
    def start_stream(self, cam):
        with vision.HandLandmarker.create_from_options(self.options) as landmarker:
            cam.start_stream(landmarker)