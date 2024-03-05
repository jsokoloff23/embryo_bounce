"""
This module contains the PositionManager class which manages object
positions.
"""

from game.assets.ball import Ball
from game.assets.border import Borders
from game.assets.paddle import Paddle
from game.managers.collision_manager import CollisionManager
from utils import constants
from utils.hand_detection import HandDetector


class PositionManager(object):
    """
    Manages object positions and updates them.

    Constructor Parameters:

    hand_detector: HandDetector
        HandDetector instance used by game

    paddle: Paddle
        Paddle instance used by game

    ball: Ball
        Ball instance used by game

    borders: Borders
        Borders instance used by game

    collision_manager: CollisionManager
        CollisionManager instance used by game
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

    def update(self, should_update_ball: bool =True):
        """
        updates game object positions
        """
        self._update_paddle_position()
        self._update_embryo_position(should_update_ball)
        self._detect_collisions(should_update_ball)
    
    def is_ball_gone(self):
        """
        returns true if ball position + radius (so it's visually completely
        off screen) is negative
        """
        if self.ball:
            return self.ball.x + self.ball.radius <= 0
        
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

    def _update_embryo_position(self, should_update_ball):
        """
        updates embryo position
        """
        if self.ball and should_update_ball:
            self.ball.x += self.ball.x_vel
            self.ball.y += self.ball.y_vel
