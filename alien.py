import pygame
import pyelement
class Alien(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.animation_cooldown = 10
        self.animation_timer = 0
        self.frame = 0
        self.monster_select = 1
        self.load_images()

        # self.stats
        self.stats = {'happiness':50,'clearness':50 , 'satiety':50}
        self.happy = self.stats['happiness']
        self.clear = self.stats['clearness']
        self.satiety = self.stats['satiety']


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