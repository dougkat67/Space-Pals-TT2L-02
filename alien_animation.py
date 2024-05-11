import pygame
import sys

class AlienAnimation:
    def __init__(self, screen):
        pygame.init()
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 500
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('alien animation')

        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 64)
        self.DARK_GREY = (50, 50, 50)

        self.sheet = pygame.image.load("alien.png").convert()
        self.cells = []
        for n in range(4):
            width, height = (480, 480)
            rect = pygame.Rect(n * width, 0, width, height)
            image = pygame.Surface(rect.size).convert()
            image.blit(self.sheet, (0, 0), rect)
            alpha = image.get_at((0, 0))
            image.set_colorkey(alpha)
            self.cells.append(image)

        self.playerImg = self.cells[0]
        self.player = self.playerImg.get_rect()
        self.player.center = (320, 240)

        self.FPS = 60
        self.FPSCLOCK = pygame.time.Clock()

        self.scaling_factor = 0.5

        # add an animation frame counter
        self.frame_counter = 0

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] != 0: self.player.y -= 4
            if keys[pygame.K_s] != 0: self.player.y += 4
            if keys[pygame.K_a] != 0: self.player.x -= 4
            if keys[pygame.K_d] != 0: self.player.x += 4

            self.screen.fill(self.DARK_GREY)

            # Get the original dimensions of the player image
            original_width, original_height = self.playerImg.get_size()

            # Calculate the scaled width and height
            scaled_width = int(original_width * self.scaling_factor)
            scaled_height = int(original_height * self.scaling_factor)

            # Scale the player image
            scaled_playerImg = pygame.transform.scale(self.playerImg, (scaled_width, scaled_height))

            # Animate the player
            self.playerImg = self.cells[self.frame_counter // 10 % len(self.cells)]  # Change image every 10 frames
            self.frame_counter += 1

            # Blit the scaled image onto the screen
            self.screen.blit(scaled_playerImg, self.player)

            pygame.display.flip()
            self.FPSCLOCK.tick(self.FPS)