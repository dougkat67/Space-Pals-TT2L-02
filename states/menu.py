from states.state import State
from states.naming import Naming
from button import Button
import pygame

class Menu(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.menu_image = pygame.image.load("images/main_menu.png").convert()
        self.button = Button(self.game)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.button.click = self.button.is_over(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                self.button.click = False


    def update(self, deltatime, actions):
        if self.button.click:
            new_state = Naming(self.game)
            new_state.enter_state()   #adds the new state to the top of the stack
        self.button.update()    
        self.game.reset_keys()

    def render(self, display, font):
        display.blit(self.menu_image, (0,0))
        self.button.render(display)

     
