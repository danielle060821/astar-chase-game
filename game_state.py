import pygame
from enum import Enum, auto

#used auto instead of numbers to avoid unexpected confusion since there are multiple classes.
#numbers are also useless in this case.
class Phase(Enum):
    INIT = auto()
    COUNTDOWN = auto()
    PLAYING = auto()
    FINISHED = auto()
class GameResult():
    NONE = auto()
    WIN = auto()
    LOSE = auto()
    
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
        