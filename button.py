
import pygame

class Button1(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/feedingbutton.png').convert_alpha()

        self.rect = self.image.get_rect(center=(100,450))

    def update(self, deltatime, player_action):
        pass

    def render(self, display):
        pass
        


