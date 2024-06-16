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

spaceship_image = pygame.transform.scale(pygame.image.load('images/spaceship.png'), (60, 35))

# holds the level layout in a list of strings
# use 20walls/row, 10walls/column
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWW",
    "W       W   WWWWWWWW",
    "WWW  WWWWW  WWWWWWWW",
    "W           WWWW   W",
    "WWWWW              W",
    "W   W WWW        W W",
    "W W W WWW  WWWW  W W",
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

font = pygame.font.Font(None, 36)
attempt = 1
attempt_text = font.render(f"Attempt : {attempt}/3", True, (255, 255, 255))
attempt_text_rect = attempt_text.get_rect(center = (screen_width // 2, 25))
screen.blit(attempt_text, attempt_text_rect)

num_hearts = 3
heart_spacing = 40
heart_position = (10, 10)
def display_hearts(attempt):
    for i in range(num_hearts):
        if attempt == 1:
            screen.blit(heart_image, (heart_position[0] + i * heart_spacing, heart_position[1]))
        elif attempt == 2:
            if i < 2:
                screen.blit(heart_image, (heart_position[0] + i * heart_spacing, heart_position[1]))
            else:
                # Convert the heart image to black and white
                bw_heart_image = heart_image.convert()
                bw_heart_image = bw_heart_image.convert_alpha()
                bw_heart_image.fill((128, 128, 128, 255), None, pygame.BLEND_RGB_MULT)
                screen.blit(bw_heart_image, (heart_position[0] + i * heart_spacing, heart_position[1]))
        elif attempt == 3:
            if i == 0:
                screen.blit(heart_image, (heart_position[0] + i * heart_spacing, heart_position[1]))
            else:
                # Convert the heart image to black and white
                bw_heart_image = heart_image.convert()
                bw_heart_image = bw_heart_image.convert_alpha()
                bw_heart_image.fill((128, 128, 128, 255), None, pygame.BLEND_RGB_MULT)
                screen.blit(bw_heart_image, (heart_position[0] + i * heart_spacing, heart_position[1]))

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
coin_positions = [(2, 2), (7, 2), (9, 2), (11, 2), (4, 3), 
                  (1, 4), (5, 4), (10, 4), (18, 4), (16, 4), 
                  (7, 5), (3, 6), (9, 6), (13, 6), (15, 7), (18, 7), 
                  (1, 8), (3, 8), (5, 8), (10, 8)
                  ]
def reset_coins(coin_positions):
    global coins
    coins = [Coin(grid_cell_size, pos, coin_images) for pos in coin_positions]


# alien's initial position
initial_grid_x = 1
initial_grid_y = 2
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

timer_text = timer_font.render("", True, (255, 255, 255))
collected_text = font.render("", True, (255, 255, 255))
coin_position = (765, 6)
timer_text_rect = timer_text.get_rect(topright=(screen_width - 130, 10 + collected_text.get_height() + 5))

running = True
initial_time = 10 
start_time = pygame.time.get_ticks() // 1000 # current time in seconds

while running and attempt <= num_hearts:
    # Calculate delta time
    dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
    current_time += dt

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_a]:
                player.move(-1, 0)  # Move left
            elif pressed_keys[pygame.K_d]:
                player.move(1, 0)  # Move right
            elif pressed_keys[pygame.K_w]:
                player.move(0, -1)  # Move up
            elif pressed_keys[pygame.K_s]:
                player.move(0, 1)  # Move down

    # Check for collision with the exit
    if player.rect.colliderect(end_rect):
        player_won = True
        running = False

    # Check for collision with coins and collect them
    for coin in coins:
        if player.rect.colliderect(coin.rect):
            collected_coins += coin.collect()
            coins.remove(coin)

    # Update all sprites
    all_sprites.update()

    # Fill the screen with background color
    screen.fill((173, 216, 230))

    # Draw walls, exit, player, and coins
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall.rect)
    screen.blit(spaceship_image, end_rect)
    screen.blit(player.image, player.rect)
    for coin in coins:
        coin.update(dt)
        screen.blit(coin.image, coin.rect)

    # Display attempt text
    screen.blit(attempt_text, attempt_text_rect)

    # Display collected coins count
    screen.blit(coin_image, coin_position)
    collected_text = font.render(f"Collected: {collected_coins:02d}/{total_coins}", True, (255, 255, 255))
    screen.blit(collected_text, (screen_width - collected_text.get_width() - 10, 10))

    # Display remaining time
    remaining_time = max(time_limit - current_time, 0)
    timer_text = timer_font.render(f"Time: {int(remaining_time)}", True, (255, 255, 255))
    screen.blit(timer_text, timer_text_rect)

    # Display end game messages if conditions are met
    if time_up and not player_won:
        message_color = (255, 0, 0)  # Red for time's up
        message_text = "Time's up!"
    elif player_won:
        message_color = (0, 255, 0)  # Green for win message
        message_text = "You win!"

    if time_up or player_won:
        end_text = pygame.font.Font(None, end_message_font_size).render(message_text, True, message_color)
        end_text_rect = end_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(end_text, end_text_rect)

    # check if time is up
    if current_time >= time_limit:
        time_up = True

    # Check end game conditions
    if time_up and not player_won:
        attempt += 1
        if attempt <= num_hearts:
            # reset game state for next attempt
            player.rect.topleft = player_initial_position
            current_time = 0
            time_up = False
            collected_coins = 0
            # update attempt text for the next attempt
            attempt_text = font.render(f"Attempt : {attempt}", True, (255, 255, 255))
            screen.blit(attempt_text, attempt_text_rect)
            reset_coins(coin_positions)
        else:
            running = False  # Player loses if hearts are exhausted

    if player_won or attempt > num_hearts:
        running = False  # End game if player won or attempted 3 times

    # Display hearts for attempts
    display_hearts(attempt)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()