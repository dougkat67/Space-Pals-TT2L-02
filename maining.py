import pygame
import sys
from setting import SCREEN_WIDTH, SCREEN_HEIGHT
from switchscreen import Switch

class Play:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pet Game')
        self.clock = pygame.time.Clock()

        self.switch = Switch()

    def run(self):
        while True:
            self.switch.run()


if __name__ == "__main__":
    game = Play()
    game.run()