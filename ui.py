import pygame
from setting import *

class UI:
    def __init__(self):
        
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT , UI_FONT_SIZE)

        # bar setup
        self.satiety_bar_rect = pygame.Rect(10,10,FEEDING_BAR_WIDTH, BAR_HEIGHT)
        self.happy_bar_rect = pygame.Rect(10,34,HAPPINESS_BAR_WIDTH ,BAR_HEIGHT)
    def display(self):
        pygame.draw.rect(self.display_surface, 'black',self.satiety_bar_rect)
        