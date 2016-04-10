import pygame
from missle import Missle

class Enemy:
    def __init__(self, image, pos, imagew, imageh):
        self.image = image
        #self.oPosX = pos[0]
        #self.oPosY = pos[1]
        self.health = 2
        self.posx = pos[0]
        self.posy = pos[1]
        self.imagew = imagew
        self.imageh = imageh
        self.lastMove = None
        self.speed = 16
        self.collider = pygame.Rect(self.posx, self.posy, imagew, imageh)

    def fire(self):
        pass
        #return Missle(0, "missle1", (self.posx + (self.imagew - 18), self.posy - (self.imageh)), 8, 32)
   
    def moveLeft(self):
        self.posx -= self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def moveRight(self):
        self.posx += self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)
        #added a Position function
    def moveDown(self):
        self.posy += self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def getPos(self):
        return (self.posx, self.posy)