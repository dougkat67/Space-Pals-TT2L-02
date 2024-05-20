import pygame

import sys

class MainMenuState:
    def __init__(self, game):
        self.game = game
        self.running = True
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.change_state("Naming")

    def update(self):
        pass

    def render(self):
        self.game.display.fill((0, 0, 0))
        background_image = pygame.image.load("WIP_art/spacepalsmenupage.png").convert()
        self.game.display.blit(background_image, (0,0))
        self.game.draw_text("Main Menu", 40, 500, 45)
        self.game.draw_text("Press ENTER to Start", 20, 470, 350)
        pygame.display.update()

class NamingState:
    def __init__(self, game):
        self.game = game
        self.running = True
        self.input_text = ""  # Variable to store the player's input text

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Do something with the input text, e.g., store it or process it
                    print("Player's input:", self.input_text)
                    self.input_text = ""  # Clear the input text for the next input
                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character from the input text
                    self.input_text = self.input_text[:-1]
                else:
                    # Append the pressed key to the input text
                    self.input_text += event.unicode

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         self.game.quit()

    def update(self):
        pass

    def render(self):
        self.game.display.fill((0, 0, 0))
        background_image = pygame.image.load("WIP_art/spacepaslnamingpage.png").convert()
        egg_image = pygame.image.load("WIP_art/newnamingegg.png").convert_alpha()
        newegg_image = pygame.transform.scale(egg_image,(300,300))
        self.game.display.blit(background_image, (0,0))
        self.game.display.blit(newegg_image, (350,95))
        self.game.draw_text("You encountered an interesting looking alien egg.", 40, 500, 50)
        self.game.draw_text("It's hatching!", 40, 500, 100)
        self.game.draw_text("Enter a name for the egg:", 30, 500, 470)
        self.game.draw_text(self.input_text, 30, 750, 470)  # Render the input text
        pygame.display.update()

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.DISPLAY_W, self.DISPLAY_H = 1000, 500
        self.display = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.clock = pygame.time.Clock()
        self.current_state = None
        self.font_name = pygame.font.SysFont("Pixeltype Regular", 50, False, False)

    def change_state(self, new_state):
        if new_state == "MainMenu":
            self.current_state = MainMenuState(self)
        elif new_state == "Naming":
            self.current_state = NamingState(self)

    def quit(self):
        self.running = False

    def draw_text(self, text, size, x, y):
        font = self.font_name
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, text_rect)

    def run(self):
        self.change_state("MainMenu")

        while self.running:
            self.current_state.handle_events()
            self.current_state.update()
            self.current_state.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()