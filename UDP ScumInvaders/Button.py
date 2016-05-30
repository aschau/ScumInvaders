import pygame

class Button():
    #screen = game scren
    #image = button image
    #sImage = Selected image
    #posx, posy = where it goes on the screen
    #imagew, imageh = image width and height
    #function (string) == what it deos ex. exit, game, etc.
    #sound = sound it makes when pressed
    #soundManager = sound manager
    def __init__(self, screen, image, sImage, posx, posy, imagew, imageh, function, sound, soundManager, disabled = False, dImage = None):
        self.screen = screen
        self.image = image
        self.sImage = sImage
        self.dImage = dImage
        self.function = function
        self.current = self.image
        self.posx = posx
        self.posy = posy
        self.sound = sound
        self.soundManager = soundManager
        self.selected = False
        self.disabled = disabled
        self.rect = pygame.Rect(posx, posy, imagew, imageh)


    def checkClicked(self, mousepos):
        if not self.disabled:
            return self.rect.collidepoint(mousepos)
    
    def checkHover(self, mousepos):
        if not self.disabled:
            if not self.selected:
                if self.rect.collidepoint(mousepos):
                    self.selected = True
                    self.flip_image()
            else:
                if not self.rect.collidepoint(mousepos):
                    self.selected = False
                    self.flip_image()

    def flip_image(self):
        if not self.disabled:
            self.soundManager.playSound("Button.ogg")
            if self.current == self.image:
                self.current = self.sImage
            
            elif self.current == self.sImage:
                self.current = self.image

    def click(self):
        if not self.disabled:
            pygame.time.delay(500)
            return self.function

    def draw(self):
        self.screen.blit(self.current, (self.posx, self.posy))