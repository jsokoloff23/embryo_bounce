"""
This module contains the DrawManager class, a static class that
draws objects on pygame surfaces
"""

import pygame

from game.assets.ball import Ball
from game.assets.paddle import Paddle
from game.assets.border import Border
from utils import constants

class DrawManager(object):
    """
    Manages drawing objects and pygame surfaces on other pygame surfaces
    """
    #angle needed to rotate imported images
    IMAGE_ANGLE = -90
    
    @classmethod
    def draw_border(cls, surface: pygame.Surface, border: Border):
        """
        Draws border object on surface

        Parameters:

        surface: pygame.Surface
            pygame surface to be drawn on

        border: Border
            Border object to be drawn
        """
        color = border.color
        width = border.width
        height = border.height
        x = border.x
        y = border.y
        cls.draw_rectangle(surface, color, x, y, width, height)

    @classmethod
    def draw_rectangle(cls, 
                       surface: pygame.Surface,
                       color: tuple[int, int, int],
                       x: int,
                       y: int,
                       width: int,
                       height: int ,
                       border_w: int = 0):
        """
        Draws rectangle with given parameters

        Parameters:

        surface: pygame.Surface
            pygame surface to be drawn on

        color: tuple[int, int, int]
            color tuple in RGB

        x: int
            x position in pixels

        y: int
            y position in pixels

        width: int
            width in pixels

        height: int
            height in pixels

        border_w: int = 0
            width of rectangle border. If border_w > 0, rectangle is
            empty with border width border_w.
        """
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, color, rect, width=border_w)

    @classmethod
    def draw_paddle(cls, surface: pygame.Surface, paddle: Paddle):
        """
        Draws paddle object on surface

        Parameters:

        surface: pygame.Surface
            pygame surface to be drawn on

        paddle: Paddle
            Paddle object to be drawn
        """
        width = paddle.width
        height = paddle.height
        image = paddle.image
        image = pygame.transform.scale(paddle.image, (height, width))
        image = pygame.transform.rotate(image, cls.IMAGE_ANGLE)
        surface.blit(image, paddle.get_coords())

    @classmethod
    def draw_ball(cls, surface: pygame.Surface, ball: Ball):
        """
        Draws ball object on surface

        Parameters:

        surface: pygame.Surface
            pygame surface to be drawn on

        ball: Ball
            Ball object to be drawn
        """
        diameter = ball.radius*2
        image = ball.image
        image = pygame.transform.scale(image, (diameter, diameter))
        x, y = ball.get_coords()
        x = int(x - ball.radius)
        y = int(y - ball.radius)
        surface.blit(image, (x,y))
    
    @classmethod
    def draw_text_box(cls, surface: pygame.Surface, 
                      text: str, 
                      x: int = None,
                      y: int= None, 
                      font_size: int=constants.DEF_F_SIZE):
        """
        draws text box with given text at coordinate (x,y). If no x or no y
        is given, that coordinate is centered on the surface.

        parameters:

        surface: pygame.Surface
            pygame surface to draw on

        text: str
            text for text box

        x: int | None
            if x is int, x is the x position in pixels. If x is None, x 
            coordinate is centered.

        y: int | None
            if y is int, y is the y position in pixels. If y is None, 
            y coordinate is centered.

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

    @classmethod
    def draw_lives(cls, surface: pygame.Surface, paddle: Paddle, lives: int):
        """
        Draws paddle object lives times to indicate number of lives remaining.

        Parameters:

        surface: pygame.Surface
            pygame surface to draw on

        paddle: Paddle
            paddle object used in game

        lives: int
            number of lives remaining
        """
        width = paddle.width
        height = paddle.height
        image = paddle.image
        image = pygame.transform.scale(paddle.image, (height, width))
        image = pygame.transform.rotate(image, cls.IMAGE_ANGLE)
        for life in range(lives-1):
            x = constants.LIVES_IMAGE_X-life*constants.LIVES_IMAGE_X_INCR
            y = constants.LIVES_IMAGE_Y
            surface.blit(image, (x, y))
    