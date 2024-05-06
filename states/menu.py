from states.state import State

class Menu(State):
    def __init__(self, game):
        State.__init__(self, game)

    def update(self, deltatime, player_action):
        self.game.reset_keys()

    def render(self, display):
        display.fill((255,255,255))
        self.game.draw_text(display, "Main Menu", (0,0,0), 500, 250)


     
