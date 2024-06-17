import pygame
import sys
import os
import json
from math import floor
from alien import Alien
from button import Button1
from button2 import Button2
from button3 import Button3
from setting import SCREEN_WIDTH, SCREEN_HEIGHT
from ui import UI
from setting import *
from states.state import State
from button5 import Button5
from data import Data


class Pet(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.visible_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)


        # Background
        self.background = pygame.image.load('background.png').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Leaderboard background
        self.leaderboard_background = pygame.image.load('leaderboard.jpg').convert()
        self.leaderboard_background = pygame.transform.scale(self.leaderboard_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.last_button_click_time = pygame.time.get_ticks()
        self.current_scene = "game"
        self.leaderboard = []
        self.start_time = pygame.time.get_ticks()
        self.screen_width = SCREEN_WIDTH
        
        self.elapsed_time = 0
        self.time_recorded = False

        # Ending images
        self.happy_ending_images = [pygame.image.load(f'images/happy_ending/happy{i}.png').convert() for i in range(5)]
        self.bad_ending_images = [pygame.image.load(f'images/bad_ending/bad{i}.png').convert() for i in range(5)]
        self.current_image_index = 0
        self.ending_type = None

        self.load_user_text()

        # File load

        self.monster = Alien((400, 350))
        self.button1 = Button1((110, 350), self.visible_sprites)
        self.button2 = Button2((110, 350), self.visible_sprites)
        self.button3 = Button3((110, 350), self.visible_sprites)
        self.button5 = Button5((55, 175), self.visible_sprites)
        
        self.data = Data((0, 0), self.visible_sprites)  

        self.ui = UI()

        # Sound 
        main_sound = pygame.mixer.Sound('audio/song.mp3')
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

        self.elapsed_time = 0

        self.click = False
        self.eat = False
        self.bath = False
        self.entertain = False

        # Day


        self.day = 1
        self.last_button_click_time = pygame.time.get_ticks()
        self.current_scene = "game"
        self.start_time = pygame.time.get_ticks()

        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as file:
                self.leaderboard = json.load(file)
        
        with open('combined_data.json', 'r') as file:
            self.combined_data = json.load(file)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not self.time_recorded:
                    self.record_time()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # click to next image at ending
                if self.current_scene in ["happy_ending", "bad_ending"]:
                    self.current_image_index += 1
                    if self.current_scene == "happy_ending" and self.current_image_index >= len(self.happy_ending_images):
                        self.enter_leaderboard()
                    elif self.current_scene == "bad_ending" and self.current_image_index >= len(self.bad_ending_images):
                        self.enter_leaderboard()
                elif self.button1.rect.collidepoint(event.pos): 
                    self.handle_button1_click()
                elif self.button2.rect.collidepoint(event.pos):  
                    self.handle_button2_click()
                elif self.button3.rect.collidepoint(event.pos):  
                    self.handle_button3_click()
                elif self.button5.rect.collidepoint(event.pos):  
                    self.current_scene = "bad_ending"
                


        current_time = pygame.time.get_ticks()
        self.elapsed_time = (current_time - self.start_time) / 1000
        if self.elapsed_time > 50 and not self.time_recorded:  # Trigger happy ending
            self.current_scene = "happy_ending"
            self.record_time()

        if self.monster.monster_select in [2, 3, 4] and current_time - self.last_button_click_time >= 3000:
            self.monster.monster_select = 1
        if self.monster.monster_select in [6, 7, 8] and current_time - self.last_button_click_time >= 3000:
            self.monster.monster_select = 5
        if self.monster.monster_select in [10, 11, 12] and current_time - self.last_button_click_time >= 3000:
            self.monster.monster_select = 9
        if self.monster.monster_select in [14, 15, 16] and current_time - self.last_button_click_time >= 3000:
            self.monster.monster_select = 13
        if self.monster.monster_select in [18, 19, 20] and current_time - self.last_button_click_time >= 3000:
            self.monster.monster_select = 17
    
    def handle_button1_click(self):
        if self.ui.cleanliness >= 10 and self.ui.coin >= 1:
            self.monster.monster_select = 2 if self.monster.monster_select < 5 else 6 if self.monster.monster_select < 9 else 10 if self.monster.monster_select < 13 else 14 if self.monster.monster_select < 17 else 18
            self.last_button_click_time = pygame.time.get_ticks()
            self.ui.feeding = min(self.ui.feeding + 20, self.ui.stats['feeding'])
            self.ui.cleanliness = min(self.ui.cleanliness - 10, self.ui.stats['cleanliness'])
            self.ui.happy = min(self.ui.happy + 5, self.ui.stats['happiness'])

            main_sound = pygame.mixer.Sound('audio/button.mp3')
            main_sound.set_volume(0.5)
            main_sound.play(loops=0)

            second_sound = pygame.mixer.Sound('audio/eat.mp3')
            second_sound.set_volume(0.5)
            second_sound.play(loops=0)

            self.ui.coin -= 1
            self.ui.save_collected_coins()

    def handle_button2_click(self):
        if self.ui.feeding >= 10 and self.ui.coin >= 1:
            self.monster.monster_select = 3 if self.monster.monster_select < 5 else 7 if self.monster.monster_select < 9 else 11 if self.monster.monster_select < 13 else 15 if self.monster.monster_select < 17 else 19
            self.last_button_click_time = pygame.time.get_ticks()
            self.ui.feeding = min(self.ui.feeding - 10, self.ui.stats['feeding'])
            self.ui.cleanliness = min(self.ui.cleanliness + 20, self.ui.stats['cleanliness'])
            self.ui.happy = min(self.ui.happy + 5, self.ui.stats['happiness'])

            main_sound = pygame.mixer.Sound('audio/button.mp3')
            main_sound.set_volume(0.5)
            main_sound.play(loops=0)

            second_sound = pygame.mixer.Sound('audio/wash.mp3')
            second_sound.set_volume(0.5)
            second_sound.play(loops=0)

            self.ui.coin -= 1
            self.ui.save_collected_coins()

    def handle_button3_click(self):
        if self.ui.feeding >= 20 and self.ui.coin >= 1:
            self.monster.monster_select = 4 if self.monster.monster_select < 5 else 8 if self.monster.monster_select < 9 else 12 if self.monster.monster_select < 13 else 16 if self.monster.monster_select < 17 else 20
            self.ui.feeding = min(self.ui.feeding - 20, self.ui.stats['feeding'])
            self.ui.cleanliness = min(self.ui.cleanliness + 5, self.ui.stats['cleanliness'])
            self.ui.happy = min(self.ui.happy + 15, self.ui.stats['happiness'])

            main_sound = pygame.mixer.Sound('audio/button.mp3')
            main_sound.set_volume(0.5)
            main_sound.play(loops=0)

            self.ui.coin -= 1
            self.ui.save_collected_coins()
    def load_user_text(self):
        try:
            with open('user_text.json', 'r') as file:
                data = json.load(file)
                self.user_text = data.get("user_text", "")
        except FileNotFoundError:
            self.user_text = ""

    def reset_user_text(self):
        self.user_text = ""
        with open('user_text.json', 'w') as file:
            json.dump({"user_text": self.user_text}, file)


    def update(self,deltatime,actions):
            self.monster.update()
            current_time = pygame.time.get_ticks() # get current time
            self.elapsed_time = (current_time - self.start_time) // 1000 # get elapsed time in seconds


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                    

            # Alien grow

            if all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 1  : # Day2
                self.ui.reset_stats() # Reset stats
                self.monster.monster_select = 5 
                self.day += 1
                print(self.day)
                main_sound = pygame.mixer.Sound('audio/Upgrade.mp3')   #sound
                main_sound.set_volume(1)
                main_sound.play(loops = 0)
                
                
            elif all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 2  : # Day3
                self.ui.reset_stats()
                self.monster.monster_select = 9 
                self.day += 1
                print(self.day)
                main_sound = pygame.mixer.Sound('audio/Upgrade.mp3')
                main_sound.set_volume(1)
                main_sound.play(loops = 0)

            elif all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 3  : # Day4
                self.ui.reset_stats()
                self.monster.monster_select = 13 
                self.day += 1
                print(self.day)
                main_sound = pygame.mixer.Sound('audio/Upgrade.mp3')
                main_sound.set_volume(1)
                main_sound.play(loops = 0)

            elif all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 4  : # Day5
                
                self.monster.monster_select = 17 
                self.day += 1
                print(self.day)
                main_sound = pygame.mixer.Sound('audio/Upgrade.mp3')
                main_sound.set_volume(1)
                main_sound.play(loops = 0)


    def render(self, display, font):
        if self.current_scene == "game":
            display.blit(self.background, (0, 0))
            self.monster.render(display)
            self.visible_sprites.draw(display)
            self.ui.display(display)
            self.render_game_timer(display)
            self.render_game_level(display)
        elif self.current_scene == "leaderboard": # switch to leaderboard
            self.render_leaderboard(display)

        elif self.current_scene == "happy_ending":
            if self.current_image_index < len(self.happy_ending_images):
                display.blit(self.happy_ending_images[self.current_image_index], (0, 0))
            else:
                self.enter_leaderboard()
        elif self.current_scene == "bad_ending":
            if self.current_image_index < len(self.bad_ending_images):
                display.blit(self.bad_ending_images[self.current_image_index], (0, 0))
            else:
                self.enter_leaderboard()
 
    def render_game_timer(self, display): # display seconds
        time_surface = self.font.render(f"Time: {int(self.elapsed_time)} seconds", True, (0, 0, 0))
        time_rect = time_surface.get_rect(topright=(self.screen_width - 20, 20))

        display.blit(time_surface, time_rect)

    def render_game_level(self, display): # displat level
        level_surface = self.font.render(f"Level: {self.day}", True, (0, 0, 0))
        level_rect = level_surface.get_rect(topright=(self.screen_width - 450, 20))
        display.blit(level_surface, level_rect)

    def render_leaderboard(self, display):
        display.blit(self.leaderboard_background, (0, 0))
        text_y = 100
        sorted_leaderboard = sorted(self.combined_data.items(), key=lambda x: x[1])
        for user_text, time in sorted_leaderboard:
            rounded_time = int(time)  
            text_surface = self.font.render(f"{user_text}: {rounded_time} seconds", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, text_y))
            display.blit(text_surface, text_rect)
            text_y += 50

    def save_leaderboard(self):
        with open("leaderboard.json", "w") as file:
            json.dump(self.leaderboard, file)

    def record_time(self):
        self.elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        self.leaderboard.append({"time": self.elapsed_time})
        self.save_leaderboard()
        self.time_recorded = True

        # Update combined data after recording time
        self.data.update_combined_data() 
        self.combined_data = self.data.combined_data  

    def enter_leaderboard(self):
        if not self.time_recorded:
            self.record_time()
        self.current_scene = "leaderboard"

    def run(self):
        self.update()
