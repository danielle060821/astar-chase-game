import pygame
import os
#background music
def play_music(music_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #only initiate once
    if not pygame.mixer.get_init:
        pygame.mixer.pre_init(44100, -16, 2, 2048)  # 44.1kHz, 16-bit, stereo, buffer 512
        pygame.mixer.init()
        
    pygame.mixer.music.load(os.path.join(BASE_DIR, music_path))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)