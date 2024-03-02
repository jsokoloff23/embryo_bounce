import pygame

from game.assets.ball import Ball, Ball
from game.assets.paddle import Paddle

class DrawManager(object):
    IMAGE_ANGLE = -90
    def draw_paddle(self, surface: pygame.Surface, paddle: Paddle):
        width = paddle.width
        height = paddle.height
        image = paddle.image
        image = pygame.transform.scale(paddle.image, (height, width))
        image = pygame.transform.rotate(image, DrawManager.IMAGE_ANGLE)
        surface.blit(image, paddle.get_coords())

    def draw_ball(cls, surface: pygame.Surface, ball: Ball):
        diameter = ball.radius*2
        image = ball.image
        image = pygame.transform.scale(image, (diameter, diameter))
        x, y = ball.get_coords()
        x = int(x - ball.radius)
        y = int(y - ball.radius)
        surface.blit(image, (x,y))
    