import pygame
from player import Player
from enemy import Enemy
from Button import Button
from Sprite_Manager import Animate
from collections import deque
import random

class game:
    def __init__(self, screen, screenw, screenh, spriteList, soundManager):
        self.sprites = spriteList
        self.screen = screen
        self.screenw = screenw
        self.screenh = screenh
        self.soundManager = soundManager
        self.player = Player(1, "ship1", "missile2", (500, 700), 32, 32)
        self.paused = False
        self.level = 1

        self.enemyGrid = []
        self.enemyRowCount = 5

        self.enemyColumnCount = 10
        self.enemyCount = 50

        self.score = 0

        self.setGrid()       
        self.missiles = []

        self.missileDelay = 100

        self.enemyDelay = 100
        self.nextMissile = pygame.time.get_ticks() + self.missileDelay
        self.nextEnemyMove = pygame.time.get_ticks() + self.enemyDelay

        self.bgHeight = 1536
        self.currentBG1Height = 0
        self.currentBG2Height = -self.bgHeight

        self.state = "Game"
        self.keyDelay = 10
        self.nextKeyInput = pygame.time.get_ticks() + self.keyDelay

        self.fontsize = 30
        self.font = pygame.font.Font(pygame.font.match_font('comicsansms'), self.fontsize)

    def reset(self):
        self.soundManager.playNewMusic("Space Invaders Theme.ogg");
        self.player = Player(1, "ship1", "missile2", (500, 700), 32, 32)
        self.enemyGrid = []
        self.missiles = []
        self.enemyCount = 50
        self.setGrid()
        self.state = "Game"

    def setGrid(self, speed = 16, health = 1):
         for row in range(self.enemyRowCount):
            self.enemyGrid.append([])
            for column in range(self.enemyColumnCount):
                rnum = random.randint(1, 2)
                enemySprite = "Alien1SpriteSheet"
                if rnum == 1:
                    enemySprite = "Alien2SpriteSheet"
                self.enemyGrid[row].append(Enemy((32 + (column * 96), (row * 64) - self.enemyRowCount * 64), 32, 32, Animate(self.sprites.getSprite(enemySprite), 2, 2, 32, 32, 10), health, speed))

    def draw(self):
        self.screen.blit(self.sprites.getSprite("GameBackground"), (0, self.currentBG1Height))
        self.screen.blit(self.sprites.getSprite("GameBackground"), (0, self.currentBG2Height))
        self.screen.blit(self.sprites.getSprite(self.player.image), self.player.getPos())
        
        for missile in self.missiles:
            self.screen.blit(self.sprites.getSprite(missile.image), missile.getPos())
     
        for row in range(self.enemyRowCount):
            for column in range(self.enemyColumnCount):
                if self.enemyGrid[row][column].health != 0:
                    self.enemyGrid[row][column].anim.draw(self.screen, self.enemyGrid[row][column].getPos())

        self.screen.blit(self.font.render("Lives: " + str(self.player.lives), True, pygame.Color(255,255,255)), (0, 670))
        self.screen.blit(self.font.render("Ammo: " + str(self.player.missileCap - self.player.missileCount), True, pygame.Color(255,255,255)), (0, 670 + self.fontsize))
        self.screen.blit(self.font.render("Score: " + str(self.score), True, pygame.Color(255,255,255)),(0,670 + (self.fontsize * 2)))

    def update(self):
        self.keyUpdate()
        if not self.paused:
            self.backgroundUpdate()
            self.state = self.enemyUpdate()
        
            if self.checkState():
                return self.state
        
            self.checkMissiles()

            self.state = self.checkPlayerLives()
            if self.checkState():
                return self.state
        
            self.checkEnemyCount()

        return self.state
    
    def togglePause(self):
        self.paused = not self.paused

    def checkState(self):
        return self.state != "Game"

    def checkPlayerLives(self):
        if (self.player.lives <= 0):
            return "Menu"
        return "Game"

    def checkEnemyCount(self):
        if self.enemyCount == 0:
            self.enemyCount = 50
            self.nextLevel()

    '''Odd levels -> change speed; even levels -> change health'''
    def nextLevel(self):
        self.enemyGrid = []
        self.level += 1
        if self.level % 2 == 0:
            self.setGrid(16 + self.level * 5, self.level/2)
        else: 
            self.setGrid(16 + (self.level -1) * 5, self.level//2 + 1)
        #for row in range(self.enemyRowCount):
        #        for column in range(self.enemyColumnCount):
        #            if self.level % 2 == 0:
        #                self.enemyGrid[row][column].speed += self.level * 5
        #            else: 
        #                rnum = random.randint(self.level - 1, self.level)
        #                self.enemyGrid[row][column].health = rnum
        if self.level %2 == 1:
            self.player.missileCap += 1 

    def keyUpdate(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:
            self.togglePause()

        if not self.paused:
            if keys[pygame.K_a]:
                    if not ((self.player.posx - self.player.speed) <= 0):
                        self.player.moveLeft()

            if keys[pygame.K_d]:
                if not ((self.player.posx + self.player.speed + self.player.imagew) >= self.screenw):
                    self.player.moveRight()

            if pygame.time.get_ticks() > self.nextMissile:
                self.nextMissile = pygame.time.get_ticks() + self.missileDelay

                if keys[pygame.K_SPACE]:
                    if self.player.missileCount < self.player.missileCap:
                        self.missiles.append(self.player.fire())

    def checkMissiles(self):
        numMissiles = 0
        while numMissiles < len(self.missiles):
            self.missiles[numMissiles].update()

            attacker = self.missiles[numMissiles].owner
            if attacker == 1:
                if ((self.missiles[numMissiles].posy - self.missiles[numMissiles].imageh) <= 0):
                    self.missiles.pop(numMissiles)
                    self.player.missileCount -= 1

                else:
                    hit = False
                    for row in range(self.enemyRowCount):
                        for column in range(self.enemyColumnCount):
                            if self.enemyGrid[row][column].health != 0:
                                #try:
                                if (numMissiles != len(self.missiles)):
                                    if self.enemyGrid[row][column].collider.colliderect(self.missiles[numMissiles].collider):
                                        hit = True
                                        attacker = self.missiles.pop(numMissiles).owner
                                        self.enemyGrid[row][column].health -= 1
                                        #checks if no more enemies 
                                        if self.enemyGrid[row][column].health == 0: 
                                            self.enemyCount -= 1
                                            self.score += 100
                                #except:
                                #    print("Num:", numMissiles)
                                #    print("Length:", len(self.missiles))
                                #    print("Row:", row, "column:", column)
                    
                    if hit:                
                        self.player.missileCount -= 1
                                
            
            elif attacker == 0:
                if (self.missiles[numMissiles].collider.colliderect(self.player.collider)):
                    self.player.lives -= 1
                    enemyGridPos = self.missiles.pop(numMissiles).getEnemyPos()
                    self.enemyGrid[enemyGridPos[0]][enemyGridPos[1]].missileCount -= 1

                elif ((self.missiles[numMissiles].posy + self.missiles[numMissiles].imageh) >= self.screenh):
                    enemyGridPos = self.missiles.pop(numMissiles).getEnemyPos()
                    self.enemyGrid[enemyGridPos[0]][enemyGridPos[1]].missileCount -= 1

            numMissiles += 1

    def enemyUpdate(self):
        if pygame.time.get_ticks() > self.nextEnemyMove:
            self.nextEnemyMove = pygame.time.get_ticks() + self.enemyDelay


            for row in range(self.enemyRowCount):
                for column in range(self.enemyColumnCount):
                    if self.enemyGrid[row][column].health != 0 and (self.enemyGrid[row][column].posy + 32 >= 768 or (self.enemyGrid[row][column].posy + 32 > self.player.posy and self.player.posx < self.enemyGrid[row][column].posx < self.player.posx + 64)) :
                        self.togglePause()

                        return "Menu"
                    
                    self.enemyGrid[row][column].anim.update()
                    if self.enemyGrid[row][column].lastMove == None:
                        if row % 2 == 0:
                            self.enemyGrid[row][column].lastMove = "Left"
                        else: 
                            self.enemyGrid[row][column].lastMove = "Right"
                        self.enemyGrid[row][column].moveDown()
                        self.enemyGrid[row][column].moveDown()
                        self.enemyGrid[row][column].moveDown()
                        #print("This happened.")
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
                    
                    rNum2 = random.randint(1,100)
                    if rNum2 == 1:
                        if (self.enemyGrid[row][column].health != 0 and self.enemyGrid[row][column].missileCount < self.enemyGrid[row][column].missileCap):
                            self.missiles.append(self.enemyGrid[row][column].fire())
            
            #rNum = random.randint(1, 5)
            #for row in range(self.enemyRowCount):
            #    for column in range(self.enemyColumnCount):
                    ##checks if enemies have reached the bottom of the screen
                    #if self.enemyGrid[row][column].posy + 32 >= 768 or (self.enemyGrid[row][column].posy + 32 > self.player.posy and self.player.posx < self.enemyGrid[row][column].posx < self.player.posx + 64) :
                    #    return "Menu"
            #        if self.enemyGrid[row][column].health != 0:
            #            if rNum >= 3:
            #                self.enemyGrid[row][column].lastMove = "Down"
            #                self.enemyGrid[row][column].moveDown() 

            #            elif rNum == 1:
            #                if (self.enemyGrid[row][column].posx - 16 >= 0) and self.enemyGrid[row][column].lastMove != "Left":
            #                    self.enemyGrid[row][column].lastMove = "Left"
            #                    self.enemyGrid[row][column].moveLeft()
                        
            #            elif rNum == 2:
            #                if ((self.enemyGrid[row][column].posx + 16 + self.enemyGrid[row][column].imagew) <= self.screenw) and self.enemyGrid[row][column].lastMove != "Right":
            #                    self.enemyGrid[row][column].lastMove = "Right"
            #                    self.enemyGrid[row][column].moveRight() 
                      
        return "Game"

    def backgroundUpdate(self):
        self.currentBG1Height += 1
        self.currentBG2Height += 1
        
        if (self.currentBG1Height >= self.bgHeight):
            self.currentBG1Height = -self.bgHeight
        elif (self.currentBG2Height >= self.bgHeight):
            self.currentBG2Height = -self.bgHeight