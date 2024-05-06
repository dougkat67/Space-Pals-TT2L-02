import pygame

class Screen1:
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('image1.png')
        self.image = pygame.transform.scale(self.image, (1000,500))

    def update(self):
        self.screen.blit(self.image,(0,0))
        pygame.display.flip()