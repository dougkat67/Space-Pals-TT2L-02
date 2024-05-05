import pygame

class Naming(State):
    def __init__(self, game_instance):
        self.game_instance = game_instance

    def start_game(self):
        self.game_instance.game_loop("You encountered an fascinating looking alien egg.",
                                     "It's hatching!")


        