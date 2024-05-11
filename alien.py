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
        self.load_images()  # Call load_images method to load images

    def load_images(self):
        # Loading area
        monster_sprite1_img = pygame.image.load('images/monster_sprite1.png').convert_alpha()
        monster_sprite2_img = pygame.image.load('images/monster_sprite2.png').convert_alpha()
        monster_sprite3_img = pygame.image.load('images/monster_sprite3.png').convert_alpha()
        monster_sprite4_img = pygame.image.load('images/monster_sprite4.png').convert_alpha()
        self.monster_sprite1 = pyelement.SpriteSheet(monster_sprite1_img)
        self.monster_sprite2 = pyelement.SpriteSheet(monster_sprite2_img)
        self.monster_sprite3 = pyelement.SpriteSheet(monster_sprite3_img)
        self.monster_sprite4 = pyelement.SpriteSheet(monster_sprite4_img)

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
            screen.blit(animation, (270, 250)) # position
        elif self.monster_select == 2:
            animation = self.monster_sprite2.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (330, 330)).convert_alpha()
            screen.blit(animation, (230, 220))
        elif self.monster_select == 3:
            animation = self.monster_sprite3.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (330, 330)).convert_alpha()
            screen.blit(animation, (230, 220))
        elif self.monster_select == 4:
            animation = self.monster_sprite4.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (330, 330)).convert_alpha()
            screen.blit(animation, (230, 220))
        