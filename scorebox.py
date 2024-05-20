import pygame
from setting import *

class Scorebox :
    def __init__(self) :
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT , UI_FONT_SIZE)

    def render(self,screen):
        current_time = pygame.time.get_ticks()
        text_surf = self.font.render(str(int(current_time/1000)),False,TEXT_COLOR)
        screen.blit(text_surf,(900,10))

    