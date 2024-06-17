import pygame
import json 
from states.state import State
from level import Pet

class Naming(State):
    def __init__(self, game):
        super().__init__(game)  
        self.game = game
        self.naming_image = pygame.image.load("WIP_art/naming_page.png").convert()
        self.naming_font = pygame.font.SysFont("Pixeltype Regular", 50, False, False)
        self.user_text = ""
        self.input_rect = pygame.Rect(500, 450, 200, 32)  
        self.color_active = (0, 0, 0)
        self.color_passive = (255, 0, 0)
        self.color = self.color_passive
        self.active = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[0:-1]
                else:
                    self.user_text += event.unicode
                
                
                if self.user_text.endswith('\r'):
                    self.save_user_text()

    def update(self, deltatime, actions):
        self.color = self.color_active if self.active else self.color_passive
        self.actions = self.game.actions

        if self.actions["play"] and self.user_text:

            new_state = Pet(self.game)
            new_state.enter_state()  
        self.game.reset_keys()

    def render(self, display, font):

        display.blit(self.naming_image, (0, 0))
        self.game.draw_text(display, "You encountered an interesting looking alien egg.", (0, 0, 0), 500, 50, font)
        self.game.draw_text(display, "It's hatching!", (0, 0, 0), 500, 100, font)
        self.game.draw_text(display, "Name the egg: ", (0, 0, 0), 300, 470, font)
        self.user_input_rect = pygame.draw.rect(display, self.color, self.input_rect, 3)  # border width
        self.user_input_rect = pygame.draw.rect(display, self.color, self.input_rect, 3)
        self.text_surface = self.naming_font.render(self.user_text, True, (0, 0, 0))
        display.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
        self.input_rect.w = max(200, self.text_surface.get_width() + 10)


    def reset_keys(self):
        for action in self.game.actions:
            self.game.actions[action] = False

    def save_user_text(self):
        
        try:
            with open('user_text.json', 'r') as file:
                data = json.load(file)
            if not isinstance(data, dict) or "user_texts" not in data:
                data = {"user_texts": []}
        except FileNotFoundError:
            data = {"user_texts": []}

       
        data["user_texts"].append(self.user_text.strip())

        
        with open('user_text.json', 'w') as file:
            json.dump(data, file, indent=4)

        
        self.user_text = ""
