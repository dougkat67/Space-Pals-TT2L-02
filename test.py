import pygame
import sys
import pyelement
from math import floor

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 1000

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
        self.monster = Data((400,350))
        self.button1 = button((110,410),self.visible_sprites)

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

            if self.monster.monster_select == 2 and current_time - self.last_button_click_time >= 3000:
                self.monster.monster_select = 1

            
            self.screen.blit(self.background, (0, 0))  
            self.monster.update(self.screen)  
            self.visible_sprites.draw(self.screen)

            pygame.display.flip()  
            self.clock.tick(60)  

class Data(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.animation_cooldown = 10
        self.animation_timer = 0
        self.frame = 0
        self.monster_select = 1
        self.load_images()

    def load_images(self):
        # Loading area
        monster_sprite1_img = pygame.image.load('images/monster_sprite1.png').convert_alpha()
        monster_sprite2_img = pygame.image.load('images/monster_sprite2.png').convert_alpha()
        self.monster_sprite1 = pyelement.SpriteSheet(monster_sprite1_img)
        self.monster_sprite2 = pyelement.SpriteSheet(monster_sprite2_img)

    def update(self, screen):
        # Animation
        self.animation_timer += 1
        if self.animation_timer >= self.animation_cooldown:
            self.frame += 1
            self.animation_timer = 0
        if self.frame >= 4:
            self.frame = 0

        # Render monster
        if self.monster_select == 1:
            animation = self.monster_sprite1.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))
        elif self.monster_select == 2:
            animation = self.monster_sprite2.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (330, 330)).convert_alpha()
            screen.blit(animation, (230, 220))


class button(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/feedingbutton.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

if __name__ == "__main__":
    game = Game()
    game.run()
