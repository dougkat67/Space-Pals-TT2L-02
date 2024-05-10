from states.state import State
from states.naming import Naming
from button import Button
import pygame

class Menu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.menu_image = pygame.image.load("WIP_art/spacepalsmenupage.png").convert()
        self.button = Button(self.game)

    def update(self, deltatime, actions):
        if self.button.click:
            new_state = Naming(self.game)
            new_state.enter_state()   #adds the new state to the top of the stack
        self.button.update()    
        self.game.reset_keys()

    def render(self, display, font):
        display.blit(self.menu_image, (0,0))
        self.game.draw_text(display, "Main Menu", (0,0,0), 500, 45, font)
        self.button.render(display)

     
