import numpy as np

from game.assets.ball import Ball
from game.assets.border import Borders
from game.assets.paddle import Paddle
from game.managers.sound_manager import SoundManager

class CollisionManager(object):
    ANGLE_RANGE = np.pi/2
    MIN_ANGLE = -ANGLE_RANGE/2
    MAX_ANGLE = ANGLE_RANGE/2
    def __init__(self, 
                 ball: Ball, 
                 fish_paddle: Paddle, 
                 borders: Borders,
                 sound_manager: SoundManager):
        self.ball = ball
        self.paddle = fish_paddle
        self.borders = borders
        self.sound_manager = sound_manager

    def top_border_collision(self):
        self.ball.y_vel = -self.ball.y_vel

    def back_border_collision(self):
        self.ball.x_vel = -self.ball.x_vel

    def bottom_border_collision(self):
        self.ball.y_vel = -self.ball.y_vel

    def paddle_collision(self):
        cent_coords = self.paddle.cent_coords
        dy = cent_coords[1] - self.ball.y
        angle_fact = dy/self.paddle.height
        angle = angle_fact*CollisionManager.ANGLE_RANGE
        angle = self._get_corrected_angle(angle)
        self.ball.x_vel = self.ball.speed*np.cos(angle)
        self.ball.y_vel = -self.ball.speed*np.sin(angle)
        self.sound_manager.play_paddle_sound()

    def _get_corrected_angle(self, angle):
        """
        makes sure angle is within range (MIN_ANGLE, MAX_ANGLE)
        """
        if angle <= CollisionManager.MIN_ANGLE:
            return CollisionManager.MIN_ANGLE
        elif angle >= CollisionManager.MAX_ANGLE:
            return CollisionManager.MAX_ANGLE
        else:
            return angle
        