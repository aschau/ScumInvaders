import pygame
from missle import Missle

class Player:
    def __init__(self, image, missleImage, pos, imagew, imageh):
        self.image = image
        self.imagew = imagew
        self.imageh = imageh
        self.missleImage = missleImage
        self.speed = 10
        self.posx = pos[0]
        self.posy = pos[1]
        self.score = 0

    def moveLeft(self):
        self.posx -= self.speed

    def moveRight(self):
        self.posx += self.speed

    def getPos(self):
        return (self.posx, self.posy)

    def fire(self):
        return Missle(self.missleImage, self.posx, self.posy + self.imageh)