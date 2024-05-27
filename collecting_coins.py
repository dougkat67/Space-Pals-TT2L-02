# coin sprite by DasBilligeAlien
# https://opengameart.org/content/rotating-coin-0

import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, grid_size, pos, coin_images):
        super().__init__()
        self.coin_images = coin_images # list of coin images for animation
        self.image_index = 0 # index track current frame of animation
        self.image = self.coin_images[self.image_index] # initial image
        self.rect = self.image.get_rect(topleft=(pos[0] * grid_size, pos[1] * grid_size)) # adjust position based on grid size
        self.animation_speed = 0.08 # speed of animation(adjust as needed)
        self.animation_timer = 0 # timer for animation

    def update(self, dt):
         # update animation timer
         self.animation_timer += dt

         # if enough time has passed, advance to the next frame
         if self.animation_timer >= self.animation_speed:
             self.image_index = (self.image_index + 1) % len(self.coin_images) # loop back to start if at end
             self.image = self.coin_images[self.image_index] # update image
             self.animation_timer = 0 # reset animation timer

    def collect(self):
        # perform actions when the coin is collected
        self.kill() # remove the coin from the sprite group
        return 1 # return value of the collected coin