import pygame
from player import Player
from enemy import Enemy
from Button import Button
from collections import deque
import random

class game:
    def __init__(self, screen, screenw, screenh, spriteList, soundManager):
        self.sprites = spriteList
        self.screen = screen
        self.screenw = screenw
        self.screenh = screenh
        self.soundManager = soundManager
        self.player = Player(1, "ship1", "missle2", (500, 700), 32, 32)

        self.enemyGrid = []
        self.enemyRowCount = 5
        self.enemyColumnCount = 10
        self.enemyCount = 50

        for row in range(self.enemyRowCount):
            self.enemyGrid.append([])
            for column in range(self.enemyColumnCount):
                rnum = random.randint(1, 2)
                enemySprite = "alien1"
                if rnum == 1:
                    enemySprite = "alien2"
                self.enemyGrid[row].append(Enemy(enemySprite, (32 + (column * 96), (row * 64) - self.enemyRowCount * 64), 32, 32))
        
        self.missles = []

        self.missleDelay = 100
        self.enemyDelay = 500
        self.nextMissle = pygame.time.get_ticks() + self.missleDelay
        self.nextEnemyMove = pygame.time.get_ticks() + self.enemyDelay

    def draw(self):
        self.screen.blit(self.sprites.getSprite("GameBackground"), (0, 0))
        self.screen.blit(self.sprites.getSprite(self.player.image), self.player.getPos())
        
        for missle in self.missles:
            self.screen.blit(self.sprites.getSprite(missle.image), missle.getPos())
     
        for row in range(self.enemyRowCount):
            for column in range(self.enemyColumnCount):
                if self.enemyGrid[row][column].health != 0:
                    self.screen.blit(self.sprites.getSprite(self.enemyGrid[row][column].image), self.enemyGrid[row][column].getPos())

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
                if not ((self.player.posx - self.player.speed) <= 0):
                    self.player.moveLeft()

        if keys[pygame.K_d]:
            if not ((self.player.posx + self.player.speed + self.player.imagew) >= self.screenw):
                self.player.moveRight()

        if keys[pygame.K_ESCAPE]:
            return "Exit"

        if pygame.time.get_ticks() > self.nextMissle:
            self.nextMissle = pygame.time.get_ticks() + self.missleDelay

            if keys[pygame.K_SPACE]:
                if self.player.missleCount < self.player.missleCap:
                    self.missles.append(self.player.fire())

        if pygame.time.get_ticks() > self.nextEnemyMove:
            self.nextEnemyMove = pygame.time.get_ticks() + self.enemyDelay

            for row in range(self.enemyRowCount):
                for column in range(self.enemyColumnCount):
                    if self.enemyGrid[row][column].posy + 32 >= 768 or (self.enemyGrid[row][column].posy + 32 > self.player.posy and self.player.posx < self.enemyGrid[row][column].posx < self.player.posx + 64) :
                        return "Menu"
                    if self.enemyGrid[row][column].lastMove == None:
                        self.enemyGrid[row][column].lastMove = "Left"
                        self.enemyGrid[row][column].moveDown()
                        self.enemyGrid[row][column].moveDown()
                        self.enemyGrid[row][column].moveDown()
                        print("This happened.")
                    elif self.enemyGrid[row][column].lastMove == "Left":
                        if self.enemyGrid[row][column].posx <= 0: 
                            self.enemyGrid[row][column].lastMove = "Right"
                            self.enemyGrid[row][column].moveDown()
                          #  self.enemyGrid[row][column].moveRight()
                        else:
                            self.enemyGrid[row][column].moveLeft()
                    elif self.enemyGrid[row][column].lastMove == "Right":
                        if self.enemyGrid[row][column].posx + 64 >= 1024:
                            self.enemyGrid[row][column].lastMove = "Left"
                            self.enemyGrid[row][column].moveDown()
                           # self.enemyGrid[row][column].moveLeft()
                        else:
                            self.enemyGrid[row][column].moveRight()

            '''
            rNum = random.randint(1, 5)
            for row in range(self.enemyRowCount):
                for column in range(self.enemyColumnCount):
                    #checks if enemies have reached the bottom of the screen
                    if self.enemyGrid[row][column].posy + 32 >= 768 or (self.enemyGrid[row][column].posy + 32 > self.player.posy and self.player.posx < self.enemyGrid[row][column].posx < self.player.posx + 64) :
                        return "Menu"
                    if self.enemyGrid[row][column].health != 0:
                        if rNum >= 3:
                            self.enemyGrid[row][column].lastMove = "Down"
                            self.enemyGrid[row][column].moveDown() 

                        elif rNum == 1:
                            if (self.enemyGrid[row][column].posx - 16 >= 0) and self.enemyGrid[row][column].lastMove != "Left":
                                self.enemyGrid[row][column].lastMove = "Left"
                                self.enemyGrid[row][column].moveLeft()
                        
                        elif rNum == 2:
                            if ((self.enemyGrid[row][column].posx + 16 + self.enemyGrid[row][column].imagew) <= self.screenw) and self.enemyGrid[row][column].lastMove != "Right":
                                self.enemyGrid[row][column].lastMove = "Right"
                                self.enemyGrid[row][column].moveRight() 
                '''
        numMissles = 0
        while numMissles < len(self.missles):
            self.missles[numMissles].update()
            if ((self.missles[numMissles].posy - self.missles[numMissles].imageh) <= 0):
                attacker = self.missles.pop(numMissles).owner
                if attacker == 1:
                    self.player.missleCount -= 1
            
            numMissles += 1
        
        for row in range(self.enemyRowCount):
            for column in range(self.enemyColumnCount):
                if self.enemyGrid[row][column].health != 0:
                    numMissles = 0
                    while numMissles < len(self.missles):
                        if self.enemyGrid[row][column].collider.colliderect(self.missles[numMissles].collider):
                            attacker = self.missles.pop(numMissles).owner
                            self.enemyGrid[row][column].health -= 1
                            #checks if no more enemies 
                            if self.enemyGrid[row][column].health == 0: 
                                self.enemyCount -= 1
                            if attacker == 1:
                                self.player.missleCount -= 1

                        numMissles += 1
                             
        if self.enemyCount == 0:
            return "Menu"
        return "Game"