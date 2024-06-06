import pygame
import sys
from setting import SCREEN_WIDTH, SCREEN_HEIGHT
from level import Game

class Play:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pet Game')
        self.clock = pygame.time.Clock()
        self.game = Game()

        # sound 
        main_sound = pygame.mixer.Sound('audio/song.mp3')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)
        

    def run(self):
        self.game.run()

if __name__ == "__main__":
    game = Play()
    game.run()
