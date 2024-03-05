"""
constants used throughout the program
"""

import os
import sys

#game surface size
GAME_X_SIZE = 800
GAME_Y_SIZE = 600
#scaling for hand position so entire webcam field of view isn't used
HAND_POSITION_SCALING = 1.8
#offset to correct scaling
HAND_COORDS_OFFSET = -220
#camera feed height in game
CAM_H = 120
#speed increase increment
SPEED_INCREMENT = 3
#character limit for high score name
NAME_CHARACTER_LIMIT = 12
#object coords and sizes
DEF_F_SIZE = 60
NEW_HS_Y = 250
HS_ENTRY_Y = 350
PLAY_AGAIN_Y = 250
PLAY_RESP_Y = 350
MENU_BOX_X = 250
MENU_BOX_Y_DEF = 460
MENU_BOX_Y_INCR = 75
MENU_BOX_W = 310
MENU_BOX_H = 75
MENU_BOX_BORDER_W = 8
GAME_UI_F_SIZE = 36
SCORE_BOX_X = 600
SCORE_BOX_Y = int(CAM_H/2)
LIVES_TEXT_X = 380
LIVES_TEXT_Y = 10
LIVES_IMAGE_X = 500
LIVES_IMAGE_X_INCR = 90
LIVES_IMAGE_Y = 40
HS_TITLE_Y = 20
HS_ESC_X = 20
HS_ESC_Y = 670
HS_NAME_X = 200
HS_Y = 100
HS_Y_INCR = 100
HS_SCORE_X = 500
#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (187, 244, 247)
#CWD is initialized on app start
CWD = os.path.dirname(sys.argv[0])
FISH_IMAGE_PATH = f"{CWD}/game/assets/images/zebrafish.png"
EMBRYO_IMAGE_PATH = f"{CWD}/game/assets/images/embryo.png"
BG_IMAGE_PATH = f"{CWD}/game/assets/images/background.jpg"
MENU_IMAGE_PATH = f"{CWD}/game/assets/images/menu.png"
GAME_SONG_PATH = f"{CWD}/game/assets/sounds/game_song.mp3"
MENU_SONG_PATH = f"{CWD}/game/assets/sounds/menu_song.mp3"
MISTAKE_SOUND_PATH = f"{CWD}/game/assets/sounds/mistake_sound.mp3"
PADDLE_SOUND_PATH = f"{CWD}/game/assets/sounds/paddle_sound.mp3"
HAND_MODEL_PATH = f"{CWD}/utils/hand_landmarker.task"
HS_CFG_PATH = f"{CWD}/highscores.cfg"
