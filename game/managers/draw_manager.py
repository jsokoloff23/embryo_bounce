import pygame

from game.assets.ball import Ball
from game.assets.paddle import Paddle
from game.assets.border import Border

class DrawManager(object):
    IMAGE_ANGLE = -90

    def draw_border(self, surface: pygame.Surface, border: Border):
        color = border.color
        width = border.width
        height = border.height
        x = border.x
        y = border.y
        self.draw_rectangle(surface, color, x, y, width, height)

    def draw_rectangle(self, surface: pygame.Surface, color, x, y, width, height , border_w=0):
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, color, rect, width=border_w)

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
    