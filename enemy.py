import pygame
from missile import Missile

'''
Functions:
    self.fire()
    self.moveLeft()
    self.moveRight()
    self.moveDown()
    self.getPos()
'''
class Enemy:
    def __init__(self, pos, imagew, imageh, animation, health, speed):
        #self.image = image
        self.anim = animation
        #self.oPosX = pos[0]
        #self.oPosY = pos[1]
        self.health = health
        self.posx = pos[0]
        self.posy = pos[1]
        self.imagew = imagew
        self.imageh = imageh
        self.lastMove = None
        self.speed = speed
        self.downSpeed = 48
        self.missileCount = 0
        self.missileCap = 100
        self.collider = pygame.Rect(self.posx, self.posy, imagew, imageh)

    def fire(self):
        self.missileCount += 1
        return Missile(0, "missile1", (self.posx + (self.imagew + 18), self.posy + (self.imageh)), 8, 32)
   
    def moveLeft(self):
        self.posx -= self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def moveRight(self):
        self.posx += self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)
        #added a Position function
    def moveDown(self):
        self.posy += self.downSpeed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def getPos(self):
        return (self.posx, self.posy)