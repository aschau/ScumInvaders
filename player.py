import pygame
from missle import Missle

class Player:
    def __init__(self, playerNum, image, missleImage, pos, imagew, imageh):
        self.image = image
        self.imagew = imagew
        self.imageh = imageh
        self.missleImage = missleImage
        self.playerNum = playerNum
        self.speed = 8
        self.posx = pos[0]
        self.posy = pos[1]
        self.collider = pygame.Rect(self.posx, self.posy, imagew, imageh)
        self.score = 0
        self.missleCount = 0
        self.missleCap = 100
        self.lives = 3

    def moveLeft(self):
        self.posx -= self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def moveRight(self):
        self.posx += self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def getPos(self):
        return (self.posx, self.posy)

    def fire(self):
        self.missleCount += 1
        return Missle(self.playerNum, self.missleImage, (self.posx + (self.imagew - 18), self.posy - (self.imageh)), 8, 32)