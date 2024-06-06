from states.state import State
from states.naming import Naming 

class Instruction(State):
    def __init__(self, game):
        super().__init__(self,game)
        self.instructions = ["1. Help your alien pet to go home.",
                             "2. There are 5 levels in total. Complete all the levels to win the game."
                             "3. Care and love your alien pet to grow it."
                             "4. Play the minigames to gain coins and use the functionalities."]
        
    def update(self, deltatime, actions):
        pass

    def render(self, display):
        display.fill((0, 0, 0))
        self.game.draw_text(display, "Instructions:", (255, 255, 255), 50,50, 32)
        self.game.draw_text(display, self.instructions[0], (255, 255, 255), 50 ,100, 24)
        self.game.draw_text(display, self.instructions[1], (255, 255, 255), 50 ,150, 24)
        self.game.draw_text(display, self.instructions[2], (255, 255, 255), 50 ,180, 24)
        self.game.draw_text(display, self.instructions[3], (255, 255, 255), 50 ,230, 24)
        self.game.draw_text(display, self.instructions[4], (255, 255, 255), 50 ,280, 24)
       

