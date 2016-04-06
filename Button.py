import pygame

class Button():
    def __init__(self, screen, image, sImage, posx, posy, imagew, imageh, function):
        self.screen = screen
        self.image = image
        self.sImage = sImage
        self.function = function
        self.current = self.image
        self.posx = posx
        self.posy = posy
        
        self.rect = pygame.Rect(posx, posy, imagew, imageh)


    def checkClicked(self, mousepos):
        return self.rect.collidepoint(mousepos)
    
    def checkHover(self, mousepos):
        if self.rect.collidepoint(mousepos):
            self.current = self.sImage

    def click(self):
        pass

    def draw(self):
        self.screen.blit(self.current, (self.posx, self.posy))