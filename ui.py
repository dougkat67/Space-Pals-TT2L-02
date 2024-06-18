import pygame , json , threading , time
from setting import *
from alien import *


class UI:
    def __init__(self):
        # general
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.satiety_bar_rect = pygame.Rect(10, 34, FEEDING_BAR_WIDTH, BAR_HEIGHT)
        self.happy_bar_rect = pygame.Rect(10, 10, HAPPINESS_BAR_WIDTH, BAR_HEIGHT)
        self.clear_bar_rect = pygame.Rect(10, 54, HAPPINESS_BAR_WIDTH, BAR_HEIGHT)

        # stats
        self.stats = {'happiness': 100, 'cleanliness': 100, 'feeding': 100}
        self.happy = self.stats['happiness'] * 0.1
        self.cleanliness = self.stats['cleanliness'] * 0.1
        self.feeding = self.stats['feeding'] * 0.2

        # Initialize the level and load coins
        self.coin = self.load_collected_coins()

        # Start the background thread to monitor the JSON file
        self.monitor_thread = threading.Thread(target=self.monitor_json_file)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def load_collected_coins(self):
        try:
            with open('coins.json', 'r') as file:
                data = json.load(file)
                return data.get('coins', 0)
        except FileNotFoundError:
            return 0

    def save_collected_coins(self):
        with open('coins.json', 'w') as file:
            json.dump({'coins': self.coin}, file)

    def show_bar(self, display, current, max_amount, bg_rect, color):
        pygame.draw.rect(display, UI_BG_COLOR, bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(display, color, current_rect)
        pygame.draw.rect(display, UI_BORDER_COLOR, bg_rect, 3)

    def show_coin(self, display, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = display.get_size()[0] - 20
        y = display.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(display, UI_COIN_BG_COLOR, text_rect.inflate(20, 20))
        display.blit(text_surf, text_rect)
        pygame.draw.rect(display, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def display(self, display):
        self.show_bar(display, self.feeding, self.stats['feeding'], self.satiety_bar_rect, SATIETY_COLOR)
        self.show_bar(display, self.happy, self.stats['happiness'], self.happy_bar_rect, HAPPY_COLOR)
        self.show_bar(display, self.cleanliness, self.stats['cleanliness'], self.clear_bar_rect, CLEAR_COLOR)
        self.show_coin(display, self.coin)

    def update(self, deltatime, player_action):
        self.coin = self.load_collected_coins()

    def render(self, display):
        pass

    def reset_stats(self):
        self.happy = 0

    def refresh_coin_display(self):
        self.coin = self.load_collected_coins()

    def monitor_json_file(self):
        while True:
            new_coins = self.load_collected_coins()
            if new_coins != self.coin:
                self.coin = new_coins
                # Trigger a UI update, assuming you have a method or mechanism to do this
                # For example, you might call display() method directly or set a flag
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"update_coins": True}))
            time.sleep(1)  # Check every second

# Assuming this is part of a larger game loop elsewhere in your code:
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    ui = UI()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT and "update_coins" in event.dict:
                ui.display(screen)  # Update display when coins change

        # Your game update logic here
        
        pygame.display.flip()
    pygame.quit()
