import pygame
import sys
from level import Game

class Switch:
    def __init__(self):
        self.gameStateManager = GameStateManager('start')
        self.start = Start(self.gameStateManager)
        self.level = Level(self.gameStateManager)

        self.state = {'start': self.start, 'level': self.level}

    def run(self):
         while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
            self.state[self.gameStateManager.get_state()].run()
            pygame.display.update()

class Level:
    def __init__(self, gameStateManager):
        self.gameStateManager = gameStateManager
        self.game = Game()

    def run(self):
        self.game.run()

class Start:
    def __init__(self, gameStateManager):
        self.gameStateManager = gameStateManager
        self.screen = pygame.display.set_mode((1280, 720))  
        self.background_color = (0, 0, 255)  

    def run(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gameStateManager.set_state('level')

        self.screen.fill(self.background_color)
        pygame.display.flip()  

class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state
