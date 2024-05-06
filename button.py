
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

import pygame 

class Button():
    def __init__(self, game):
        self.game = game
        image = pygame.image.load("WIP_art/start_button.png").convert_alpha()
        self.button = pygame.transform.scale(image,(300,200))
        self.rect = self.button.get_rect()
        self.rect.x, self.rect.y = 350, 270
        self.click = False

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(self.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

    def render(self, display):
        display.blit(self.button, (350,270))

