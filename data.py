import json
import pygame

class Data(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('images/playing.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

        # file path
        self.user_text_file = 'user_text.json'
        self.leaderboard_file = 'leaderboard.json'


        self.combined_data = self.combine_data() 

    def combine_data(self): #combined two json files
        with open(self.user_text_file, 'r') as file:
            user_text_data = json.load(file)
        
        with open(self.leaderboard_file, 'r') as file:
            leaderboard_data = json.load(file)
        
        # Combine data into a dictionary
        combined_data = {}
        user_texts = user_text_data if isinstance(user_text_data, list) else user_text_data.get("user_texts", [])
        times = [entry.get("time") for entry in leaderboard_data]
        
        for user_text, time in zip(user_texts, times):
            combined_data[user_text] = time
        
        with open("combined_data.json", 'w') as file:
            json.dump(combined_data, file, indent=4)
        
        self.combined_data = combined_data  
        return combined_data

    def update(self, deltatime, player_action):
        pass

    def render(self, display):
        pass

    def update_combined_data(self):
        self.combine_data()
