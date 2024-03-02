from utils import constants
from game.assets.ball import Ball
from game.assets.paddle import Paddle
from utils.hand_detection import HandDetector


class PositionManager(object):
    """
    Manages object positions and updates them.
    """
    def __init__(self, 
                 hand_detector: HandDetector, 
                 paddle: Paddle, 
                 ball: Ball):
        self.hand_detector = hand_detector
        self.paddle = paddle
        self.ball = ball

    def update(self):
        """
        updates game object positions
        """
        self._update_paddle_position()
        self._update_embryo_position()

    def _update_paddle_position(self):
        """
        updates paddle position with hand coordinates
        """
        hand_coords = self.hand_detector.get_norm_coords()
        #get_coords() returns None if no detector results
        if hand_coords:
            #scaling so that user doesn't have to use full webcam field of view
            #to move paddle
            scaling = constants.HAND_POSITION_SCALING
            #offset to correct for scaling
            offset = constants.HAND_COORDS_OFFSET
            y = (hand_coords[1]*constants.GAME_Y_SIZE)*scaling + offset
            self.paddle.y = y

    def _update_embryo_position(self):
        """
        updates embryo position
        """
        self.ball.x += self.ball.x_vel
        self.ball.y += self.ball.y_vel