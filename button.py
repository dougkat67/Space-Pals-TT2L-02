import pygame

class Button1(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/feedingbutton.png').convert_alpha()

        self.rect = self.image.get_rect(center=(100,450))
        


class Button3(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        self.playing = pygame.image.load('images/playing.png').convert_alpha()
        self.rect = self.playing.get_rect(center=(300,300))
