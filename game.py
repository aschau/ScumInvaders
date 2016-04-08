import pygame
from player import Player
from enemy import Enemy
from button import Button
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
        self.enemyColumnCount = 11

        for row in range(self.enemyRowCount):
            self.enemyGrid.append([])
            for column in range(self.enemyColumnCount):
                rnum = random.randrange(1, 2)
                enemySprite = "alien1"
                if rnum == 1:
                    enemySprite = "alien2"
                self.enemyGrid[row].append(Enemy(enemySprite, (column * 32, row * 32), 32, 32))
        
        self.missles = []

        self.delay = 100
        self.next = pygame.time.get_ticks() + self.delay

    def draw(self):
        self.screen.blit(self.sprites.getSprite("GameBackground"), (0, 0))
        self.screen.blit(self.sprites.getSprite(self.player.image), self.player.getPos())
        
        for missle in self.missles:
            self.screen.blit(self.sprites.getSprite(missle.image), missle.getPos())
     
        for row in range(self.enemyRowCount):
            for column in range(self.enemyColumnCount):
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

        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.delay

            if keys[pygame.K_SPACE]:
                if self.player.missleCount < 5:
                    self.missles.append(self.player.fire())

        numMissles = 0
        while numMissles < len(self.missles):
            self.missles[numMissles].update()
            if ((self.missles[numMissles].posy - self.missles[numMissles].imageh) <= 0):
                attacker = self.missles.pop(numMissles).owner
                if attacker == 1:
                    self.player.missleCount -= 1

            numMissles += 1

        return "Game"