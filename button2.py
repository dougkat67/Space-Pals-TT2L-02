import pygame

class Button2(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/drinkingbutton.png').convert_alpha()
        self.rect = self.image.get_rect(center=(300,450))
    
    def update(self, deltatime, player_action):
        pass

    def render(self, display):
        pass