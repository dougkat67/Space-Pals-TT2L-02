import pygame
from states.state import State

class Naming(State):    #inherit from State
    def __init__(self, game):
        State.__init__(self, game)  #use back the abstract state class
        self.naming_image =  pygame.image.load("WIP_art/spacepaslnamingpage.png").convert()
        
    def update(self, deltatime, actions):
        pass
       
    def render(self, display, font):
        display.blit(self.naming_image, (0,0))
        self.game.draw_text(display, "Hello", (0,0,0), 500, 100, font)

    

        