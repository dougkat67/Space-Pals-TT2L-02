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


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pet Game')
        self.clock = pygame.time.Clock()
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

        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as file:
                self.leaderboard = json.load(file)

    def update(self):
        while True:
            current_time = pygame.time.get_ticks()
            self.elapsed_time = (current_time - self.start_time) // 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    if self.button1.rect.collidepoint(event.pos):
                        self.monster.monster_select = 2
                        self.last_button_click_time = current_time
                        if self.ui.feeding >= self.ui.stats['feeding']:
                            self.ui.feeding = self.ui.stats['feeding']
                        else:
                            self.ui.feeding += 10
                    elif self.button2.rect.collidepoint(event.pos):
                        self.monster.monster_select = 3
                        self.last_button_click_time = current_time
                        if self.ui.cleanliness >= self.ui.stats['cleanliness']:
                            self.ui.cleanliness = self.ui.stats['cleanliness']
                        else :
                            self.ui.cleanliness += 10
                    elif self.button3.rect.collidepoint(event.pos):
                        self.monster.monster_select = 4
                        self.last_button_click_time = current_time
                        if self.ui.happy >= self.ui.stats['happiness']:
                            self.ui.happy = self.ui.stats['happiness']
                        else :
                            self.ui.happy += 10

            self.screen.blit(self.background, (0, 0))
            self.monster.update(self.screen)
            self.visible_sprites.draw(self.screen)

            self.ui.display()

            if self.monster.monster_select == 2 and current_time - self.last_button_click_time >= 3000:
                self.monster.monster_select = 1
            if self.monster.monster_select == 3 and current_time - self.last_button_click_time >= 3000:
                self.monster.monster_select = 1
            if self.monster.monster_select == 4 and current_time - self.last_button_click_time >= 3000:
                self.monster.monster_select = 1

            if self.current_scene == "game":
                self.render_game_timer()
            elif self.current_scene == "leaderboard":
                self.render_leaderboard()

            pygame.display.flip()
            self.clock.tick(60)

    def render_game_timer(self):
        time_surface = self.font.render(f"Time: {self.elapsed_time} seconds", True, (0, 0, 0))
        time_rect = time_surface.get_rect(topright=(self.screen_width - 20, 20))
        self.screen.blit(time_surface, time_rect)

    def render_leaderboard(self):
        text_y = 100
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x["time"])
        for entry in sorted_leaderboard:
            text_surface = self.font.render(f"{entry['time']} seconds", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, text_y))
            self.screen.blit(text_surface, text_rect)
            text_y += 50

    def save_leaderboard(self):
        with open("leaderboard.json", "w") as file:
            json.dump(self.leaderboard, file)

    def run(self):
        self.update()

if __name__ == "__main__":
    game = Game()
    game.run()