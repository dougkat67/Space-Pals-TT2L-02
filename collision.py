import os
import pygame
from alien_animation import AlienAnimation

# class for the orange dude
class Player(pygame.sprite.Sprite):

    def __init__(self, start_pos, tile_size, animation):
        super().__init__()
        self.animation = animation
        self.rect = self.animation.player
        self.rect.topleft = start_pos

    def move(self, dx, dy):
        # move each axis separately. Note that this checks for collisions
        self.rect.x += dx
        self.rect.y += dy

    def move_single_axis(self, dx, dy, tile_size):

        # move the rect
        self.rect.x += dx
        self.rect.y += dy

        # if you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; hit left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0: # Moving left; hit right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0: # Moving down; hit top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0: # Moving up; hit bottom side of the wall
                    self.rect.top = wall.rect.bottom

# nice class to hold a wall rect
class Wall(object):
    def __init__(self, pos, tile_size):
        walls.append(self)
        self.rect = pygame.Rect(pos[0] * tile_size, pos[1] * tile_size, tile_size, tile_size)

# initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# set up the display
pygame.display.set_caption("Maze")
screenwidth, screenheight = 1000,500
screen = pygame.display.set_mode((screenwidth, screenheight))

clock = pygame.time.Clock()
walls = []

# holds the level layout in a list of strings
level = [
    "WWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                       W",
    "W                       W",
    "WWW    WWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWW",
    "WWW    WWWWWWWWWWWWWWWWWW",
    "WWW                     W",
    "WWW                    EW",
    "WWWWWWWWWWWWWWWWWWWWWWWWW",
]

# calculate the tile size based on the dimensions of the window and the number of rows and columns in the maze
rows = len(level)
columns = len(level[0])
tile_size = min(screenwidth // columns, screenheight // rows)

# Find a starting position for the player that is not within a wall
start_pos = None
for y, row in enumerate(level):
    for x, col in enumerate(row):
        if col == " ":
            start_pos = (x * tile_size + tile_size // 4, y * tile_size + tile_size // 4)
            break
    if start_pos:
        break

# create an instance of AlienAnimation
alien_animation = AlienAnimation(screen)

# create the player object using the animated alien
player = Player(start_pos, tile_size, alien_animation)

# parse the level string above. W = wall, E = exit
for y, row in enumerate(level):
    for x, col in enumerate(row):
        if col == "W":
            Wall((x, y), tile_size)
        if col == "E":
            end_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.move(0, -tile_size)
            elif event.key == pygame.K_s:
                player.move(0, tile_size)
            elif event.key == pygame.K_a:
                player.move(-tile_size, 0)
            elif event.key == pygame.K_d:
                player.move(tile_size, 0)
    # Update the game state
    # No additional updates needed for now since player movement is handled in event handling

    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    # bilt the animated alien onto the screen
    screen.blit(player.animation.playerImg, player.rect)
    pygame.draw.rect(screen, (0, 255, 0), end_rect)  # Drawing the exit
    pygame.display.flip()  # Update the display

    # Cap the frame rate
    clock.tick(60)

pygame.quit()