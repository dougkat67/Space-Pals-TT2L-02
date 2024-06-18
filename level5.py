import sys
import pygame
from collecting_coins import Coin
from states.state import State
import json

class Level5(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.walls = []  # list to hold the walls
        self.grid_cell_size = 25


        #coin sfx
        self.coin_sound = pygame.mixer.Sound('audio/coin.mp3')
        self.coin_sound.set_volume(0.2)

        self.data = {
            'coins': 0
        }


        
        # Load images with error handling
        try:
            self.heart_image = pygame.image.load('images/heart.png')
            self.coin_images = [
                pygame.transform.scale(pygame.image.load('images/coin_0.png'), (20, 20)),
                pygame.transform.scale(pygame.image.load('images/coin_1.png'), (20, 20)),
                pygame.transform.scale(pygame.image.load('images/coin_2.png'), (20, 20)),
                pygame.transform.scale(pygame.image.load('images/coin_3.png'), (20, 20)),
                pygame.transform.scale(pygame.image.load('images/coin_4.png'), (20, 20)),
                pygame.transform.scale(pygame.image.load('images/coin_5.png'), (20, 20))
              ]

            self.spaceship_image = pygame.transform.scale(pygame.image.load('images/spaceship.png'), (60, 35))

            self.alien_images = [
                pygame.transform.scale(pygame.image.load('images/alien5_1.png'), (25, 25)),
                pygame.transform.scale(pygame.image.load('images/alien5_2.png'), (25, 25)),
                pygame.transform.scale(pygame.image.load('images/alien5_3.png'), (25, 25)),
                pygame.transform.scale(pygame.image.load('images/alien5_4.png'), (25, 25))
            ]
        except pygame.error as e:
            print(f"Error loading image: {e}")
            sys.exit(1)

        self.level5 =  [
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
            "W W W WW                 W   W     W   W",
            "WWW W    WWWW  WWW  W  W    WW   W W   W",
            "W W WW W WW      W WW WWWWW W  WWW W W W",
            "W W    W    W  W W  W          W     W W",
            "W WW  WWWWWWW  WWWWWWWW  WWWWWWWW  WWW W",
            "W                                      W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

        self.num_cols = len(self.level5[0])
        self.num_rows = len(self.level5)
        self.grid_cell_size = 25
        self.screen_width = self.num_cols * self.grid_cell_size
        self.screen_height = self.num_rows * self.grid_cell_size

        self.font = pygame.font.Font(None, 36)
        self.attempt = 1
        self.attempt_text = self.font.render(f"Attempt : {self.attempt}/3", True, (255, 255, 255))
        self.attempt_text_rect = self.attempt_text.get_rect(center=(self.screen_width // 2, 25))

        self.num_hearts = 3
        self.heart_spacing = 40
        self.heart_position = (10, 10)

        self.coin_positions =  [(1, 6), (1, 17), (3, 14), (4, 10), (7, 3), 
                  (9, 13), (10, 7), (13, 9), (11, 15), (16, 3), 
                  (20, 10), (18, 16), (21, 16), (23, 18), (29, 9),
                  (31, 14), (36, 5), (34, 17), (34, 6), (38, 3)
                  ]
        
        self.reset_coins()

        self.player_initial_position = (1 * self.grid_cell_size, 3 * self.grid_cell_size)
        self.player = Player(self.alien_images, self.grid_cell_size, self.walls, initial_position = self.player_initial_position)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        self.collected_coins = 0
        self.total_coins = len(self.coins)
        self.coin_image = pygame.image.load('images/coin_0.png')

        self.time_limit = 35
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
        for y, row in enumerate(self.level5):
            for x, col in enumerate(row):
                if col == "W":
                    Wall((x * self.grid_cell_size, y * self.grid_cell_size), self.walls, self.grid_cell_size)
                if col == "E":
                    self.end_rect = pygame.Rect(x * self.grid_cell_size, y * self.grid_cell_size, self.grid_cell_size, self.grid_cell_size)

    def reset_coins(self):
        self.coins = [Coin(self.grid_cell_size, pos, self.coin_images) for pos in self.coin_positions]

    def display_hearts(self, display, attempt):
        for i in range(self.num_hearts):
            if attempt == 1:
                display.blit(self.heart_image, (self.heart_position[0] + i * self.heart_spacing, self.heart_position[1]))
            elif attempt == 2:
                if i < 2:
                    display.blit(self.heart_image, (self.heart_position[0] + i * self.heart_spacing, self.heart_position[1]))
                else:
                    bw_heart_image = self.heart_image.convert()
                    bw_heart_image = bw_heart_image.convert_alpha()
                    bw_heart_image.fill((128, 128, 128, 255), None, pygame.BLEND_RGB_MULT)
                    display.blit(bw_heart_image, (self.heart_position[0] + i * self.heart_spacing, self.heart_position[1]))
            elif attempt == 3:
                if i == 0:
                    display.blit(self.heart_image, (self.heart_position[0] + i * self.heart_spacing, self.heart_position[1]))
                else:
                    bw_heart_image = self.heart_image.convert()
                    bw_heart_image = bw_heart_image.convert_alpha()
                    bw_heart_image.fill((128, 128, 128, 255), None, pygame.BLEND_RGB_MULT)
                    display.blit(bw_heart_image, (self.heart_position[0] + i * self.heart_spacing, self.heart_position[1]))


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
            self.save_collected_coins()

        # Check for collision with coins and collect them
        for coin in self.coins:
            if self.player.rect.colliderect(coin.rect):
                self.coin_sound.play()
                self.collected_coins += coin.collect()
                self.coins.remove(coin)
                self.data['coins'] += 1
                self.save_collected_coins()

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
            else:
                self.exit_state()

        # Display end game messages if conditions are met
        if self.time_up and not self.player_won :
            message_color = (255, 0, 0)  # Red for time's up
            message_text = "Time's up!" 

        elif self.player_won:
            message_color = (0, 255, 0)  # Green for win message
            message_text = "You win!" 
            self.exit_state()

        elif self.attempt == 4:
            message_color = (255, 0, 0)  # Red for time's up
            message_text = "Game over!" 
            self.exit_state()

        if self.time_up or self.player_won:
            end_text = self.end_message_font.render(message_text, True, message_color)
            end_text_rect = end_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            display.blit(end_text, end_text_rect)

        self.display_hearts(display,self.attempt)
    def save_collected_coins(self):
         with open('coins.json', 'w') as file:
            json.dump(self.data, file)

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

    def render(self, display, font):
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

