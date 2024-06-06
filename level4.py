import os 
import random 
import pygame
from collecting_coins import Coin

# class the orange dude
class Player(pygame.sprite.Sprite):
    def __init__(self, images, grid_size, animation_speed=0.2, initial_position=(0, 0)):
        super().__init__()
        if isinstance(images, list):
            self.images = images
        else:
            self.images = [images] # ensure images is always treated as a list
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.animation_speed = animation_speed
        self.animation_timer = 0
        # ensure initial_position is a tuple
        self.rect = self.image.get_rect(topleft=initial_position if isinstance(initial_position, tuple) else (0, 0))
        self.grid_size = grid_size

    def update(self):
        # update the player's image for animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def move(self, dx, dy):
        # move the player
        self.rect.x += dx * self.grid_size
        self.rect.y += dy * self.grid_size

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

alien_images = [
    pygame.transform.scale(pygame.image.load('images/alien_0.png'), (45, 45)),
    pygame.transform.scale(pygame.image.load('images/alien_1.png'), (45, 45)),
    pygame.transform.scale(pygame.image.load('images/alien_2.png'), (45, 45)),
    pygame.transform.scale(pygame.image.load('images/alien_3.png'), (45, 45))
    ]

clock = pygame.time.Clock()
walls = [] # list to hold the walls
grid_cell_size = 50

heart_image = pygame.image.load('images/heart.png')

coin_images = [
    pygame.image.load('images/coin_0.png'),
    pygame.image.load('images/coin_1.png'),
    pygame.image.load('images/coin_2.png'),
    pygame.image.load('images/coin_3.png'),
    pygame.image.load('images/coin_4.png'),
    pygame.image.load('images/coin_5.png')
    ]

coins = [Coin(grid_cell_size, (x, y), coin_images) for x in range(0, screen_width, grid_cell_size) for y in range(0, screen_height, grid_cell_size)]

spaceship_image = pygame.transform.scale(pygame.image.load('images/spaceship.png'), (grid_cell_size, grid_cell_size))

# holds the level layout in a list of strings
# use 20walls/row, 10walls/column
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W                  W",
    "W WWWW WWWW WWWW   W",
    "W W  W W  W W  W W W",
    "W W  W W  W W  W W W",
    "W    W    W    W   W",
    "W WWWW WWWW WWWW W W",
    "W                  W",
    "W WWWW WWWW WWWW W W",
    "W W  W W  W W  W W W",
    "W W  W W  W W  W W W",
    "W    W    W    W   W",
    "W WWWW WWWW WWWW W W",
    "W                  W",
    "W WWWW WWWW WWWW W W",
    "W W  W W  W W  W W W",
    "W W  W W  W W  W W W",
    "W    W    W    W   W",
    "W WWWW WWWW WWWW E W",
    "WWWWWWWWWWWWWWWWWWWW",
]

# Calculate the size of each grid cell based on the screen dimensions and number of cells
num_cols = len(level[0])
num_rows = len(level)
max_grid_width = screen_width // num_cols
max_grid_height = screen_height // num_rows
grid_cell_size = min(max_grid_width, max_grid_height)

# Recalculate screen dimensions based on adjusted grid cell size / OLD version
#screen_width = num_cols * grid_cell_size
#screen_height = num_rows * grid_cell_size

# Calculate the starting coordinates to center the maze  / #NEW version
start_x = (screen_width - num_cols * grid_cell_size) // 2
start_y = (screen_height - num_rows * grid_cell_size) // 2

# Parse the level string above. W = wall, E = exit  / OLD version
# for y, row in enumerate(level):
#     for x, col in enumerate(row):
#         if col == "W":
#             Wall((x * grid_cell_size, y * grid_cell_size))
#         if col == "E":
#             end_rect = pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size)
#             pygame.draw.rect(screen, (255, 165, 0), end_rect) # Draw the exit
            

# Parse the level string above. W = wall, E = exit / NEW version
for y, row in enumerate(level):
    for x, col in enumerate(row):
        if col == "W":
            Wall((start_x + x * grid_cell_size, start_y + y * grid_cell_size))
        if col == "E":
            end_rect = pygame.Rect(start_x + x * grid_cell_size, start_y + y * grid_cell_size, grid_cell_size, grid_cell_size)

num_hearts = 3
heart_spacing = 40
heart_position = (screen_width // 2 - heart_spacing, 15)
def display_hearts():
    for i in range(num_hearts):
        screen.blit(heart_image, (heart_position[0] + i * heart_spacing, heart_position[1]))

# create coins at specific positions (20 coins in every level)
coins = [Coin(grid_cell_size,(2, 2), coin_images),
         Coin(grid_cell_size,(7, 2), coin_images),
         Coin(grid_cell_size, (9, 2), coin_images),
         Coin(grid_cell_size,(11, 2), coin_images),
         Coin(grid_cell_size,(4, 3), coin_images),
         Coin(grid_cell_size, (1, 4), coin_images),
         Coin(grid_cell_size, (5, 4), coin_images),
         Coin(grid_cell_size, (10, 4), coin_images),
         Coin(grid_cell_size, (18, 4), coin_images),
         Coin(grid_cell_size, (16, 4), coin_images),
         Coin(grid_cell_size, (7, 5), coin_images),
         Coin(grid_cell_size, (3, 6), coin_images),
         Coin(grid_cell_size, (9, 6), coin_images),
         Coin(grid_cell_size, (13, 6), coin_images),
         Coin(grid_cell_size, (15, 7), coin_images),
         Coin(grid_cell_size, (18, 7), coin_images),
         Coin(grid_cell_size, (1, 8), coin_images),
         Coin(grid_cell_size, (3, 8), coin_images),
         Coin(grid_cell_size, (5, 8), coin_images),
         Coin(grid_cell_size,(10, 8), coin_images),
         ]

# alien's initial position
initial_grid_x = 3
initial_grid_y = 4
player_initial_position = (initial_grid_x * grid_cell_size, initial_grid_y * grid_cell_size)
player = Player(alien_images, grid_cell_size, animation_speed=0.9, initial_position=player_initial_position)  # Create the player with adjusted initial position

# set up the alien sprite
grid_cell_size = 50
player_initial_position = (1 * grid_cell_size, 2 * grid_cell_size)
player = Player(alien_images, grid_cell_size, initial_position=player_initial_position)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# variables to track collected coins
collected_coins = 0
total_coins = len(coins)
# font type for displaying collected points
font = pygame.font.Font(None, 36)
# load the coin image
coin_image = pygame.image.load('images/coin_0.png')

# initialize variables for the timer
time_limit = 10 # 10 seconds
current_time = 0
timer_font = pygame.font.Font(None, 36)

# add variables to track game and conditions
player_won = False
time_up = False

end_message_font_size = 188
end_message_duration = 3000  # 3 seconds in milliseconds
end_message_display_time = 0  # Variable to track how long the end message has been displayed
end_message_font = pygame.font.Font(None, end_message_font_size)

running = True
initial_time = 10 # initial time(30 seconds)
start_time = pygame.time.get_ticks() // 1000 # current time in seconds
while running:
    # calculate delta time
    dt = clock.tick(60) / 1000.0 # convert milliseconds to seconds
    current_time += dt

    # check if the timer has reached the time limit
    if current_time >= time_limit:
        time_up = True
        running = False

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
        player_won = True
        running = False

    # check for collision with coins
    for coin in coins:
        if player.rect.colliderect(coin.rect):
            collected_coins += coin.collect()
            coins = [c for c in coins if c is not coin] # remove collected coin from the list

    # update all sprites
    all_sprites.update()

    # fill the screen with bg image
    screen.fill((173, 216, 230))

    # draw all sprites
    all_sprites.draw(screen)

    # draw the walls
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall.rect)

    # draw the exit
    screen.blit(spaceship_image, end_rect)

    # draw the player
    screen.blit(player.image, player.rect)
    for coin in coins:
        coin.update(dt) # update coin animation
        screen.blit(coin.image, coin.rect) # render coin image on screen

    # display collected coins using coin image
    coin_position = (10, 10)
    screen.blit(coin_image, coin_position)

    # display collected coins at the top left corner
    collected_text = font.render(f"Collected: {collected_coins}/{total_coins}", True, (255, 255, 255))
    screen.blit(collected_text, (50,10))

    # Display timer text
    # calculate remaining time
    remaining_time = max(time_limit - current_time, 0)
    timer_text = timer_font.render(f"Time: {int(remaining_time)}", True, (255, 255, 255))
    timer_text_rect = timer_text.get_rect(topright=(screen_width - 10, 10))
    screen.blit(timer_text, timer_text_rect)

    # Display end game messages if conditions are met
    if time_up and not player_won:
        end_text = pygame.font.Font(None, end_message_font_size).render("Time's up!", True, (255, 0, 0))  # Red color for time's up message
        end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(end_text, end_text_rect)
    elif player_won:
        end_text = pygame.font.Font(None, end_message_font_size).render("You win!", True, (0, 255, 0))  # Green color for you win message
        end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(end_text, end_text_rect)

    display_hearts()
    # display end game messages if conditions are met
    if time_up and not player_won:
        end_text = pygame.font.Font(None, end_message_font_size).render("Time's up!", True, (255, 0, 0))  # Red color for time's up message
        end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(end_text, end_text_rect)
    elif player_won:
        end_text = pygame.font.Font(None, end_message_font_size).render("You win!", True, (0, 255, 0))  # Green color for you win message
        end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(end_text, end_text_rect)

    # update the display
    pygame.display.flip()

    # Check if an end game message is being displayed
    if (time_up and not player_won) or player_won:
        # Get the current time
        current_time = pygame.time.get_ticks()

        # Check if the end message has been displayed for the desired duration
        if current_time - end_message_display_time >= end_message_duration:
            running = False  # Exit the game loop and quit the game

    # cap the frame rate
    clock.tick(60)

pygame.quit()