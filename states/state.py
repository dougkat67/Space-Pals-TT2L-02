class State():                    #now as an abstract base class; also will be used as a template for other states    
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, deltatime, player_action):
        pass

    def render(self, surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self) #push

    def exit_state(self):
        self.game.state_stack.pop() 
