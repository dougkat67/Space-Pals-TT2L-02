import pygame

class Button4(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        image = pygame.image.load('images/gamebutton.png').convert_alpha()
        new_size = (200,160)
        self.image = pygame.transform.scale(image, new_size)
        self.rect = self.image.get_rect(center=(700,450))

    def update(self):
        pass

    def render(self, display):
        pass