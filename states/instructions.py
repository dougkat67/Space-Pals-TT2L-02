import pygame
from states.state import State
from level import Pet
from button import NextButton

class Instruction(State):
    def __init__(self, game):
        super().__init__(game)
        self.font_title = pygame.font.SysFont("Pixeltype Regular", 40, False, False)
        self.font_text = pygame.font.SysFont("Pixeltype Regular", 35, False, False)
        self.instructions_image = pygame.image.load("images/instruction.png").convert()
        self.next_button = NextButton(self.game)
        self.instructions = [
            ("- nurture  your  alien  pet  till  all  5  levels of  the  game", 500, 220),
            ("- use  coins  earned  in  the  mini  game  to  interact with  your  pet", 500, 250),
            ("- use  the  A, W, S, D  keys  to  move  the  pet  around  the  maze  and  collect  the  coins", 500, 340),
            ("within  the  time  limit.", 500, 360),
            ("*NOTE: each  level  only  has  one  chance  to  play , so  earn  as  many  coins  to  level  up.", 500, 400)
            ]
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.next_button.click = self.next_button.is_over(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                self.next_button.click = False
       
    def update(self, deltatime, actions):
        if self.next_button.click:
            new_state = Pet(self.game)
            new_state.enter_state()   #adds the new state to the top of the stack
        self.next_button.update()    
        self.game.reset_keys()

    def render(self, display, font):
        display.blit(self.instructions_image, (0,0))
        self.game.draw_text(display, "Help  take  care  of  the  alien  pet  you  found  so  it  can  retun  back  home", (0, 0, 0), 500,100, self.font_title)
        self.game.draw_text(display, "before  the  alien's  family  wreaks  havoc!", (0, 0, 0), 500,120, self.font_title)
        self.game.draw_text(display, "How  to  play  Main  Game:", (0, 0, 0), 500,170, self.font_title)
        self.game.draw_text(display, "How  to  play  Mini  Game:", (0, 0, 0), 500,290, self.font_title)
        
        for instruction, x, y in self.instructions:
            self.game.draw_text(display, instruction, (0, 0, 0), x, y, self.font_text)

        self.next_button.render(display)
            
        

