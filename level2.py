import sys
import pygame
from collecting_coins import Coin
from states.state import State

class Level2(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.walls = []  # list to hold the walls
        self.grid_cell_size = 25
        self.health = Health(game)
        

        # Load images with error handling
        try:
            self.heart_image = pygame.image.load('images/heart.png')
            self.coin_images = [
                pygame.image.load('images/coin_0.png'),
                pygame.image.load('images/coin_1.png'),
                pygame.image.load('images/coin_2.png'),
                pygame.image.load('images/coin_3.png'),
                pygame.image.load('images/coin_4.png'),
                pygame.image.load('images/coin_5.png')
            ]

            self.spaceship_image = pygame.transform.scale(pygame.image.load('images/spaceship.png'), (60, 35))

            self.alien_images = [
                pygame.transform.scale(pygame.image.load('images/alien_0.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load('images/alien_1.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load('images/alien_2.png'), (45, 45)),
                pygame.transform.scale(pygame.image.load('images/alien_3.png'), (45, 45))
            ]
        except pygame.error as e:
            print(f"Error loading image: {e}")
            sys.exit(1)

        self.level2 = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W  W                     W             W",
            "W  W                     W             W",
            "W  W  WWWWWW   WWWWWWWW  W  WWWWWWWWW  W",
            "W        W            W  W          W  W",
            "W        W            W  W          W  W",
            "WWWWWWW  W  WWWW   W  W  WW  WW  W  W  W",
            "W     W  W  W      W  W       W  W  W  W",
            "W     W  W  W      W  W       W  W  W  W",
            "W  W  W  W  W  W   W          W  W     W",
            "W  W  W  W  W  W   W          W  W     W",
            "W  W  W  W  W  W  WWWWWWWWWWWWW  WWWWWWW",
            "W  W        W  W  W                    W",
            "W  W        W  W  W                    W",
            "W  WWWWWWW  W  W  W  W   WWWWWWWWWWWWWWW",
            "W           W  W     W             E   W",
            "W           W  W     W                 W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

        self.num_cols = len(self.level2[0])
        self.num_rows = len(self.level2)
        self.grid_cell_size = 25
        self.screen_width = self.num_cols * self.grid_cell_size
        self.screen_height = self.num_rows * self.grid_cell_size

        self.font = pygame.font.Font(None, 36)
        self.attempt = 1
        self.attempt_text = self.font.render(f"Attempt : {self.attempt}/3", True, (255, 255, 255))
        self.attempt_text_rect = self.attempt_text.get_rect(center=(self.screen_width // 2, 25))

        self.coin_positions = [(1, 6), (1, 17), (4, 14), (4, 9), (7, 3), 
                  (9, 14), (10, 7), (13, 9), (13, 15), (16, 3), 
                  (20, 14), (20, 11), (22, 17), (23, 6), (29, 9),
                  (31, 14), (34, 11), (34, 17), (34, 6), (37, 3)
                  ]
        
        self.reset_coins()

        self.player_initial_position = (1 * self.grid_cell_size, 3 * self.grid_cell_size)
        self.player = Player(self.alien_images, self.grid_cell_size, self.walls, initial_position = self.player_initial_position)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.enemy_image = pygame.transform.scale(pygame.image.load('images/enemy.png'),(67.75, 38.75))
        enemy_initial_position = [(38 * self.grid_cell_size, 14 * self.grid_cell_size), (5 * self.grid_cell_size, 3 * self.grid_cell_size)]
        enemy = Enemies(self.enemy_image, self.grid_cell_size, self.walls, self.player, enemy_initial_position)
        self.all_sprites.add(enemy)
        
        self.num_collisions= 0
        self.hearts_left = 3

        self.collected_coins = 0
        self.total_coins = len(self.coins)
        self.coin_image = pygame.image.load('images/coin_0.png')

        self.time_limit = 25  
        self.current_time = 0
        self.timer_font = pygame.font.Font(None, 36)

        self.player_won = False
        self.time_up = False

        self.end_message_font_size = 188
        self.end_message_duration = 3000  # 3 seconds in milliseconds
        self.end_message_display_time = 0  # Variable to track how long the end message has been displayed
        self.end_message_font = pygame.font.Font(None, self.end_message_font_size)

        self.timer_text = self.timer_font.render("", True, (255, 255, 255))
        self.collected_text = self.font.render("", True, (255, 255, 255))
        self.coin_position = (765, 6)
        self.timer_text_rect = self.timer_text.get_rect(topright=(self.screen_width - 130, 10 + self.collected_text.get_height() + 5))

        self.start_time = pygame.time.get_ticks() // 1000  # current time in seconds

        self.parse_level()

    def parse_level(self):
        for y, row in enumerate(self.level2):
            for x, col in enumerate(row):
                if col == "W":
                    Wall((x * self.grid_cell_size, y * self.grid_cell_size), self.walls, self.grid_cell_size)
                if col == "E":
                    self.end_rect = pygame.Rect(x * self.grid_cell_size, y * self.grid_cell_size, self.grid_cell_size, self.grid_cell_size)

    def reset_coins(self):
        self.coins = [Coin(self.grid_cell_size, pos, self.coin_images) for pos in self.coin_positions]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.move(-1, 0)  # Move left
                elif event.key == pygame.K_d:
                    self.player.move(1, 0)  # Move right
                elif event.key == pygame.K_w:
                    self.player.move(0, -1)  # Move up
                elif event.key == pygame.K_s:
                    self.player.move(0, 1)  # Move down

    def update(self, deltatime, actions):
        self.current_time += self.game.clock.tick(60) / 1000.0  # Convert milliseconds to seconds

        # Check for collision with the exit
        if self.player.rect.colliderect(self.end_rect):
            self.player_won = True

        # Check for collision with coins and collect them
        for coin in self.coins:
            if self.player.rect.colliderect(coin.rect):
                self.collected_coins += coin.collect()
                self.coins.remove(coin)

        # Update all sprites
        self.all_sprites.update(deltatime, actions)

        # check if time is up
        if self.current_time >= self.time_limit:
            self.time_up = True

    def render(self, display, font):
        display.fill((173, 216, 230))  # Fill the screen with background color

        # Draw walls, exit, player, and coins
        for wall in self.walls:
            pygame.draw.rect(display, (0, 0, 0), wall.rect)
        display.blit(self.spaceship_image, self.end_rect)
        display.blit(self.player.image, self.player.rect)
        for coin in self.coins:
            coin.update(self.game.clock.get_time() / 1000.0)
            display.blit(coin.image, coin.rect)

        self.health.render(display)

        self.all_sprites.draw(display)

        # Display attempt text
        display.blit(self.attempt_text, self.attempt_text_rect)

        # Display collected coins count
        display.blit(self.coin_image, self.coin_position)
        self.collected_text = self.font.render(f"Collected: {self.collected_coins}/{self.total_coins}", True, (255, 255, 255))
        display.blit(self.collected_text, (self.screen_width - self.collected_text.get_width() - 10, 10))

        # Display remaining time
        remaining_time = max(self.time_limit - self.current_time, 0)
        self.timer_text = self.timer_font.render(f"Time: {int(remaining_time)}", True, (255, 255, 255))
        display.blit(self.timer_text, self.timer_text_rect)

        # Display end game messages if conditions are met
        if self.time_up and not self.player_won:
            message_color = (255, 0, 0)  # Red for time's up
            message_text = "Time's up!"
        elif self.player_won:
            message_color = (0, 255, 0)  # Green for win message
            message_text = "You win!"

        if self.time_up or self.player_won:
            end_text = self.end_message_font.render(message_text, True, message_color)
            end_text_rect = end_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            display.blit(end_text, end_text_rect)

        # Check end game conditions
        if self.time_up and not self.player_won:
            self.attempt += 1
            if self.attempt <= self.num_hearts:
                # reset game state for next attempt
                self.player.rect.topleft = self.player_initial_position
                self.current_time = 0
                self.time_up = False
                self.collected_coins = 0
                # update attempt text for the next attempt
                self.attempt_text = self.font.render(f"Attempt : {self.attempt}", True, (255, 255, 255))

                self.reset_coins()

class Player(pygame.sprite.Sprite):
    def __init__(self, images, grid_size, walls, animation_speed=0.2, initial_position=(0, 0)):
        super().__init__()
        self.images = images if isinstance(images, list) else [images]  # Ensure images is always treated as a list
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.animation_speed = animation_speed
        self.animation_timer = 0
        self.rect = self.image.get_rect(topleft=initial_position if isinstance(initial_position, tuple) else (0, 0))
        self.grid_size = grid_size
        self.walls = walls
        self.num_collisions = 0
        self.hearts_left = 3

    def handle_events(self, events):
        pass

    def update(self, deltatime, actions):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

        if self.rect.colliderect(self.enemy.rect):
            self.collide_with_enemy()
            return True  # Return True to indicate collision
        
        return False  # Return False if no collision

    def move(self, dx, dy):
        self.rect.x += dx * self.grid_size
        self.rect.y += dy * self.grid_size
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; hit left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; hit right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; hit top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; hit bottom side of the wall
                    self.rect.top = wall.rect.bottom

    def collide_with_enemy(self):
        if self.num_collisions == 0:
           self.hearts_left -= 1
           self.num_collisions += 1

    def render(self, display, font):
        pass

class Enemies(pygame.sprite.Sprite):
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
        self.direction = 1    # 1 for right, -1 for left
        self.speed = 4.0 

    def handle_events(self, events):
        pass

    def update(self, deltatime, actions):
        # move enemy left or right
        self.rect.x += self.direction * self.speed

        # check collision with walls
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
            self.player.num_collisions = 0 
            
        
        # update current position index if enemy reaches the end of the path
        if self.rect.x < min(self.positions, key=lambda x: x[0])[0] or self.rect.x > max(self.positions, key=lambda x: x[0])[0]:
            self.current_position_index = (self.current_position_index + 1) % len(self.positions)
            self.rect.topleft = self.positions[self.current_position_index]

        

    def render(self, display):
        pass

class Wall:
    def __init__(self, pos, walls, grid_cell_size):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], grid_cell_size, grid_cell_size)

    def handle_events(self, events):
        pass

    def update(self, deltatime, actions):
        pass

    def render(self, display, font):
        pass

class Health():
    def __init__(self, game):
        self.game = game
        self.heart= pygame.image.load('images/heart.png')
        self.heart_rect = self.heart.get_rect()
        self.hearts_left = 3

    def handle_events(self, events):
        pass

    def update(self, deltatime, actions):
        pass

    def render(self, display):
        if self.hearts_left == 3:
            display.blit(self.heart,(20,10))
            display.blit(self.heart,(60,10))
            display.blit(self.heart,(100,10))
        elif self.hearts_left == 2:
                display.blit(self.heart,(20,10))
                display.blit(self.heart,(60,10))
        elif self.hearts_left == 1:
                display.blit(self.heart,(20,10))