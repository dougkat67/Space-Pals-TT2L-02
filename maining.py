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

    def run(self):
        self.game.run()

if __name__ == "__main__":
    game = Play()
    game.run()
