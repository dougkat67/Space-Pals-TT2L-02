import pygame
import sys
from screen1 import Screen1
from alien_animation import AlienAnimation

# Initialize Pygame
pygame.init()

# set up the screen
screenwidth = 1000
screenheight = 500
screen = pygame.display.set_mode((screenwidth, screenheight))
pygame.display.set_caption('minigame')

# create instances of screens
screen1 = Screen1(screen)
screen2 = AlienAnimation(screen)

# Variable to keep track of which screen to display
current_screen = screen1

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # switch to the next screen
                if current_screen == screen1:
                    current_screen = screen2
                else:
                    current_screen = screen2

    # update current screen
    current_screen.update()

    # refresh screen
    pygame.display.update()

# quit pygame
pygame.quit()
sys.exit()