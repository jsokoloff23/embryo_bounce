"""
This module contains the class CollisionManager which manages object
collisions
"""

import numpy as np

from game.assets.ball import Ball
from game.assets.border import Borders
from game.assets.paddle import Paddle
from game.managers.sound_manager import SoundManager


class CollisionManager(object):
    """
    Manages collision of objects.
    """
    #angle range of ball-paddle collision
    ANGLE_RANGE = np.pi/2
    #min angle from ball-paddle-collision
    MIN_ANGLE = -ANGLE_RANGE/2
    #max angle from ball-paddle-collision
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
        """
        called when ball-top border collision occurs
        """
        #on top and bottom border collision, only vertical velocity changes.
        self.ball.y_vel = -self.ball.y_vel

    def back_border_collision(self):
        """
        called when ball-back border collision occurs
        """
        #on back border, only horizantal velocity changes.
        self.ball.x_vel = -self.ball.x_vel

    def bottom_border_collision(self):
        """
        called when ball-bottom border collision occurs
        """
        self.ball.y_vel = -self.ball.y_vel

    def paddle_collision(self):
        """
        called when ball-paddle collision occurs
        """
        #center right coordinate of paddle
        cent_coords = self.paddle.cent_coords
        #difference between center coord y and ball y positions
        dy = cent_coords[1] - self.ball.y
        #angle factor taken as ratio of dy and paddle height
        angle_fact = dy/self.paddle.height
        #angle factor multiplied by ANGLE_RANGE to get angle change
        angle = angle_fact*CollisionManager.ANGLE_RANGE
        #ensures angle is within accetable range
        angle = self._get_corrected_angle(angle)
        #velocities are changed byased on angle
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
        