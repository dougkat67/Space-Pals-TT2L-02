import os
import random
import pygame
from collecting_coins import Coin

class Player(pygame.sprite.Sprite):
    def __init__(self, images, grid_size, walls, enemies, animation_speed=0.2, initial_position=(0, 0)):
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
        self.walls = walls
        self.enemies = enemies
        self.num_collisions = 0  # Track the number of collisions with enemies
        self.hearts_left = 3

    def update(self):
        # update the player's image for animation
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

        collided_enemies = pygame.sprite.spritecollide(self, self.enemies, False)
        for enemy in collided_enemies:
            self.collide_with_enemy(enemy)
            return True
        
        return False

    def move(self, dx, dy):
        # calculate the change in position based on grid size
        move_amount_x = dx * self.grid_size
        move_amount_y = dy * self.grid_size
        # update the center coordinates of the alien
        self.rect.centerx += move_amount_x
        self.rect.centery += move_amount_y
        # check for collision and the position
        self.move_single_axis(dx, dy)

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


    def collide_with_enemy(self, enemy):
         if self.num_collisions == 0:
           self.hearts_left -= 1
           self.num_collisions += 1



class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, grid_size, walls, player, initial_positions):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.grid_size = grid_size
        self.walls = walls
        self.player = player
        self.enemies = enemies
        self.positions = initial_positions
        self.current_position_index = 0
        self.rect.topleft = self.positions[self.current_position_index]
        self.direction = 1 # 1 for right, -1 for left
        self.vertical_direction = 0
        self.speed = 2.0 
        self.vertical_speed = 1.0 
        
    def update(self):
        # Move enemy left or right
        self.rect.x += self.direction* self.speed

        # Check collision with walls
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if self.direction > 0 and self.rect.right >= wall.rect.left:
                    self.direction = -1
                    self.rect.right = wall.rect.left
                elif self.direction < 0 and self.rect.left <= wall.rect.right:
                    self.direction = 1
                    self.rect.left = wall.rect.right


        self.rect.y += self.vertical_direction* self.vertical_speed

        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if self.vertical_direction > 0 and self.rect.bottom >= wall.rect.top:
                    self.vertical_direction = -1
                    self.rect.bottom = wall.rect.top
                elif self.vertical_direction < 0 and self.rect.top <= wall.rect.bottom:
                    self.vertical_direction = 1
                    self.rect.top = wall.rect.bottom

        # Check collision with player
        if self.rect.colliderect(self.player.rect):
            self.player.collide_with_enemy(self)
            self.player.num_collisions = 0
            return True


        # Update current position index if enemy reaches the end of the path
        if (self.rect.x < min(self.positions, key=lambda x: x[0])[0] or self.rect.x > max(self.positions, key=lambda x: x[0])[0] or
           self.rect.y < min(self.positions, key=lambda x: x[1])[1] or self.rect.y > max(self.positions, key=lambda x: x[1])[1]):
            self.current_position_index = (self.current_position_index + 1) % len(self.positions)
            self.rect.topleft = self.positions[self.current_position_index]
        return False
        
class Wall(object):
    def __init__(self, pos):
        super().__init__()
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], grid_cell_size, grid_cell_size)

# initialise pygame
pygame.init()

# set up the display
pygame.display.set_caption("Maze")
screen_width, screen_height = 1000, 500
screen = pygame.display.set_mode((screen_width, screen_height))

alien_images = [
    pygame.transform.scale(pygame.image.load('images/alien4_1.png'), (25, 25)),
    pygame.transform.scale(pygame.image.load('images/alien4_2.png'), (25, 25)),
    pygame.transform.scale(pygame.image.load('images/alien4_3.png'), (25, 25)),
    pygame.transform.scale(pygame.image.load('images/alien4_4.png'), (25, 25))
    ]

clock = pygame.time.Clock()
walls = [] # list to hold the walls
grid_cell_size = 25

heart= pygame.image.load('images/heart.png')
heart_rect = heart.get_rect()
hearts_left = 3
mortality = True

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
level4 = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W                                      W",
    "W WWWWWWWWWW  WWWW  WWWWWW  WWWWWWWWWW W",
    "W W                      W  W W      W W",
    "W W WWWW  WWWWWWWWWWWW  WW WW W    W   W",
    "W W W           W        W  W W WW W   W",
    "W W W WWWWWWWW  W WWWW   W  W   W  WWW W",
    "W W W W         W WE W W        W    W W",
    "W     W W  WWW  W W  W WW WWWWWWWWWW W W",
    "W     W WW             W       W     W W",
    "W W   W  W  WWW  WWWWWWWWWWWWW W WWWWW W",
    "W W W WW                 W   W W   W   W",
    "WWW W    WWWW  WWW  W  W    WW   W W   W",
    "W W WW W WW      W WW WWWWW W  WWW W W W",
    "W W    W    W  W W  W          W     W W",
    "W WW  WWWWWWW  WWWWWWWW  WWWWWWWW  WWW W",
    "W                                      W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",

]

# Calculate the size of each grid cell based on the screen dimensions and number of cells
num_cols = len(level4[0])
num_rows = len(level4)
grid_cell_size = 25
screen_width = num_cols * grid_cell_size
screen_height = num_rows * grid_cell_size
end_rect = None

# Parse the level string above. W = wall, E = exit
for y, row in enumerate(level4):
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
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
grid_cell_size = 25
player_initial_position = (1 * grid_cell_size, 3 * grid_cell_size)

player = Player(alien_images, grid_cell_size, walls, enemies, initial_position=player_initial_position)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)


# Calculate the size of each grid cell based on the screen dimensions and number of cells
num_cols = len(level4[0])
num_rows = len(level4)
max_grid_width = screen_width // num_cols
max_grid_height = screen_height // num_rows
grid_cell_size = min(max_grid_width, max_grid_height)

# Recalculate screen dimensions based on adjusted grid cell size 
screen_width = num_cols * grid_cell_size
screen_height = num_rows * grid_cell_size

# Parse the level string above. W = wall, E = exit  
for y, row in enumerate(level4):
    for x, col in enumerate(row):
        if col == "W":
            Wall((x * grid_cell_size, y * grid_cell_size))
        if col == "E":
            end_rect = pygame.Rect(x * grid_cell_size, y * grid_cell_size, grid_cell_size, grid_cell_size)
            pygame.draw.rect(screen, (255, 165, 0), end_rect) # Draw the exit

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

enemy_image = pygame.transform.scale(pygame.image.load('images/enemy.png'),(42, 22))
enemy1_initial_position = [(3 * grid_cell_size, 18 * grid_cell_size), (35 * grid_cell_size, 18 * grid_cell_size)]
enemy2_initial_position = [(3 * grid_cell_size, 5 * grid_cell_size), (24 * grid_cell_size, 5 * grid_cell_size)] 
enemy3_initial_position = [(9 * grid_cell_size, 13 * grid_cell_size), (23 * grid_cell_size, 13 * grid_cell_size)]                        
                          
enemy1 = Enemy(enemy_image, grid_cell_size, walls, player, enemy1_initial_position)
enemy2 = Enemy(enemy_image, grid_cell_size, walls, player, enemy2_initial_position)
enemy3 = Enemy(enemy_image, grid_cell_size, walls, player, enemy3_initial_position)
all_sprites.add(enemy1)
all_sprites.add(enemy2)
all_sprites.add(enemy3)

# Add enemies and player to sprite groups
enemies.add(enemy1, enemy2, enemy3)
all_sprites.add(player, enemy1, enemy2, enemy3)
 
# variables to track collected coins
collected_coins = 0
total_coins = len(coins)
# font type for displaying collected points
font = pygame.font.Font(None, 36)
# load the coin image
coin_image = pygame.image.load('images/coin_0.png')

# initialize variables for the timer

time_limit = 40 # ? seconds

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
initial_time = 30 # initial time(30 seconds)
start_time = pygame.time.get_ticks() // 1000 # current time in seconds

while running and attempt <= hearts_left:
    # calculate delta time
    dt = clock.tick(60) / 1000.0 # convert milliseconds to seconds
    current_time += dt

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
    player.update()

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

    if hearts_left == 3:
            screen.blit(heart,(20,10))
            screen.blit(heart,(60,10))
            screen.blit(heart,(100,10))
    elif hearts_left == 2:
            screen.blit(heart,(20,10))
            screen.blit(heart,(60,10))
    elif hearts_left == 1:
            screen.blit(heart,(20,10))

    if player.update():
        player.collide_with_enemy()
        hearts_left -= 1

    # display enemy
    screen.blit(enemy1.image, enemy1.rect)
    screen.blit(enemy2.image, enemy2.rect)
    screen.blit(enemy3.image, enemy3.rect)

    # display attempt text
    screen.blit(attempt_text, attempt_text_rect)

    # display collected coins count
    screen.blit(coin_image, coin_position)
    collected_text = font.render(f"Collected: {collected_coins}/{total_coins}", True, (255, 255, 255))
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
        if attempt <= hearts_left:
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

    if player_won or attempt > hearts_left:
        running = False  # End game if player won or attempted 3 times

    all_sprites.draw(screen)

    pygame.display.flip()
   
    clock.tick(60)

pygame.quit()