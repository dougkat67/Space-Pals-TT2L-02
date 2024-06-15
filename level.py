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
# from leaderboard import ButtonGame



class Pet(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.visible_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 36)


        #Background
        self.background = pygame.image.load('background.png').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))


        # file load
        self.monster = Alien((400, 350))
        self.button1 = Button1((110, 350), self.visible_sprites)
        self.button2 = Button2((110, 350), self.visible_sprites)
        self.button3 = Button3((110, 350), self.visible_sprites)
        self.ui = UI()

        #Sound 
        main_sound = pygame.mixer.Sound('audio/song.mp3')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)

        # OTHER variable

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
        

        

    def handle_events(self, events):
        pass

    def update(self, deltatime, actions):
        self.monster.update()
        current_time = pygame.time.get_ticks()
        self.elapsed_time = (current_time - self.start_time) // 1000
        if self.button1.rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.eat = True
                if self.eat:
                    self.monster.monster_select = 2 if self.monster.monster_select < 5 else 6 if  self.monster.monster_select < 9 else 10
                    self.last_button_click_time = current_time
                    self.ui.feeding = min(self.ui.feeding + 10, self.ui.stats['feeding'])
                    self.eat = False
                self.click = True
            if pygame.mouse.get_pressed()[0]:
                self.eat = False
                self.click = False

        if self.button2.rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.bath = True
                if self.bath:
                    self.monster.monster_select = 3 if self.monster.monster_select < 5 else 7 if  self.monster.monster_select < 9 else 11
                    self.last_button_click_time = current_time
                    self.ui.cleanliness = min(self.ui.cleanliness + 10, self.ui.stats['cleanliness'])
                    self.bath = False
                self.click = True
                
            if pygame.mouse.get_pressed()[0]:
                self.bath = False
                self.click = False

        if self.button3.rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.entertain = True
                if self.entertain:
                    self.monster.monster_select = 4 if self.monster.monster_select < 5 else 8 if  self.monster.monster_select < 9 else 12
                    self.last_button_click_time = current_time
                    self.ui.happy = min(self.ui.happy + 10, self.ui.stats['happiness'])
                    self.entertain = False
                self.click = True
                
            if pygame.mouse.get_pressed()[0]:
                self.entertain = False
                self.click = False          


    def update(self,deltatime,actions):
            self.monster.update()
            current_time = pygame.time.get_ticks()
            self.elapsed_time = (current_time - self.start_time) // 1000


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button1.rect.collidepoint(event.pos): # Feeding
                        if self.ui.cleanliness >= 10 and self.ui.coin >= 1 :
                            self.monster.monster_select = 2 if self.monster.monster_select < 5 else 6 if  self.monster.monster_select < 9 else 10 if  self.monster.monster_select < 13 else 14  if  self.monster.monster_select < 17 else 18 
                            self.last_button_click_time = current_time
                            self.ui.feeding = min(self.ui.feeding + 20, self.ui.stats['feeding']) # Feeding 
                            self.ui.cleanliness = min(self.ui.cleanliness - 10, self.ui.stats['cleanliness']) # Bathing
                            self.ui.happy = min(self.ui.happy + 5, self.ui.stats['happiness']) # Happiness


                            main_sound = pygame.mixer.Sound('audio/button.mp3')
                            main_sound.set_volume(0.5)
                            main_sound.play(loops = 0)

                            second_sound = pygame.mixer.Sound('audio/eat.mp3')
                            second_sound.set_volume(0.5)
                            second_sound.play(loops = 0)

                            self.ui.coin -= 1
                        else :
                            pass
                        

                    elif self.button2.rect.collidepoint(event.pos): # Bathing
                        if self.ui.feeding >= 10 and self.ui.coin >= 1 :
                            self.monster.monster_select = 3 if self.monster.monster_select < 5 else 7 if  self.monster.monster_select < 9 else 11 if  self.monster.monster_select < 13 else 15 if  self.monster.monster_select < 17 else 19
                            self.last_button_click_time = current_time
                            self.ui.feeding = min(self.ui.feeding - 10, self.ui.stats['feeding'])
                            self.ui.cleanliness = min(self.ui.cleanliness + 20, self.ui.stats['cleanliness'])
                            self.ui.happy = min(self.ui.happy + 5, self.ui.stats['happiness'])

                            main_sound = pygame.mixer.Sound('audio/button.mp3')
                            main_sound.set_volume(0.5)
                            main_sound.play(loops = 0)

                            second_sound = pygame.mixer.Sound('audio/wash.mp3')
                            second_sound.set_volume(0.5)
                            second_sound.play(loops = 0)

                            self.ui.coin -= 1
                        else :
                            pass

                    elif self.button3.rect.collidepoint(event.pos): # Happiness
                        if self.ui.feeding >= 20 and self.ui.coin >= 1 :
                            self.monster.monster_select = 4 if self.monster.monster_select < 5 else 8 if  self.monster.monster_select < 9 else 12 if  self.monster.monster_select < 13 else 16 if  self.monster.monster_select < 17 else 20
                            self.ui.feeding = min(self.ui.feeding - 20, self.ui.stats['feeding'])
                            self.ui.cleanliness = min(self.ui.cleanliness + 5, self.ui.stats['cleanliness'])
                            self.ui.happy = min(self.ui.happy + 15, self.ui.stats['happiness'])

                            main_sound = pygame.mixer.Sound('audio/button.mp3')
                            main_sound.set_volume(0.5)
                            main_sound.play(loops = 0)

                            self.ui.coin -= 1
                        else :
                            pass
                    

            # Alien grow

            if all([self.ui.happy >= self.ui.stats['happiness']]) and self.day == 1  : # Day2
                self.ui.reset_stats()
                self.monster.monster_select = 5 
                self.day += 1
                print(self.day)
                main_sound = pygame.mixer.Sound('audio/Upgrade.mp3')
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

            if self.current_scene == "game":
                self.render_game_timer()

            pygame.display.flip()
            self.clock.tick(60)



        
            

            

    
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

