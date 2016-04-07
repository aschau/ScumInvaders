import pygame

class Button():
    def __init__(self, screen, image, sImage, posx, posy, imagew, imageh, function, sound, soundManager):
        self.screen = screen
        self.image = image
        self.sImage = sImage
        self.function = function
        self.current = self.image
        self.posx = posx
        self.posy = posy
        self.sound = sound
        self.soundManager = soundManager
        self.selected = False
        self.rect = pygame.Rect(posx, posy, imagew, imageh)


    def checkClicked(self, mousepos):
        return self.rect.collidepoint(mousepos)
    
    def checkHover(self, mousepos):
        if not self.selected:
            if self.rect.collidepoint(mousepos):
                self.selected = True
                self.flip_image()
        else:
            if not self.rect.collidepoint(mousepos):
                self.selected = False
                self.flip_image()

    def flip_image(self):
        self.soundManager.playSound("Button.ogg")
        if self.current == self.image:
            self.current = self.sImage
            
        elif self.current == self.sImage:
            self.current = self.image

    def click(self):
        self.soundManager.playSound(self.sound)
        return self.function

    def draw(self):
        self.screen.blit(self.current, (self.posx, self.posy))