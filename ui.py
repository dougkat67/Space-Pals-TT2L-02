import pygame
from setting import *
from alien import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT , UI_FONT_SIZE)

        # bar setup
        self.satiety_bar_rect = pygame.Rect(10, 10, FEEDING_BAR_WIDTH, BAR_HEIGHT)
        self.happy_bar_rect = pygame.Rect(10, 34, HAPPINESS_BAR_WIDTH, BAR_HEIGHT)
        self.clear_bar_rect = pygame.Rect(10, 54, HAPPINESS_BAR_WIDTH, BAR_HEIGHT)

        # stats
        self.stats = {'happiness':100, 'clearness':100, 'satiety':100}
        self.happy = self.stats['happiness'] * 0.5
        self.clear = self.stats['clearness'] * 0.5
        self.satiety = self.stats['satiety'] * 0.5
    
    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
                
    def display(self, ): # display ui on screen
        self.show_bar(self.satiety, self.stats['satiety'], self.satiety_bar_rect, SATIETY_COLOR)
        self.show_bar(self.happy, self.stats['happiness'], self.happy_bar_rect, HAPPY_COLOR)
        self.show_bar(self.clear, self.stats['clearness'], self.clear_bar_rect, CLEAR_COLOR)
        