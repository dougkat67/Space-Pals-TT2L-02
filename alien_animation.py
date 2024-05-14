import pygame
import sys

class AlienAnimation:
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()

        # Constants
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 500
        self.BLACK = (0, 0, 0)
        self.DARK_GREY = (50, 50, 50)
        self.FPS = 60
        self.scaling_factor = 0.5
        self.player_speed = 4

        # Load alien image and create cells
        self.load_alien_image()
        self.create_cells()

        # Player attributes
        self.player_rect = self.playerImg.get_rect(center=(320, 240))

    def load_alien_image(self):
        self.sheet = pygame.image.load("alien.png").convert_alpha()

    def create_cells(self):
        self.cells = [self.sheet.subsurface(pygame.Rect(n * 480, 0, 480, 480)) for n in range(4)]
        self.playerImg = self.cells[0]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def move_player(self, keys):
        if keys[pygame.K_w]: self.player_rect.y -= self.player_speed
        if keys[pygame.K_s]: self.player_rect.y += self.player_speed
        if keys[pygame.K_a]: self.player_rect.x -= self.player_speed
        if keys[pygame.K_d]: self.player_rect.x += self.player_speed

    def animate_player(self):
        self.playerImg = self.cells[self.frame_counter // 10 % len(self.cells)]
        self.frame_counter += 1

    def run(self):
        self.frame_counter = 0
        while True:
            self.handle_events()
            keys = pygame.key.get_pressed()
            self.move_player(keys)

            self.screen.fill(self.DARK_GREY)
            self.animate_player()
            scaled_playerImg = pygame.transform.scale(self.playerImg, (int(self.playerImg.get_width() * self.scaling_factor), int(self.playerImg.get_height() * self.scaling_factor)))
            self.screen.blit(scaled_playerImg, self.player_rect)
            pygame.display.flip()
            self.clock.tick(self.FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption('Alien Animation')
    game = AlienAnimation(screen)
    game.run()

if __name__ == "__main__":
    main()