import cv2
import numpy as np
import pygame

from game.managers.draw_manager import DrawManager
from game.assets.paddle import Paddle
from game.assets.ball import Ball
from game.assets.border import Borders
from utils.hand_detection import HandDetector
from utils.camera import HandCam
from utils import constants


class DisplayManager():
    def __init__(self, 
                 hand_detector: HandDetector,
                 hand_cam: HandCam,
                 paddle: Paddle, 
                 ball: Ball,
                 borders: Borders):
        self.hand_detector = hand_detector
        self.hand_cam = hand_cam
        self.paddle = paddle
        self.ball = ball
        self.borders = borders
        self.size = (800, 720)
        self.cam_size = self._init_cam_size()
        self.cam_coords = (0, 0)
        self.bg_coords = (0, 0)
        self.bg_size = (800, 600)
        self.game_coords = (0, self.cam_size[1])
        self.display = pygame.display.set_mode(self.size)
        #init copies so we only have to load them once
        self.bg_surface_copy = self._init_bg_surface_copy()
        self.game_surface_copy = self._init_game_surface_copy()
        self.menu_surface_copy = self._init_menu_surface_copy()

    def game_update(self, lives, score):
        self._set_cam_surface()
        self._draw_game(lives, score)
        self._blit_bg_surface()
        self._blit_cam_surface()
        self._blit_game_surface()
        pygame.display.update()

    def high_score_entry_update(self, name):
        self._set_cam_surface()
        self._draw_high_score_entry(name)
        self._blit_bg_surface()
        self._blit_cam_surface()
        self._blit_game_surface()
        pygame.display.update()

    def play_again_update(self, response):
        self._set_cam_surface()
        self._draw_play_again(response)
        self._blit_bg_surface()
        self._blit_cam_surface()
        self._blit_game_surface()
        pygame.display.update()

    def menu_update(self, button_num):
        self._draw_menu(button_num)
        self._blit_menu_surface()
        pygame.display.update()

    def _init_cam_size(self):
        aspect_ratio = self.hand_cam.aspect_ratio
        return (int(constants.CAM_H*aspect_ratio), constants.CAM_H)

    def _set_cam_surface(self):
        if self.hand_detector.image is not None:
            frame = self.hand_detector.image
            #resize webcam image to standardized size
            frame = cv2.resize(frame, self.cam_size)
            #frame requires rotation to match pygame orientation
            frame = np.rot90(frame)
            #cv2 cap uses BGR instead of RGB, but pygame uses RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.cam_surface = pygame.surfarray.make_surface(frame)
        else:
            #Only occurs before webcam stream initializes
            #3 for number of color channels
            shape = (self.cam_size[0], self.cam_size[1], 3)
            frame = np.ones(shape)*constants.WHITE
            self.cam_surface = pygame.surfarray.make_surface(frame)

    def _blit_bg_surface(self):
        self.display.blit(self.bg_surface, self.bg_coords)

    def _blit_cam_surface(self):
        self.display.blit(self.cam_surface, self.cam_coords)
    
    def _blit_game_surface(self):
        self.display.blit(self.game_surface, self.game_coords)

    def _blit_menu_surface(self):
        self.display.blit(self.menu_surface, self.bg_coords)

    #TODO all of these draw events should probably go to the draw manager
    def _draw_menu(self, button_num):
        #copy so we don't have to load image in each time
        self.menu_surface = self.menu_surface_copy.copy()
        DrawManager.draw_rectangle(surface=self.menu_surface, 
                                   color=constants.GREEN, 
                                   x=constants.MENU_BOX_X, 
                                   y=constants.MENU_BOX_Y_DEF+constants.MENU_BOX_Y_INCR*button_num, 
                                   width=constants.MENU_BOX_W, 
                                   height=constants.MENU_BOX_H, 
                                   border_w=constants.MENU_BOX_BORDER_W)
        
    def _draw_game(self, score, lives):
        self.game_surface = self.game_surface_copy.copy()
        self.bg_surface = self.bg_surface_copy.copy()
        DrawManager.draw_border(self.game_surface, self.borders.top)
        DrawManager.draw_border(self.game_surface, self.borders.back)
        DrawManager.draw_border(self.game_surface, self.borders.bot)
        if self.ball:
            DrawManager.draw_ball(self.bg_surface_copy, self.ball)
        DrawManager.draw_paddle(self.bg_surface, self.paddle)
        DrawManager.draw_lives(self.bg_surface, self.paddle, lives)
        DrawManager.draw_text_box(surface=self.bg_surface, 
                                  text=f"Score: {score}", 
                                  x=constants.SCORE_BOX_X, 
                                  y=constants.SCORE_BOX_Y, 
                                  font_size=constants.GAME_UI_F_SIZE)
        DrawManager.draw_text_box(surface=self.bg_surface, 
                                  text=f"Lives", 
                                  x=constants.LIVES_TEXT_X, 
                                  y=constants.LIVES_TEXT_Y, 
                                  font_size=constants.GAME_UI_F_SIZE)

    def _draw_high_score_entry(self, name):
        self.game_surface = self.game_surface_copy.copy()
        DrawManager.draw_text_box(
            self.game_surface, "New High Score!", y=constants.NEW_HS_Y)
        DrawManager.draw_text_box(
            self.game_surface, f"Enter Name: {name}", y=constants.HS_ENTRY_Y)
        
    def _draw_play_again(self, response):
        self.game_surface = self.game_surface_copy.copy()
        DrawManager.draw_text_box(
            self.game_surface, "Play again?", y=constants.PLAY_AGAIN_Y)
        DrawManager.draw_text_box(
            self.game_surface, f"Type y or n: {response}", y=constants.PLAY_RESP_Y)

    def _init_bg_surface_copy(self):
        #3 for number of color channels
        bg_shape = (self.size[0], self.size[1], 3)
        bg_array = np.ones(bg_shape)*constants.LIGHT_BLUE
        return pygame.surfarray.make_surface(bg_array)

    def _init_game_surface_copy(self):
        game_surface = pygame.image.load(constants.BG_IMAGE_PATH)
        return pygame.transform.scale(game_surface, self.bg_size)
    
    def _init_menu_surface_copy(self):
        menu_surface =  pygame.image.load(constants.MENU_IMAGE_PATH)
        return pygame.transform.scale(menu_surface, self.size)
    