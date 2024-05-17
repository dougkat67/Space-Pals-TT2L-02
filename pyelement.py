import pygame


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale),int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False
    
    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                for event in pygame.event.get():    
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.clicked = True
                        action = True
            
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
    def update(self, deltatime, player_action):
        pass

    def render(self, display):
        pass

class ImageDraw():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale),int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self,surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, deltatime, player_action):
        pass

    def render(self, display):
        pass

class ImageCenterDraw():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale),int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self,surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, deltatime, player_action):
        pass

    def render(self, display):
        pass

class SpriteSheet():
    def __init__(self,image):
        self.sheet = image

    def get_frame(self,frame,width,height,scale,colour):
        image = pygame.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0, 0),((frame*width), 0, width,height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)
        
        return image
    def update(self, deltatime, player_action):
        pass

    def render(self, display):
        pass