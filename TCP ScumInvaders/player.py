import pygame
from socket import *
from missile import Missile

'''
Functions:
    self.fire()
    self.moveLeft()
    self.moveRight()
    self.getPos()
'''
class Player:
    def __init__(self, playerNum, image, missileImage, pos, imagew, imageh, animation):
        self.image = image
        self.imagew = imagew
        self.imageh = imageh
        self.missileImage = missileImage
        self.playerNum = playerNum
        self.speed = 8
        self.posx = pos[0]
        self.posy = pos[1]
        self.collider = pygame.Rect(self.posx, self.posy, imagew, imageh)
        self.score = 0
        self.missileCount = 0
        self.missileCap = 3
        self.lives = 3
        self.alive = True
        self.anim = animation

    def moveLeft(self):
        self.posx -= self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def moveRight(self):
        self.posx += self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def getPos(self):
        return (self.posx, self.posy)

    def fire(self):
        self.missileCount += 1
        return Missile(self.playerNum, self.missileImage, (self.posx + (self.imagew - 18), self.posy - (self.imageh)), 8, 32)