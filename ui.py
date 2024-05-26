import pygame
from setting import *
from alien import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.satiety_bar_rect = pygame.Rect(10, 10, FEEDING_BAR_WIDTH, BAR_HEIGHT)
        self.happy_bar_rect = pygame.Rect(10, 34, HAPPINESS_BAR_WIDTH, BAR_HEIGHT)
        self.clear_bar_rect = pygame.Rect(10, 54, HAPPINESS_BAR_WIDTH, BAR_HEIGHT)

        # stats
        self.stats = {'happiness': 100, 'cleanliness': 100, 'feeding': 100}
        self.happy = self.stats['happiness'] * 0.0
        self.cleanliness = self.stats['cleanliness'] * 0.1
        self.feeding = self.stats['feeding'] * 0.0

        self.coin = 5000

    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_coin(self,exp):
        text_surf = self.font.render(str(int(exp)),False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright = (x,y))
        
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,text_rect.inflate(20,20),3)

    def display(self):
        self.show_bar(self.feeding, self.stats['feeding'], self.satiety_bar_rect, SATIETY_COLOR)
        self.show_bar(self.happy, self.stats['happiness'], self.happy_bar_rect, HAPPY_COLOR)
        self.show_bar(self.cleanliness, self.stats['cleanliness'], self.clear_bar_rect, CLEAR_COLOR)

        self.show_coin(self.coin)
        
    



    def update(self, deltatime, player_action):
        pass

    def render(self, display):
        pass

    def reset_stats(self):
        self.happy = 0