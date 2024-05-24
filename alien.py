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

        # Day 1
        monster_sprite1_img = pygame.image.load('images/monster_sprite1.png').convert_alpha()
        monster_sprite2_img = pygame.image.load('images/monster_sprite2.png').convert_alpha()
        monster_sprite3_img = pygame.image.load('images/monster_sprite3.png').convert_alpha()
        monster_sprite4_img = pygame.image.load('images/monster_sprite4.png').convert_alpha()
        self.monster_sprite1 = pyelement.SpriteSheet(monster_sprite1_img)
        self.monster_sprite2 = pyelement.SpriteSheet(monster_sprite2_img)
        self.monster_sprite3 = pyelement.SpriteSheet(monster_sprite3_img)
        self.monster_sprite4 = pyelement.SpriteSheet(monster_sprite4_img)

        # Day 2
        monster_sprite2_1_img = pygame.image.load('images/Day2/Monster_sprite2_1.png').convert_alpha()
        monster_sprite2_2_img = pygame.image.load('images/Day2/Monster_sprite2_2.png').convert_alpha()
        monster_sprite2_3_img = pygame.image.load('images/Day2/Monster_sprite2_3.png').convert_alpha()
        monster_sprite2_4_img = pygame.image.load('images/Day2/Monster_sprite2_4.png').convert_alpha()
        self.monster_sprite2_1 = pyelement.SpriteSheet(monster_sprite2_1_img)
        self.monster_sprite2_2 = pyelement.SpriteSheet(monster_sprite2_2_img)
        self.monster_sprite2_3 = pyelement.SpriteSheet(monster_sprite2_3_img)
        self.monster_sprite2_4 = pyelement.SpriteSheet(monster_sprite2_4_img)

        # Day 3
        monster_sprite3_1_img = pygame.image.load('images/Day3/Monster_sprite3_1.png').convert_alpha()
        monster_sprite3_2_img = pygame.image.load('images/Day3/Monster_sprite3_2.png').convert_alpha()
        monster_sprite3_3_img = pygame.image.load('images/Day3/Monster_sprite3_3.png').convert_alpha()
        monster_sprite3_4_img = pygame.image.load('images/Day3/Monster_sprite3_4.png').convert_alpha()
        self.monster_sprite3_1 = pyelement.SpriteSheet(monster_sprite3_1_img)
        self.monster_sprite3_2 = pyelement.SpriteSheet(monster_sprite3_2_img)
        self.monster_sprite3_3 = pyelement.SpriteSheet(monster_sprite3_3_img)
        self.monster_sprite3_4 = pyelement.SpriteSheet(monster_sprite3_4_img)

        # Day 4
        monster_sprite4_1_img = pygame.image.load('images/Day4/Monster_sprite4_1.png').convert_alpha()
        monster_sprite4_2_img = pygame.image.load('images/Day4/Monster_sprite4_2.png').convert_alpha()
        monster_sprite4_3_img = pygame.image.load('images/Day4/Monster_sprite4_3.png').convert_alpha()
        monster_sprite4_4_img = pygame.image.load('images/Day4/Monster_sprite4_4.png').convert_alpha()
        self.monster_sprite4_1 = pyelement.SpriteSheet(monster_sprite4_1_img)
        self.monster_sprite4_2 = pyelement.SpriteSheet(monster_sprite4_2_img)
        self.monster_sprite4_3 = pyelement.SpriteSheet(monster_sprite4_3_img)
        self.monster_sprite4_4 = pyelement.SpriteSheet(monster_sprite4_4_img)

        # Day 5
        monster_sprite5_1_img = pygame.image.load('images/Day5/Monster_sprite5_1.png').convert_alpha()
        monster_sprite5_2_img = pygame.image.load('images/Day5/Monster_sprite5_2.png').convert_alpha()
        monster_sprite5_3_img = pygame.image.load('images/Day5/Monster_sprite5_3.png').convert_alpha()
        monster_sprite5_4_img = pygame.image.load('images/Day5/Monster_sprite5_4.png').convert_alpha()
        self.monster_sprite5_1 = pyelement.SpriteSheet(monster_sprite5_1_img)
        self.monster_sprite5_2 = pyelement.SpriteSheet(monster_sprite5_2_img)
        self.monster_sprite5_3 = pyelement.SpriteSheet(monster_sprite5_3_img)
        self.monster_sprite5_4 = pyelement.SpriteSheet(monster_sprite5_4_img)

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
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()  #scale
            screen.blit(animation, (270, 250)) # position
        elif self.monster_select == 2:
            animation = self.monster_sprite2.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))
        elif self.monster_select == 3:
            animation = self.monster_sprite3.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 4:
            animation = self.monster_sprite4.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 5: #Day 2
            animation = self.monster_sprite2_1.get_frame(self.frame, 480, 600, 1, (0, 0, 0)) #area
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 150))

        elif self.monster_select == 6:
            animation = self.monster_sprite2_2.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 7:
            animation = self.monster_sprite2_3.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 8:
            animation = self.monster_sprite2_4.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 9: #Day 3
            animation = self.monster_sprite3_1.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 10:
            animation = self.monster_sprite3_2.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 11:
            animation = self.monster_sprite3_3.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 12:
            animation = self.monster_sprite3_4.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 13: #Day 4
            animation = self.monster_sprite3_1.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 14:
            animation = self.monster_sprite3_2.get_frame(self.frame, 480, 480, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 15:
            animation = self.monster_sprite3_3.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 16:
            animation = self.monster_sprite3_4.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 17: #Day 5
            animation = self.monster_sprite3_1.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 18:
            animation = self.monster_sprite3_2.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 19:
            animation = self.monster_sprite3_3.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))

        elif self.monster_select == 20:
            animation = self.monster_sprite3_4.get_frame(self.frame, 480, 600, 1, (0, 0, 0))
            animation = pygame.transform.scale(animation, (250, 250)).convert_alpha()
            screen.blit(animation, (270, 250))