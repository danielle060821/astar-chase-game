import pygame
from enum import Enum

class Phase(Enum):
    INIT = 0
    COUNTDOWN = 1
    PLAYING = 2
    FINISHED = 3

class GameState:
    def __init__(self):
        self.running = True
        self.phase = Phase.INIT
        self.phase_start_time = pygame.time.get_ticks()
        self.result = None
        self.finish_time = None
        
    def set_phase(self, new_phase):
        self.phase = new_phase
        self.phase_start_time = pygame.time.get_ticks()
        