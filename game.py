import pygame
from menu import Mainmenu


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1000, 500
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = pygame.font.SysFont("Pixeltype Regular", 50, False, False)
        self.current_menu = Mainmenu(self)

   
    def game_loop(self, text1, text2):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill((0,0,0))
            self.draw_text(text1, text2, 200, 500, 25)  # Pass text arguments to draw_text method
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()

    def draw_text(self, text1, text2, x, y, size):
        font = self.font_name
        text_surface1 = font.render("You encountered an fascinating looking alien egg.", True, (255, 255, 255))
        text_surface2 = font.render("It's hatching!", True, (255, 255, 255))
        text_rect1 = text_surface1.get_rect()
        text_rect2 = text_surface2.get_rect()
        text_rect1.center = (x, y)
        text_rect2.center = (x, y + 30)
        self.display.blit(text_surface1, text_rect1)
        self.display.blit(text_surface2, text_rect2)

    #to break the game-loop
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.current_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
            #now add a variable for when players are not pressing up, the variable should not be True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False


    #self is the reference to the game, to have access to all the variables
    # def draw_text(self, text1, text2, size, x, y):
    #     font = self.font_name
    #     text_surface1 = font.render(text1, True, (255, 255, 255))
    #     text_surface2 = font.render(text2, True, (255, 255, 255))
    #     text_rect1 = text_surface1.get_rect()
    #     text_rect2 = text_surface2.get_rect()
    #     text_rect1.center = (x, y)
    #     text_rect2.center = (x, y + 30)  # Adjust the y-coordinate for the second line
    
    
    # def draw_text(self, text, size, x, y ):
    #     font = self.font_name
    #     text_surface = font.render(text,True, (255,255,255))
    #     text_rect = text_surface.get_rect()
    #     text_rect.center = (x,y)
    #     self.display.blit(text_surface,text_rect)
    