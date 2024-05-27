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
alien_animation = AlienAnimation(screen) # pass screen object here

# set the initial screen
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
                    current_screen = alien_animation
                    alien_animation.run() # call the run method to start the animation loop
                else:
                    current_screen = screen1

    # check the current screen type and update accordingly
    if current_screen == screen1 :
        screen1.update()
    elif current_screen == alien_animation:
        # no need to call update for AlienAnimation science it has its own animation loop
        pass

    # refresh screen
    pygame.display.update()

# quit pygame
pygame.quit()
sys.exit()