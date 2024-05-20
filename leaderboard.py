import pygame
import os
import json
from level import Game
from setting import *

class ButtonGame:
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pet Game')
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 36) #font 
        self.start_time = 0 # start time
        self.elapsed_time = 0 # passed time
        
        self.game = Game
        self.game = "main.menu" # set main menu as game
        

        self.current_scene = "main_menu" # scene
        self.leaderboard = [] # score box display
        if os.path.exists("leaderboard.json"): # save data
            with open("leaderboard.json", "r") as file:
                self.leaderboard = json.load(file)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
            self.update()
            self.render()
            self.clock.tick(60)
        self.save_leaderboard()
        pygame.quit()

    def handle_mouse_click(self, event):
        if self.current_scene == "main_menu":
            if self.button_rect.collidepoint(event.pos): # click the button
                self.current_scene = "leaderboard" # change scene to leaderboard

                self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000 #recording time

                self.leaderboard.append({"time": self.elapsed_time}) #display time
                self.start_time = pygame.time.get_ticks() #calculating time
        elif self.current_scene == "leaderboard":
            self.current_scene = "main_menu"

    def update(self):
        if self.current_scene == "main_menu":
            self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def render(self):
        self.screen.fill(self.white)
        if self.current_scene == "main_menu":
            self.render_main_menu()
        elif self.current_scene == "leaderboard":
            self.render_leaderboard()
        pygame.display.flip()

    def render_main_menu(self): # display the main menu
        self.button_rect = pygame.draw.rect(self.screen, self.red, (self.screen_width // 2 - 50, self.screen_height // 2 - 25, 100, 50))
        time_surface = self.font.render(f"Time: {self.elapsed_time} seconds", True, (0, 0, 0))
        time_rect = time_surface.get_rect(topright=(self.screen_width - 20, 20))
        self.screen.blit(time_surface, time_rect)

    def render_leaderboard(self): #display the leaderboard
        text_y = 100
        sorted_leaderboard = sorted(self.leaderboard, key=lambda x: x["time"])
        for entry in sorted_leaderboard:
            text_surface = self.font.render(f"{entry['time']} seconds", True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen_width // 2, text_y))
            self.screen.blit(text_surface, text_rect)
            text_y += 50

    def save_leaderboard(self): # save and load 
        with open("leaderboard.json", "w") as file:
            json.dump(self.leaderboard, file)

if __name__ == "__main__":
    game = ButtonGame()
    game.run()