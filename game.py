import pygame
from player import Player
from enemy import Enemy
from button import Button

class game:
    def __init__(self, screen, screenw, screenh, spriteList, soundManager):
        self.sprites = spriteList
        self.screen = screen
        self.screenw = screenw
        self.screenh = screenh
        self.soundManager = soundManager
        self.player = Player("ship1", "missleimage", (500, 700), 32, 32)

        enemyGrid = []
        enemyRowCount = 5
        enemyColumnCount = 11

        for row in range(enemyRowCount):
            enemyGrid.append([])
            for enemy in range(enemyColumnCount):
                enemyGrid[row].append(Enemy())
        
        self.missles = []

        self.wait = 50
        self.next = pygame.time.get_ticks() + self.wait

    def draw(self):
        self.screen.blit(self.sprites.getSprite("GameBackground"), (0, 0))
        self.screen.blit(self.sprites.getSprite(self.player.image), self.player.getPos())
        
        for missle in missles:
            self.screen.blit(missle.image, missle.getPos())
     
    def update(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.wait
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                if not ((self.player.posx - self.player.speed) <= 0):
                    self.player.moveLeft()

            if keys[pygame.K_d]:
                if not ((self.player.posx + self.player.speed + self.player.imagew) >= self.screenw):
                    self.player.moveRight()

            if keys[pygame.K_SPACE]:
                self.missles.append(self.player.fire())


        for missle in range(len(missles)):
            missles[missle].update()
            if ((missles[missle].posy - missles[missle].imageh) >= 0):
                missles.pop(missle)

        return "Game"