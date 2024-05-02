import pygame

class Button(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/feedingbutton.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)