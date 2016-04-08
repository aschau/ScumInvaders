import pygame

class Missle:
    def __init__(self, owner, image, pos, imagew, imageh):
        self.owner = owner
        self.image = image
        self.posx = pos[0]
        self.posy = pos[1]
        self.imagew = imagew
        self.imageh = imageh
        self.speed = 10

    def update(self):
        self.posy -= self.speed

    def getPos(self):
        return (self.posx, self.posy)