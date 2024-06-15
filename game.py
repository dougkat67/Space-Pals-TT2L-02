import pygame
import time
from states.menu import Menu



class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Space Pals')
        self.running, self.playing = True, True
        self.DISPLAY_W, self.DISPLAY_H = 1000, 500
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = pygame.font.SysFont("Pixeltype Regular", 50, False, False)
        self.actions = {"left": False, "right": False, "up": False, "down": False, "action1": False, "action2": False, "start": False, "play": False}
        self.dt, self.prev_time = 0, 0    #dt is delta time
        self.state_stack = []
        self.clock = pygame.time.Clock()
        self.load_states()
        
    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()
            self.clock.tick(60)


    def get_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.actions["start"] = True

            self.mouse = pygame.mouse.get_pos()
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    self.playing = False
                if event.key == pygame.K_a:
                    self.actions["left"] = True
                if event.key == pygame.K_d:
                    self.actions["right"] = True
                if event.key == pygame.K_w:
                    self.actions["up"] = True
                if event.key == pygame.K_s:
                    self.actions["down"] = True
                if event.key == pygame.K_o:
                    self.actions["action1"] = True
                if event.key == pygame.K_p:
                    self.actions["action2"] = True
                if event.key == pygame.K_RETURN:
                    self.actions["play"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.actions["left"] = False
                if event.key == pygame.K_d:
                    self.actions["right"] = False
                if event.key == pygame.K_w:
                    self.actions["up"] = False
                if event.key == pygame.K_s:
                    self.actions["down"] = False
                if event.key == pygame.K_o:
                    self.actions["action1"] = False
                if event.key == pygame.K_p:
                    self.actions["action2"] = False
                if event.key == pygame.K_RETURN:
                    self.actions["play"] = False

            if event.type == pygame.MOUSEBUTTONUP:
                if pygame.mouse.get_pressed()[0]:
                 self.actions["start"] = False

        if self.state_stack:
                self.state_stack[-1].handle_events(events)

    def update(self):
        self.state_stack[-1].update(self.dt, self.actions)
   
    def render(self):
        self.state_stack[-1].render(self.display, self.font_name)
        self.window.blit(self.display, (0,0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y, font):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_surface, text_rect)

    def load_states(self):
        self.menu_screen = Menu(self)
        self.state_stack.append(self.menu_screen)

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False
   
if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()