import os
import random
import pygame

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

# holds the level layout in a list of strings
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                        W",
    "W                        W",
    "WWW    WWWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWWW",
    "WWW                      W",
    "WWW                     EW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# Calculate the size of each grid cell based on the screen dimensions and number of cells
num_cols = len(level[0])
num_rows = len(level)
grid_cell_size = min(screen_width // num_cols, screen_height // num_rows)

# Parse the level string above. W = wall, E = exit
for y, row in enumerate(level):
    for x, col in enumerate(row):
        if col == "W":
            Wall((x * grid_cell_size, y * grid_cell_size))
        if col == "E":
            end_rect = pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size)
            pygame.draw.rect(screen, (255, 165, 0), end_rect) # Draw the exit

# Set the player's initial position
player_initial_position = (grid_cell_size // 0.85, grid_cell_size // 0.85)  # Adjust the initial position here
player = Player(grid_cell_size, player_initial_position)  # Create the player with adjusted initial position

running = True
while running:
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

    # fill the screen with black
    screen.fill((0, 0, 0))

    # draw the walls
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)

    # draw the exit
    pygame.draw.rect(screen, (255, 165, 0), end_rect)

    # draw the player
    pygame.draw.rect(screen, (0, 0, 255), player.rect)

    # check for collision with the exit
    if player.rect.colliderect(end_rect):
        print("You win!")
        running = False

    # update the display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(60)

pygame.quit()