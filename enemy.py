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
    def __init__(self, pos, imagew, imageh, animation, health, speed, row, col, type):
        self.anim = animation
        self.type = type
        self.health = health
        self.row = row
        self.col = col
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
        self.dead = False

    def fire(self):
        self.missileCount += 1
        return Missile(-1, "missile", (self.posx + (self.imagew - 18), self.posy + (self.imageh)), 8, 32, self.row, self.col)
   
    def moveLeft(self):
        self.posx -= self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def moveRight(self):
        self.posx += self.speed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def moveDown(self):
        self.posy += self.downSpeed
        self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def getPos(self):
        return (self.posx, self.posy)