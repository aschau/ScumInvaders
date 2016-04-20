import pygame, os
from player import Player
from enemy import Enemy
from Button import Button
from Sprite_Manager import Animate
from collections import deque
import random
from datetime import datetime

'''
initializes score, enemyCount, enemyGrid, missile count, and level here 
functions:
    self.setGrid(speed, health) - sets the grid for Enemy placement and their initialized values
    self.draw() - draws onto the screen 
    self.update()
    self.togglePause() - still needs work but means to pause the screen
    self.checkState() - checks whether scene has changed (eg. Menu)
    self.checkPlayerLives() 
    self.checkEnemyCount()
    self.nextLevel() - called at the end of every level when checkEnemyCount() == 0
    self.keyUpdate() - for key presses
    self.checkMissiles() - checks to see if hit something/out of screen
    self.backgroundUpdate() - scrolls background

'''
class game:
    def __init__(self, screen, screenw, screenh, spriteList, soundManager):
        self.sprites = spriteList
        self.screen = screen
        self.screenw = screenw
        self.screenh = screenh
        self.soundManager = soundManager
        self.player = Player(1, "shipupgrade1", "missile5", (500, 700), 32, 32)
        self.paused = False
        self.level = 1

        self.background = "GameBackground"
        self.background2 = "GameBackground"
        self.enemyGrid = []
        self.enemyRowCount = 5

        self.enemyColumnCount = 10
        self.enemyCount = 50

        #self.player.score = 0

        self.setGrid()       
        self.missiles = []

        self.missileDelay = 100

        self.enemyDelay = 100
        self.enemyFireChance = 100
        self.nextMissile = pygame.time.get_ticks() + self.missileDelay
        self.nextEnemyMove = pygame.time.get_ticks() + self.enemyDelay

        self.bgHeight = 1536
        self.currentBG1Height = 0
        self.currentBG2Height = -self.bgHeight

        self.state = "Game"
        self.keyDelay = 500
        self.nextKeyInput = pygame.time.get_ticks()

        self.fontsize = 30
        self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontsize)

        self.pauseButtons = []
        self.pauseButtons.append(Button(screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 330, 281, 68, "Menu", 'Exit.ogg', soundManager))
        
        self.mouseDelay = 100
        self.mouseNext = pygame.time.get_ticks()

        random.seed(datetime.now())

    def reset(self):
        self.soundManager.playNewMusic("Space Invaders Theme.ogg");
        self.player = Player(1, "shipupgrade1", "missile5", (500, 700), 32, 32)
        self.enemyGrid = []
        self.missiles = []
        self.enemyCount = 50
        self.setGrid()
        self.level = 1
        self.player.score = 0
        self.state = "Game"
        self.paused = False

    def setGrid(self, speed = 16, health = 1):
         for row in range(self.enemyRowCount):
            self.enemyGrid.append([])
            for column in range(self.enemyColumnCount):
                rnum = random.randint(1, 100)
                enemySprite = "Alien1SpriteSheet"
                if rnum <= 45:
                    enemySprite = "Alien2SpriteSheet"

                elif rnum >= 90 and rnum < 98:
                    enemySprite = "Alien3SpriteSheet"

                elif rnum >= 98:
                    enemySprite = "Alien4SpriteSheet"

                self.enemyGrid[row].append(Enemy((32 + (column * 96), (row * 64) - self.enemyRowCount * 64), 32, 32, Animate(self.sprites.getSprite(enemySprite), 2, 2, 32, 32, 10), health, speed, row, column, enemySprite))

    def draw(self):
        self.screen.blit(self.sprites.getSprite(self.background), (0, self.currentBG1Height))
        self.screen.blit(self.sprites.getSprite(self.background2), (0, self.currentBG2Height))
        self.screen.blit(self.sprites.getSprite(self.player.image), self.player.getPos())
        
        for missile in self.missiles:
            self.screen.blit(self.sprites.getSprite(missile.image), missile.getPos())
     
        for row in range(self.enemyRowCount):
            for column in range(self.enemyColumnCount):
                self.enemyGrid[row][column].anim.draw(self.screen, self.enemyGrid[row][column].getPos())

        self.screen.blit(self.font.render("Lives: " + str(self.player.lives), True, pygame.Color(255,255,255)), (0, 670))
        self.screen.blit(self.font.render("Ammo: " + str(self.player.missileCap - self.player.missileCount), True, pygame.Color(255,255,255)), (0, 670 + self.fontsize))
        self.screen.blit(self.font.render("Score: " + str(self.player.score), True, pygame.Color(255,255,255)),(0,670 + (self.fontsize * 2)))
        self.screen.blit(self.font.render("Level: " + str(self.level), True, pygame.Color(255,255,255)), (0, 670 - self.fontsize))

        if self.paused:
            for button in self.pauseButtons:
                button.draw()

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

        else:
            return self.mouseUpdate()

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
            if self.enemyFireChance > 20:
                self.enemyFireChance -= 2;
            self.setGrid(16 + self.level/2, self.level/2)
        else: 
            self.setGrid(16 + (self.level -1)/2, self.level//2 + 1)
            

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
        
        if pygame.time.get_ticks() > self.nextKeyInput:
            if keys[pygame.K_ESCAPE]:
                self.togglePause()
                self.nextKeyInput = pygame.time.get_ticks() + self.keyDelay

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
    
    def mouseUpdate(self):
        for button in self.pauseButtons:
            button.checkHover(pygame.mouse.get_pos())

        if pygame.time.get_ticks() >= self.mouseNext:
            if pygame.mouse.get_pressed()[0]:
                for button in self.pauseButtons:
                    if button.checkClicked(pygame.mouse.get_pos()):
                        return button.click()
                                    
                self.mouseNext = pygame.time.get_ticks() + self.mouseDelay

        return "Game"

    def checkHit(self, numMissiles):
        for row in range(self.enemyRowCount):
            for column in range(self.enemyColumnCount):
                if self.enemyGrid[row][column].health != 0:
                    if self.enemyGrid[row][column].collider.colliderect(self.missiles[numMissiles].collider):
                        attacker = self.missiles.pop(numMissiles).owner
                        self.enemyGrid[row][column].health -= 1
                        self.player.missileCount -= 1
                        if self.enemyGrid[row][column].health == 0 and not self.enemyGrid[row][column].dead:
                            self.enemyGrid[row][column].dead = True
                            self.enemyGrid[row][column].anim = Animate(self.sprites.getSprite(self.enemyGrid[row][column].type[:6] + "DeathSpriteSheet"), 3, 3, 32, 32, 2, False)
                            self.enemyCount -= 1
                            if self.enemyGrid[row][column].type == "Alien4SpriteSheet":
                                self.player.score += (100  * self.level) * 10
                           
                            elif self.enemyGrid[row][column].type != "Alien3SpriteSheet":
                                self.player.score += (100  * self.level) * 2

                            else:
                                self.player.score += 100 * self.level
                        return


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
                    self.checkHit(numMissiles)
                                
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
                    
                    rNum2 = random.randint(1,self.enemyFireChance)
                    if rNum2 == 1:
                        if (self.enemyGrid[row][column].health != 0 and self.enemyGrid[row][column].missileCount < self.enemyGrid[row][column].missileCap):
                            self.missiles.append(self.enemyGrid[row][column].fire())

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
                        if self.enemyGrid[row][column].posx + self.enemyGrid[row][column].imagew >= 1024:
                            self.enemyGrid[row][column].lastMove = "Left"
                            self.enemyGrid[row][column].moveDown()
                           # self.enemyGrid[row][column].moveLeft()
                        else:
                            self.enemyGrid[row][column].moveRight()
            
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
            rnum = random.randint(1,3)
        
            if rnum == 1:
                self.background = "GameBackground"
            elif rnum == 2:
                self.background = "GameBackground2"
            else:
                self.background = "GameBackground3"
        elif (self.currentBG2Height >= self.bgHeight):
            self.currentBG2Height = -self.bgHeight

            rnum = random.randint(1,3)
        
            if rnum == 1:
                self.background2 = "GameBackground"
            elif rnum == 2:
                self.background2 = "GameBackground2"
            else:
                self.background2 = "GameBackground3"
