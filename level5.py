import os
import random
import pygame
from collecting_coins import Coin

class Level1:
     def __init__(self, game):
        super().__init__(game)
        self.screen_width, self.screen_height = 1000, 500
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.display.fill((173, 216, 230))
        self.clock = pygame.time.Clock()
        self.time_limit = 10  # 10 seconds
        self.current_time = 0
        self.start_time = pygame.time.get_ticks() // 1000  # current time in seconds
        self.font = pygame.font.Font(None, 36)
        self.running = True

     def handle_events(self, actions):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_a]:
                    self.game.player["left"] = True 
                if pressed_keys[pygame.K_d]:
                    self.game.player["right"] = True  
                if pressed_keys[pygame.K_w]:
                    self.game.player["up"] = True 
                if pressed_keys[pygame.K_s]:
                    self.game.player["down"] = True 

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.game.player["left"] = False
                if event.key == pygame.K_d:
                    self.game.player["right"] = False
                if event.key == pygame.K_w:
                    self.game.player["up"] = False
                if event.key == pygame.K_s:
                    self.game.player["down"] = False

     def update(self, deltatime, actions):
        self.current_time = pygame.time.get_ticks() // 1000 - self.start_time
        if self.current_time >= self.time_limit:
            self.running = False
            # Transition to end state
            self.game.change_state(Level1(self.game))

     def render(self, display):
        display.fill((173, 216, 230))
        remaining_time = max(self.time_limit - self.current_time, 0)
        timer_text = self.font.render(f"Time: {int(remaining_time)}", True, (255, 255, 255))
        timer_text_rect = timer_text.get_rect(topright=(self.screen_width - 10, 10))
        display.blit(timer_text, timer_text_rect)

        # Update and draw all sprites
        self.game.all_sprites.update()
        self.game.all_sprites.draw(display)

class Player(pygame.sprite.Sprite):
    def __init__(self, images, grid_size, animation_speed=0.2, initial_position=(0, 0)):
        super().__init__()
        self.images = images if isinstance(images, list) else [images]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.animation_speed = animation_speed
        self.animation_timer = 0
        self.rect = self.image.get_rect(topleft=initial_position)
        self.grid_size = grid_size
        self.walls = []

    def update(self):
        self.animation_timer += self.game.clock.get_time() / 1000.0
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def move(self, dx, dy):
        self.rect.x += dx * self.grid_size
        self.rect.y += dy * self.grid_size
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

                    