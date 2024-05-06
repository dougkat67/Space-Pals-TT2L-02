import pygame
from states.state import State


class Naming(State):    #inherit from State
    def __init__(self, game):
        State.__init__(self, game)  #use back the abstract state class
        self.game = game
        self.naming_image =  pygame.image.load("WIP_art/spacepaslnamingpage.png").convert()
        image = pygame.image.load("WIP_art/newnamingegg.png").convert_alpha()
        self.egg_image = pygame.transform.scale(image,(300,300))
        self.user_text = ""
        self.input_rect = pygame.Rect(200,200,140,32)
        self.color = pygame.Color('Black')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[0:-1]
                else:
                    self.user_text += event.unicode
        
    def update(self, deltatime, actions):
        pass
       
    def render(self, display, font):
        display.blit(self.naming_image, (0,0))
        display.blit(self.egg_image, (350,100))
        self.game.draw_text(display, "You encountered an interesting looking alien egg.", (0,0,0), 500, 50, font)
        self.game.draw_text(display, "It's hatching!", (0,0,0), 500, 100, font)
        self.text_surface = self.game.font_name.render(self.user_text, True, (0,0,0))
        display.blit(self.text_surface, self.input_rect)
        pygame.draw.rect(self.game.window,self.color,self.input_rect)

    

        