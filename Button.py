import pygame

class Button():
    def __init__(self, screen, image, sImage, posx, posy, imagew, imageh):
        self.screen = screen
        self.image = image
        self.sImage = sImage
        self.current = self.image
        self.posx = posx
        self.posy = posy
        
        self.rect = pygame.Rect(posx, posy, imagew, imageh)


    def check(self, mousepos, click = False):
        if self.rect.collidepoint(mousepos) and click:
            pass
        
        elif self.rect.collidepoint(mousepos):
            pass

    def draw(self):
        self.screen.blit(self.current, (self.posx, self.posy))