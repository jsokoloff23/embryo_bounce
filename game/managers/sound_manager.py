import pygame

class SoundManager(object):
    def __init__(self):
        self.paddle_sound = pygame.mixer.Sound("game/assets/sounds/paddle_sound.mpy")
        self.mistake_sound = pygame.mixer.Sound("game/assets/sounds/mistake_sound.mpy")

    def play_paddle_sound(self):
        self.paddle_sound.play()

    def play_mistake_sound(self):
        self.mistake_sound.play()
        