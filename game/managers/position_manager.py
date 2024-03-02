from utils import constants
from game.managers.collision_manager import CollisionManager
from game.assets.ball import Ball
from game.assets.paddle import Paddle
from game.assets.border import Borders
from utils.hand_detection import HandDetector


class PositionManager(object):
    """
    Manages object positions and updates them.
    """
    def __init__(self, 
                 hand_detector: HandDetector, 
                 paddle: Paddle, 
                 ball: Ball,
                 borders: Borders,
                 collision_manager: CollisionManager):
        self.hand_detector = hand_detector
        self.paddle = paddle
        self.ball = ball
        self.borders = borders
        self.collision_manager = collision_manager

    def update(self):
        """
        updates game object positions
        """
        self._update_paddle_position()
        self._update_embryo_position()
        self._detect_collisions()

    def _detect_collisions(self, should_detect_collision: bool):
        """
        detect all ball collision events
        """
        if should_detect_collision:
            self._detect_paddle()
            self._detect_top_border()
            self._detect_back_border()
            self._detect_bot_border()
        
    def _detect_paddle(self):
        top_coords = self.paddle.top_coords
        if (self.ball.x-self.ball.radius - top_coords[0]) <= 1:
            top_y = self.paddle.y-self.ball.radius
            bot_y = self.paddle.y+self.paddle.height+self.ball.radius
            if top_y < self.ball.y < bot_y:
                self.collision_manager.paddle_collision()

    def _detect_top_border(self):
        border_y = self.borders.top.y + self.borders.top.height
        embryo_y = self.ball.y - self.ball.radius
        if embryo_y - border_y <= 1:
            self.collision_manager.top_border_collision()

    def _detect_back_border(self):
        border_x = self.borders.back.x
        embryo_x = self.ball.x + self.ball.radius
        if border_x - embryo_x <= 1:
            self.collision_manager.back_border_collision()

    def _detect_bot_border(self):
        border_y = self.borders.bot.y
        embryo_y = self.ball.y + self.ball.radius
        if border_y - embryo_y <= 1:
            self.collision_manager.bottom_border_collision()

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
        