import pygame
from player import Player
from enemy import Enemy
from button import Button
from collections import deque

class game:
    def __init__(self, screen, screenw, screenh, spriteList, soundManager):
        self.sprites = spriteList
        self.screen = screen
        self.screenw = screenw
        self.screenh = screenh
        self.soundManager = soundManager
        self.player = Player(1, "ship1", "missle2", (500, 700), 32, 32)

        enemyGrid = []
        enemyRowCount = 5
        enemyColumnCount = 11

        for row in range(enemyRowCount):
            enemyGrid.append([])
            for enemy in range(enemyColumnCount):
                enemyGrid[row].append(Enemy())
        
        self.missles = []

        self.delay = 50
        self.next = pygame.time.get_ticks() + self.delay

    def draw(self):
        self.screen.blit(self.sprites.getSprite("GameBackground"), (0, 0))
        self.screen.blit(self.sprites.getSprite(self.player.image), self.player.getPos())
        
        for missle in self.missles:
            self.screen.blit(self.sprites.getSprite(missle.image), missle.getPos())
     
    def update(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.delay
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                if not ((self.player.posx - self.player.speed) <= 0):
                    self.player.moveLeft()

            if keys[pygame.K_d]:
                if not ((self.player.posx + self.player.speed + self.player.imagew) >= self.screenw):
                    self.player.moveRight()

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