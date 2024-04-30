import pygame

class Menu():
    #reference back to the game functions
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
                                    #(x, y, width, height)
        self.cursor_rect = pygame.Rect(0, 0, 20, 20 )
        self.offset = -100 
        #makes sure cursor not on top of the text but on the left

    def draw_cursor(self):
        self.game.draw_text("*", 15, 20, self.cursor_rect.x,self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

#inherit the base class Menu earlier
class Mainmenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0,0,0))
            self.game.draw_text("Main Menu", 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 -20, 20 )
            self.game.draw_text("Start Game", 20, self.startx, self.starty, 20)
            self.draw_cursor()
            self.blit_screen()

    #def move_cursor(self):
    def check_input(self):
        self.draw_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.playing = True
            self.run_display = False


     
