import os
import random
import pygame
from collecting_coins import Coin

# class the orange dude
class Player(object):
    def __init__(self, grid_size, initial_position=(0, 0)):
        self.rect = pygame.Rect(initial_position[0], initial_position[1], grid_size, grid_size)
        self.grid_size = grid_size

    def move(self, dx, dy):
        # move by grid size
        dx *= self.grid_size
        dy *= self.grid_size
        # move each axis separately. Note that this checks for collision
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        # move the rect
        self.rect.x += dx
        self.rect.y += dy

        # if collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # moving right; hit left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # moving left; hit right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # moving down; hit top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # moving up; hit bottom side of the wall
                    self.rect.top = wall.rect.bottom

# nice class to hold a wall rect
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], grid_cell_size, grid_cell_size)

# initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# set up the display
pygame.display.set_caption("Maze")
screen_width, screen_height = 1000,500
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
walls = [] # list to hold the walls
grid_cell_size = 50
coin_images = [pygame.image.load('images/coin_0.png'),
               pygame.image.load('images/coin_1.png'),
               pygame.image.load('images/coin_2.png'),
               pygame.image.load('images/coin_3.png'),
               pygame.image.load('images/coin_4.png'),
               pygame.image.load('images/coin_5.png')]
coins = [Coin(grid_cell_size, (x, y), coin_images) for x in range(0, screen_width, grid_cell_size) for y in range(0, screen_height, grid_cell_size)]

# holds the level layout in a list of strings
# use 20walls/row, 10walls/column
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W       W   WWWWWWWW",
    "WWW  WWWWW  WWWWWWWW",
    "WWW         WWWW   W",
    "W           WWWW   W",
    "WWWWW              W",
    "W   W WWW        W W",
    "W W   WWW  WWWW  W W",
    "W W   WWW   WWWWWWEW",
    "WWWWWWWWWWWWWWWWWWWW",
]

# Calculate the size of each grid cell based on the screen dimensions and number of cells
num_cols = len(level[0])
num_rows = len(level)
grid_cell_size = 50
screen_width = num_cols * grid_cell_size
screen_height = num_rows * grid_cell_size

# Parse the level string above. W = wall, E = exit
for y, row in enumerate(level):
    for x, col in enumerate(row):
        if col == "W":
            Wall((x * grid_cell_size, y * grid_cell_size))
        if col == "E":
            end_rect = pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size)
            pygame.draw.rect(screen, (255, 165, 0), end_rect) # Draw the exit

# create coins at specific positions
coins = [Coin(grid_cell_size,(4, 2), coin_images),
         Coin(grid_cell_size, (10, 4), coin_images),
         Coin(grid_cell_size, (18, 6), coin_images)
         ]

# Set the player's initial position
initial_grid_x = 1
initial_grid_y = 1
player_initial_position = (initial_grid_x * grid_cell_size, initial_grid_y * grid_cell_size)
player = Player(grid_cell_size, player_initial_position)  # Create the player with adjusted initial position

running = True
while running:
    # calculate delta time
    dt = clock.tick(60) / 1000.0 # convert milliseconds to seconds
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_a]:
                player.move(-1, 0)  # Move left
            elif pressed_keys[pygame.K_d]:
                player.move(1, 0)   # Move right
            elif pressed_keys[pygame.K_w]:
                player.move(0, -1)  # Move up
            elif pressed_keys[pygame.K_s]:
                player.move(0, 1)   # Move down

    # check for collision with the exit
    if player.rect.colliderect(end_rect):
        print("You win!")
        running = False

    # fill the screen with black
    screen.fill((0, 0, 0))
    # draw the walls
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    # draw the exit
    pygame.draw.rect(screen, (255, 165, 0), end_rect)
    # draw the player
    pygame.draw.rect(screen, (0, 0, 255), player.rect)
    for coin in coins:
        coin.update(dt) # update coin animation
        screen.blit(coin.image, coin.rect) # render coin image on screen

    # update the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(60)

pygame.quit()