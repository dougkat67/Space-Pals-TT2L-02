import pygame
import sys
import pyelement
from math import floor
from alien import Alien
from button import Button1
from button2 import Button2
from setting import *
from ui import UI



class Game:
    def __init__(self):
        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pet Game')
        self.clock = pygame.time.Clock()
        self.visible_sprites = pygame.sprite.Group()

        # Load background image
        self.background = pygame.image.load('background.png').convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))


        #build the sprite
        self.monster = Alien((400,350))
        self.button1 = Button1((110,410),self.visible_sprites)
        self.button2 = Button2((110,410),self.visible_sprites)

        #Ui
        self.ui = UI()


    def run(self):
        while True:
            current_time = pygame.time.get_ticks() #record time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  
                    if self.button1.rect.collidepoint(event.pos):  #for button1
                        self.monster.monster_select = 2
                        self.last_button_click_time = current_time
                        if self.ui.satiety >= self.ui.stats['satiety']:
                            self.ui.health = self.ui.stats['satiety']
                        else:
                            self.ui.satiety += 10
                    
                    if self.button2.rect.collidepoint(event.pos): #for button2
                        self.monster.monster_select = 3
                        self.last_button_click_time = current_time


            if self.monster.monster_select == 2 and current_time - self.last_button_click_time >= 3000:
                self.monster.monster_select = 1

            
            self.screen.blit(self.background, (0, 0))  
            self.monster.update(self.screen)  
            self.visible_sprites.draw(self.screen)
            
            self.ui.display()

            pygame.display.flip()  
            self.clock.tick(60)  






if __name__ == "__main__":
    game = Game()
    game.run()
