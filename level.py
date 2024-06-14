import pygame
import sys
import os
import json
from math import floor
from alien import Alien
from button import Button1
from button2 import Button2
from button3 import Button3
from button4 import Button4
from setting import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import UI
from states.state import State
# from leaderboard import ButtonGame


class Pet(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.visible_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)

        self.background = pygame.image.load('background.png').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.monster = Alien((400, 350))
        self.button1 = Button1((110, 350), self.visible_sprites)
        self.button2 = Button2((110, 350), self.visible_sprites)
        self.button3 = Button3((110, 350), self.visible_sprites)
        self.button4 = Button4((110, 350), self.visible_sprites)

        self.ui = UI()
        self.last_button_click_time = pygame.time.get_ticks()

        self.current_scene = "game"
        self.leaderboard = []
        self.start_time = pygame.time.get_ticks()
        self.screen_width = SCREEN_WIDTH

        self.elapsed_time = 0

        # Day
        self.day = 1

        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as file:
                self.leaderboard = json.load(file)

    def handle_events(self, events):
        pass

    def update(self, deltatime, actions):
        self.monster.update()
        current_time = pygame.time.get_ticks()
        self.elapsed_time = (current_time - self.start_time) // 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.button1.rect.collidepoint(event.pos):
                    self.monster.monster_select = 2 if self.monster.monster_select < 5 else 6 if  self.monster.monster_select < 9 else 10
                    self.last_button_click_time = current_time
                    self.ui.feeding = min(self.ui.feeding + 10, self.ui.stats['feeding'])

                elif self.button2.rect.collidepoint(event.pos):
                    self.monster.monster_select = 3 if self.monster.monster_select < 5 else 7 if  self.monster.monster_select < 9 else 11
                    self.last_button_click_time = current_time
                    self.ui.cleanliness = min(self.ui.cleanliness + 10, self.ui.stats['cleanliness'])

                elif self.button3.rect.collidepoint(event.pos):
                    self.monster.monster_select = 4 if self.monster.monster_select < 5 else 8 if  self.monster.monster_select < 9 else 12
                    self.last_button_click_time = current_time
                    self.ui.happy = min(self.ui.happy + 10, self.ui.stats['happiness'])

        if all([self.ui.feeding >= self.ui.stats['feeding'], # Day 2
                self.ui.cleanliness >= self.ui.stats['cleanliness'],
                self.ui.happy >= self.ui.stats['happiness']]) and self.day == 1  :
            self.ui.reset_stats()
            self.monster.monster_select = 5 
            self.day += 1
            
            
        elif all([self.ui.feeding >= self.ui.stats['feeding'], # Day 3
                self.ui.cleanliness >= self.ui.stats['cleanliness'],
                self.ui.happy >= self.ui.stats['happiness']]) and self.day == 2  :
            self.ui.reset_stats()
            self.monster.monster_select = 9 
            self.day += 1

        if self.monster.monster_select in [2, 3, 4] and current_time - self.last_button_click_time >= 3000:
            self.monster.monster_select = 1
        elif self.monster.monster_select in [6, 7, 8] and current_time - self.last_button_click_time >= 3000:
            self.monster.monster_select = 5
        elif self.monster.monster_select in [10, 11, 12] and current_time - self.last_button_click_time >= 3000:
            self.monster.monster_select = 9

    
    def render(self, display, font):
        # Render the current game state
        display.blit(self.background, (0, 0))
        self.monster.render(display)
        self.visible_sprites.draw(display)
        self.ui.display(display)

        if self.current_scene == "game":
            self.render_game_timer(display)
        elif self.current_scene == "leaderboard":
            self.render_leaderboard(display)

    def render_game_timer(self, display):
        time_surface = self.font.render(f"Time: {self.elapsed_time} seconds", True, (0, 0, 0))
        time_rect = time_surface.get_rect(topright=(self.screen_width - 20, 20))
        display.blit(time_surface, time_rect)

    def run(self):
        self.update()

