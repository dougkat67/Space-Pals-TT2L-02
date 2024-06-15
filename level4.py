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
        self.num_collisions = 0  # Track the number of collisions with enemies
        self.heart_images = [heart_image.copy() for _ in range(num_hearts)]  # Copy heart images

    def update(self):
        # update the player's image for animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

    def move(self, dx, dy):
        # calculate the change in position based on grid size
        move_amount_x = dx * self.grid_size
        move_amount_y = dy * self.grid_size
        # update the center coordinates of the alien
        self.rect.centerx += move_amount_x
        self.rect.centery += move_amount_y
        # check for collision and the position
        self.move_single_axis(dx, dy)

      
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
                elif dx < 0: # moving left; hit right side of the wall
                    self.rect.left = wall.rect.right
                elif dy > 0: # moving down; hit top side of the wall
                    self.rect.bottom = wall.rect.top
                elif dy < 0: # moving up; hit bottom side of the wall
                    self.rect.top = wall.rect.bottom



    def collide_with_enemy(self):
        if self.num_collisions < num_hearts:
            # Convert corresponding heart image to black and white
            bw_heart_image = self.heart_images[self.num_collisions].convert()
            bw_heart_image = bw_heart_image.convert_alpha()
            bw_heart_image.fill((128, 128, 128, 255), None, pygame.BLEND_RGB_MULT)
            self.heart_images[self.num_collisions] = bw_heart_image
        self.num_collisions += 1
    
        if self.num_collisions >= num_hearts:
            # End game loop if all hearts are black and white
            running = False  # Assuming 'running' is accessible here


    def draw_hearts(self, screen):
        for i, heart_image in enumerate(self.heart_images):
            screen.blit(heart_image, (heart_position[0] + i * heart_spacing, heart_position[1]))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, grid_size, walls, player, initial_positions):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.walls = walls
        self.player = player
        self.positions = initial_positions
        self.current_position_index = 0
        self.rect.topleft = self.positions[self.current_position_index]
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 0.8  # Adjust this value to control the speed

    def update(self):
        # Move enemy left or right
        self.rect.x += self.direction * self.speed

        # Check collision with walls
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                # If collision with left side of the wall and moving right
                if self.direction == 1 and self.rect.right >= wall.rect.left and self.rect.left < wall.rect.left:
                    self.direction = -1  # Change direction to left
                    self.rect.right = wall.rect.left  # Move back to avoid overlapping
                # If collision with right side of the wall and moving left
                elif self.direction == -1 and self.rect.left <= wall.rect.right and self.rect.right > wall.rect.right:
                    self.direction = 1  # Change direction to right
                    self.rect.left = wall.rect.right  # Move back to avoid overlapping
                    break

        # Check collision with player
        if self.rect.colliderect(self.player.rect):
            self.player.collide_with_enemy()

        # Update current position index if enemy reaches the end of the path
        if self.rect.x < min(self.positions, key=lambda x: x[0])[0] or self.rect.x > max(self.positions, key=lambda x: x[0])[0]:
            self.current_position_index = (self.current_position_index + 1) % len(self.positions)
            self.rect.topleft = self.positions[self.current_position_index]




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
    pygame.transform.scale(pygame.image.load('images/alien3_0.png'), (25, 25)),
    pygame.transform.scale(pygame.image.load('images/alien3_1.png'), (25, 25)),
    pygame.transform.scale(pygame.image.load('images/alien3_2.png'), (25, 25)),
    pygame.transform.scale(pygame.image.load('images/alien3_3.png'), (25, 25))
    ]

clock = pygame.time.Clock()
walls = [] # list to hold the walls

grid_cell_size = 25


heart_image = pygame.image.load('images/heart.png')

coin_images = [

    pygame.transform.scale(pygame.image.load('images/coin_0.png'), (20, 20)),
    pygame.transform.scale(pygame.image.load('images/coin_1.png'), (20, 20)),
    pygame.transform.scale(pygame.image.load('images/coin_2.png'), (20, 20)),
    pygame.transform.scale(pygame.image.load('images/coin_3.png'), (20, 20)),
    pygame.transform.scale(pygame.image.load('images/coin_4.png'), (20, 20)),
    pygame.transform.scale(pygame.image.load('images/coin_5.png'), (20, 20))
    ]

coins = [Coin(grid_cell_size, (x, y), coin_images) for x in range(0, screen_width, grid_cell_size) for y in range(0, screen_height, grid_cell_size)]


spaceship_image = pygame.transform.scale(pygame.image.load('images/spaceship.png'), (50, 28))

# holds the level layout in a list of strings

# 40x20 (25pixels per grid cell)
level2 = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                      W",
    "W WWWWWWWWWW  WWWW  WWWWWW  WWWWWWWWWW W",
    "W W                      W  W W      W W",
    "W W WWWW  WWWWWWWWWWWW  WW WW W    W W W",
    "W W W           W        W  W W WW W   W",
    "W W W WWWWWWWWW W WWWW   W  W   W  WWW W",
    "W W W W         W WE W W        W    W W",
    "W     W W  WWW  W W  W WW WWWWWWWWWW W W",
    "W   W W WW             W       W     W W",
    "W W   W  W  WWW  WWWWWWWWWWWWW W WWWWW W",
    "W W W WW                 W   W W   W   W",
    "WWW W    WWWW  WWW  W  W    WW   W W W W",
    "W W WW W WW      W WW WWWWW W  WWW W W W",
    "W W    W    W  W W  W          W     W W",
    "W WW  WWWWWWW  WWWWWWWW  WWWWWWWW  WWW W",
    "W                                      W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",

]

# Calculate the size of each grid cell based on the screen dimensions and number of cells
num_cols = len(level2[0])
num_rows = len(level2)
grid_cell_size = 25
screen_width = num_cols * grid_cell_size
screen_height = num_rows * grid_cell_size
end_rect = None

# Parse the level string above. W = wall, E = exit
for y, row in enumerate(level2):
    for x, col in enumerate(row):
        if col == "W":
            Wall((x * grid_cell_size, y * grid_cell_size))
        if col == "E":
            end_rect = pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size)
            pygame.draw.rect(screen, (255, 165, 0), end_rect) # Draw the exit

font = pygame.font.Font(None, 36)
attempt = 1
attempt_text = font.render(f"Attempt: {attempt}/3", True, (255, 255, 255))
attempt_text_rect = attempt_text.get_rect(center = (screen_width // 2, 25))
screen.blit(attempt_text, attempt_text_rect)

num_hearts = 3
heart_spacing = 40
heart_position = (10, 10)

# create coins at specific positions (20 coins in every level)
coins = [Coin(grid_cell_size,(1, 6), coin_images),
         Coin(grid_cell_size,(1, 17), coin_images),
         Coin(grid_cell_size, (3, 14), coin_images),
         Coin(grid_cell_size,(4, 10), coin_images),
         Coin(grid_cell_size,(7, 3), coin_images),
         Coin(grid_cell_size, (9, 13), coin_images),
         Coin(grid_cell_size, (10, 7), coin_images),
         Coin(grid_cell_size, (13, 9), coin_images),
         Coin(grid_cell_size, (11, 15), coin_images),
         Coin(grid_cell_size, (16, 3), coin_images),
         Coin(grid_cell_size, (20, 10), coin_images),
         Coin(grid_cell_size, (18, 16), coin_images),
         Coin(grid_cell_size, (21, 16), coin_images),
         Coin(grid_cell_size, (23, 18), coin_images),
         Coin(grid_cell_size, (29, 9), coin_images),
         Coin(grid_cell_size, (31, 14), coin_images),
         Coin(grid_cell_size, (34, 11), coin_images),
         Coin(grid_cell_size, (34, 17), coin_images),
         Coin(grid_cell_size, (36, 5), coin_images),
         Coin(grid_cell_size,(38, 3), coin_images),
         ]
coin_positions = [(1, 6), (1, 17), (3, 14), (4, 10), (7, 3), 
                  (9, 13), (10, 7), (13, 9), (11, 15), (16, 3), 
                  (20, 10), (18, 16), (21, 16), (23, 18), (29, 9),
                  (31, 14), (36, 5), (34, 17), (34, 6), (38, 3)
                  ]
def reset_coins(coin_positions):
    global coins
    coins = [Coin(grid_cell_size, pos, coin_images) for pos in coin_positions]


# set up the alien sprite
grid_cell_size = 25
player_initial_position = (1 * grid_cell_size, 3 * grid_cell_size)


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


# alien's initial position
initial_grid_x = 3
initial_grid_y = 4
player_initial_position = (initial_grid_x * grid_cell_size, initial_grid_y * grid_cell_size)
player = Player(alien_images, grid_cell_size, animation_speed=0.9, initial_position=player_initial_position)  # Create the player with adjusted initial position

# set up the alien sprite
player = Player(alien_images, grid_cell_size, initial_position=player_initial_position)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


enemy_image = pygame.transform.scale(pygame.image.load('images/enemy.png'),(42, 22))
enemy_initial_position = [(3 * grid_cell_size, 19 * grid_cell_size), (35 * grid_cell_size, 18 * grid_cell_size),
                          (3 * grid_cell_size, 5 * grid_cell_size), (24 * grid_cell_size, 5 * grid_cell_size)]
enemy = Enemy(enemy_image, grid_cell_size, walls, player, enemy_initial_position)
all_sprites.add(enemy)


# variables to track collected coins
collected_coins = 0
total_coins = len(coins)
# font type for displaying collected points
font = pygame.font.Font(None, 36)
# load the coin image
coin_image = pygame.image.load('images/coin_0.png')

# initialize variables for the timer
time_limit = 30 # ? seconds
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
initial_time = 30
start_time = pygame.time.get_ticks() // 1000 # current time in seconds

while running and attempt <= num_hearts:
    # Calculate delta time
    dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
    current_time += dt

    # Handle events

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
                player.move(1, 0)  # Move right
            elif pressed_keys[pygame.K_w]:
                player.move(0, -1)  # Move up
            elif pressed_keys[pygame.K_s]:
                player.move(0, 1)  # Move down

    # Check for collision with the exit
    if end_rect is not None and player.rect.colliderect(end_rect):
        player_won = True
        running = False

    # Check for collision with coins and collect them
    for coin in coins:
        if player.rect.colliderect(coin.rect):
            collected_coins += coin.collect()
            coins.remove(coin)

    # Update all sprites
    all_sprites.update()
    enemy.update()

    # fill the screen with background color
    screen.fill((173, 216, 230))

    # draw walls, exit, player, and coins
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 0), wall.rect)
    if end_rect is not None:
        screen.blit(spaceship_image, end_rect)
        screen.blit(player.image, player.rect)
    for coin in coins:
        coin.update(dt)
        screen.blit(coin.image, coin.rect)

    # display enemy
    screen.blit(enemy.image, enemy.rect)

    # display attempt text
    screen.blit(attempt_text, attempt_text_rect)

    # display collected coins count
    screen.blit(coin_image, coin_position)
    collected_text = font.render(f"Collected: {collected_coins:02d}/{total_coins}", True, (255, 255, 255))
    screen.blit(collected_text, (screen_width - collected_text.get_width() - 10, 10))

    # display remaining time
    remaining_time = max(time_limit - current_time, 0)
    timer_text = timer_font.render(f"Time: {int(remaining_time)}", True, (255, 255, 255))
    screen.blit(timer_text, timer_text_rect)

    # display end game messages if conditions are met
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

    # check end game conditions
    if time_up and not player_won:
        attempt += 1
        if attempt <= num_hearts:
            # reset game state for next attempt
            player.rect.topleft = player_initial_position
            current_time = 0
            time_up = False
            collected_coins = 0
            # update attempt text for the next attempt
            attempt_text = font.render(f"Attempt: {attempt}/3", True, (255, 255, 255))
            screen.blit(attempt_text, attempt_text_rect)
            reset_coins(coin_positions)
        else:
            running = False  # Player loses if hearts are exhausted

    if player_won or attempt > num_hearts:
        running = False  # End game if player won or attempted 3 times

    player.draw_hearts(screen)
    
    # update display
    pygame.display.flip()

    # cap the frame rate
    clock.tick(60)

# Quit Pygame
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