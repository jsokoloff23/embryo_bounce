import pygame

from game.assets.ball import Ball
from game.assets.paddle import Paddle
from game.assets.border import Border
from utils import constants

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

    def draw_text_box(self, surface: pygame.Surface, 
                      text: str, 
                      x: int = None,
                      y: int= None, 
                      font_size: int=constants.DEF_F_SIZE):
        """
        draws text box with given text at coordinate (x,y). If no x or no y
        is given, that coordinate is centered on the surface.

        parameters:

        surface: pygame.Surface
            surface for text box to be drawn on

        text: str
            text for text box

        x: int | None
            if x is int, x is the x coordinate. If x is None, x coordinate is
            centered.

        y: int | None
            if y is int, y is the x coordinate. If y is None, y coordinate is
            centered.

        font_size: int
            font size. Default is set by constants.DEF_F_SIZE.
        """
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, constants.BLACK)
        # Blit the text.
        size = surface.get_size()
        if x is None:
            x = size[0]/2 - text_surface.get_width()/2
        if y is None:
            y = size[0]/2 - text_surface.get_height()/2
        surface.blit(text_surface, (x, y))

    def draw_ball(cls, surface: pygame.Surface, ball: Ball):
        diameter = ball.radius*2
        image = ball.image
        image = pygame.transform.scale(image, (diameter, diameter))
        x, y = ball.get_coords()
        x = int(x - ball.radius)
        y = int(y - ball.radius)
        surface.blit(image, (x,y))
    