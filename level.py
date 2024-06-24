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
from setting import *
from states.state import State
from level1 import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4
from level5 import Level5
from button5 import Button5
from data import Data

class Pet(State):
    def __init__(self, game):
        # general 
        super().__init__(game)
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.visible_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)

        # main game background
        self.background = pygame.image.load('images/background.png').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Leaderboard background
        self.leaderboard_background = pygame.image.load('images/leaderboard.jpg').convert()
        self.leaderboard_background = pygame.transform.scale(self.leaderboard_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    

        # Ending images
        self.happy_ending_images = [pygame.image.load(f'images/happy_ending/happy{i}.png').convert() for i in range(11)]
        self.bad_ending_images = [pygame.image.load(f'images/bad_ending/bad{i}.png').convert() for i in range(12)]
        self.current_image_index = 0
        self.ending_type = None

    
        

        # File load
        self.monster = Alien((400, 350))
        self.button1 = Button1((110, 350), self.visible_sprites)
        self.button2 = Button2((110, 350), self.visible_sprites)
        self.button3 = Button3((110, 350), self.visible_sprites)
        self.button4 = Button4((110, 350), self.visible_sprites)
        self.button5 = Button5((55, 175), self.visible_sprites)
        self.data = Data((0, 0), self.visible_sprites)  
        self.ui = UI()

        # Sound 
        main_sound = pygame.mixer.Sound('audio/song.mp3')
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

        

        # Other variable
        self.day = 1
        self.last_button_click_time = pygame.time.get_ticks() 
        self.current_scene = "game"
        self.start_time = pygame.time.get_ticks()
        self.leaderboard = []
        self.time_recorded = False
        self.elapsed_time = 0

        # mini game
        self.mini_game = 1
        self.button4.update()
        self.game.reset_keys()
        self.load_user_text()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not self.time_recorded:
                    self.record_time()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # click to next image at ending
                if self.current_scene in ["happy_ending", "bad_ending"]: # if current scene is ending
                    self.current_image_index += 1 # add 1 to current image index
                    if self.current_scene == "happy_ending" and self.current_image_index >= len(self.happy_ending_images): # when current images > total images will enter leaderboard
                        self.enter_leaderboard()
                elif self.button1.rect.collidepoint(event.pos): 
                    self.handle_button1_click()
                elif self.button2.rect.collidepoint(event.pos):  
                    self.handle_button2_click()
                elif self.button3.rect.collidepoint(event.pos):  
                    self.handle_button3_click()
                elif self.button5.rect.collidepoint(event.pos):  
                    self.current_scene = "bad_ending"
                
                elif self.button4.rect.collidepoint(event.pos): # enter the game
                    if self.mini_game == 1:
                        new_state = Level1(self.game)
                        new_state.enter_state()
                        
                    elif self.mini_game == 2 and self.day == 2:
                        new_state = Level2(self.game)
                        new_state.enter_state()
                        
                    elif self.mini_game == 3 and self.day == 3:
                        new_state = Level3(self.game)
                        new_state.enter_state()
                        
                    elif self.mini_game == 4 and self.day == 4:
                        new_state = Level4(self.game)
                        new_state.enter_state()
                        
                    elif self.mini_game == 5 and self.day == 5:
                        new_state = Level5(self.game)
                        new_state.enter_state()
                        

        current_time = pygame.time.get_ticks()
        self.elapsed_time = (current_time - self.start_time) / 1000
        
        if self.day == 6 and self.ui.stats['happiness'] == 100 and not self.time_recorded:  # Trigger happy ending
            self.current_scene = "happy_ending"
            self.record_time()

        if self.monster.monster_select in [2, 3, 4] and current_time - self.last_button_click_time >= 3000: # if there monster id is 2,3,4 and time > 3 second ,their monster display will become 1
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

            # add ui status
            self.monster.monster_select = 2 if self.monster.monster_select < 5 else 6 if self.monster.monster_select < 9 else 10 if self.monster.monster_select < 13 else 14 if self.monster.monster_select < 17 else 18
            self.last_button_click_time = pygame.time.get_ticks()
            self.ui.feeding = min(self.ui.feeding + 25, self.ui.stats['feeding']) # to limit 
            self.ui.cleanliness = min(self.ui.cleanliness - 10, self.ui.stats['cleanliness'])
            self.ui.happy = min(self.ui.happy + 5, self.ui.stats['happiness'])

            # button sound
            main_sound = pygame.mixer.Sound('audio/button.mp3')
            main_sound.set_volume(0.5)
            main_sound.play(loops=0)

            # feeding sound
            second_sound = pygame.mixer.Sound('audio/eat.mp3')
            second_sound.set_volume(0.5)
            second_sound.play(loops=0)
            self.ui.coin -= 1
            self.ui.save_collected_coins()

    def handle_button2_click(self):
        if self.ui.feeding >= 10 and self.ui.coin >= 1:

            # add ui status
            self.monster.monster_select = 3 if self.monster.monster_select < 5 else 7 if self.monster.monster_select < 9 else 11 if self.monster.monster_select < 13 else 15 if self.monster.monster_select < 17 else 19
            self.last_button_click_time = pygame.time.get_ticks()
            self.ui.feeding = min(self.ui.feeding - 10, self.ui.stats['feeding'])
            self.ui.cleanliness = min(self.ui.cleanliness + 25, self.ui.stats['cleanliness'])
            self.ui.happy = min(self.ui.happy + 5, self.ui.stats['happiness'])

            #button sound
            main_sound = pygame.mixer.Sound('audio/button.mp3')
            main_sound.set_volume(0.5)
            main_sound.play(loops=0)

            #washing sound
            second_sound = pygame.mixer.Sound('audio/wash.mp3')
            second_sound.set_volume(0.5)
            second_sound.play(loops=0)
            self.ui.coin -= 1
            self.ui.save_collected_coins()

    def handle_button3_click(self):
        if self.ui.feeding >= 20 and self.ui.coin >= 1:
            
            # add ui status
            self.monster.monster_select = 4 if self.monster.monster_select < 5 else 8 if self.monster.monster_select < 9 else 12 if self.monster.monster_select < 13 else 16 if self.monster.monster_select < 17 else 20
            self.ui.feeding = min(self.ui.feeding - 20, self.ui.stats['feeding'])
            self.ui.cleanliness = min(self.ui.cleanliness + 5, self.ui.stats['cleanliness'])
            self.ui.happy = min(self.ui.happy + 20, self.ui.stats['happiness'])

            #button sound
            main_sound = pygame.mixer.Sound('audio/button.mp3')
            main_sound.set_volume(0.5)
            main_sound.play(loops=0)
            self.ui.coin -= 1
            self.ui.save_collected_coins()

    def load_user_text(self):
        try: #prevent game crash
            with open('user_text.json', 'r') as file:
                data = json.load(file)
                self.user_text = data.get("user_text", "")
        except FileNotFoundError:
            self.user_text = ""

    



    def update(self, deltatime, actions):
        self.monster.update()
        current_time = pygame.time.get_ticks()  # get current time
        self.elapsed_time = current_time // 1000  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not pygame.mouse.get_pressed()[0]:
            self.click = False

        # Alien grow
        if all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 1:  # Day2
            self.ui.reset_stats()  # Reset stats
            self.monster.monster_select = 5
            self.day += 1
            self.mini_game += 1
            print(self.day)
            main_sound = pygame.mixer.Sound('audio/Upgrade.mp3')  # sound
            main_sound.set_volume(1)
            main_sound.play(loops=0)
        elif all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 2:  # Day3
            self.ui.reset_stats()
            self.monster.monster_select = 9
            self.day += 1
            print(self.day)
            self.mini_game += 1
            main_sound = pygame.mixer.Sound('audio/Upgrade.mp3')
            main_sound.set_volume(1)
            main_sound.play(loops=0)
        elif all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 3:  # Day4
            self.ui.reset_stats()
            self.monster.monster_select = 13
            self.mini_game += 1
            self.day += 1
            print(self.day)
            main_sound = pygame.mixer.Sound('audio/Upgrade.mp3')
            main_sound.set_volume(1)
            main_sound.play(loops=0)
        elif all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 4:  # Day5
            self.ui.reset_stats()
            self.monster.monster_select = 17
            self.day += 1
            self.mini_game += 1
            print(self.day)
            main_sound = pygame.mixer.Sound('audio/Upgrade.mp3')
            main_sound.set_volume(1)
            main_sound.play(loops=0)
        elif all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 5:
            self.day += 1

    def render(self, display, font):
        if self.current_scene == "game": # display
            display.blit(self.background, (0, 0))
            self.monster.render(display)
            self.visible_sprites.draw(display)
            self.ui.display(display)
            self.render_game_timer(display)
            self.render_game_level(display)

        elif self.current_scene == "leaderboard":  # switch to leaderboard
            self.render_leaderboard(display)
        elif self.current_scene == "happy_ending":
            if self.current_image_index < len(self.happy_ending_images):
                display.blit(self.happy_ending_images[self.current_image_index], (0, 0))
            else:
                self.enter_leaderboard()
        elif self.current_scene == "bad_ending":
            if self.current_image_index < len(self.bad_ending_images):
                display.blit(self.bad_ending_images[self.current_image_index], (0, 0))

    def render_game_timer(self, display):  # display seconds
        time_surface = self.font.render(f"Time: {int(self.elapsed_time)} seconds", True, (0, 0, 0))
        time_rect = time_surface.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        display.blit(time_surface, time_rect)

    def render_game_level(self, display):  # display level
        level_surface = self.font.render(f"Level: {self.day}", True, (0, 0, 0))
        level_rect = level_surface.get_rect(topright=(SCREEN_WIDTH - 450, 20))
        display.blit(level_surface, level_rect)


    def render_leaderboard(self, display):
        display.blit(self.leaderboard_background, (0, 0))
        text_y = 100
        sorted_leaderboard = sorted(self.combined_data.items(), key=lambda x: x[1]) #compare
        for user_text, time in sorted_leaderboard:
            rounded_time = int(time)
            text_surface = self.font.render(f"{user_text}: {rounded_time} seconds", True, (0, 0, 0)) #display x
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, text_y)) #y
            display.blit(text_surface, text_rect)
            text_y += 50 # two data between range

    def save_leaderboard(self): # json
        with open("leaderboard.json", "w") as file:
            json.dump(self.leaderboard, file)

    def record_time(self): # save
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
