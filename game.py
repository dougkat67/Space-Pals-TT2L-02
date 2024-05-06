import pygame
import time
from states.menu import Menu


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, True
        self.DISPLAY_W, self.DISPLAY_H = 1000, 500
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = pygame.font.SysFont("Pixeltype Regular", 50, False, False)
        self.actions = {"left": False, "right": False, "up": False, "down": False, "action1": False, "action2": False, "start": False}
        self.dt, self.prev_time = 0, 0    #dt is delta time
        self.state_stack = []
        #self.load_assets()
        
    def game_loop(self):
        while self.playing:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
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
                    self.actions["start"] = True

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
                    self.actions["start"] = False

    def update(self):
        pass
   
    def render(self):
        self.display.blit(self.display, (0,0))
        pygame.display.flip()

    def get_dt(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now

    def draw_text(self, surface, text, color, x, y):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        surface.blit = (text_surface, text_rect)

    #did not add the OS function

    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False
   
if __name__ == "__main__":
    g = Game()
    while g.running:
        g.game_loop()