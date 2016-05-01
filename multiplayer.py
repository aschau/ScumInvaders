import pygame, os
from player import Player
from enemy import Enemy
from Button import Button
from Sprite_Manager import Animate
from collections import deque
import random
from datetime import datetime
from socket import *
from Connect import Connect

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
class multiGame:

    def __init__(self, screen, screenw, screenh, spriteList, soundManager, numPlayers, clientPlayerNum, ip, hostName):
        self.sprites = spriteList
        self.hostName = hostName
        self.clientPlayerNum = int(clientPlayerNum)
        self.numPlayers = int(numPlayers)
        self.screen = screen
        self.screenw = screenw 
        self.screenh = screenh
        self.soundManager = soundManager
        self.playerList = []
        self.playerList.append(Player(1, "ship1", "missile1", (300, 700), 32, 32))
        if numPlayers > 1:
            self.playerList.append(Player(2, "ship2", "missile2", (400, 700), 32, 32))

        if numPlayers > 2:
            self.playerList.append(Player(3, "ship3", "missle3", (500, 700), 32, 32))

        if numPlayers > 3:
            self.playerList.append(Player(4, "ship4", "missle4", (600, 700), 32, 32))
        
        self.paused = False
        self.start = True
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

        self.state = "multiGame"
        self.keyDelay = 500
        self.nextKeyInput = pygame.time.get_ticks()

        self.fontsize = 30
        self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontsize)

        self.pauseButtons = []
        self.pauseButtons.append(Button(screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 330, 281, 68, "Menu", 'Exit.ogg', soundManager))
        
        self.mouseDelay = 100
        self.mouseNext = pygame.time.get_ticks()

        #for server
        self.socket = Connect()

        self.socket.serverName = ip
        self.socket.clientSocket.setblocking(False)

        random.seed(datetime.now())
        self.startTime = pygame.time.get_ticks()

    #def reset(self, numPlayers):
    #    self.numPlayers = numPlayers
    #    self.playerList = []
    #    self.playerList.append(Player(1, "ship1", "missile1", (300, 700), 32, 32))

    #    if numPlayers > 1:
    #        self.playerList.append(Player(2, "ship2", "missile2", (400, 700), 32, 32))

    #    if numPlayers > 2:
    #        self.playerList.append(Player(3, "ship3", "missle3", (500, 700), 32, 32))

    #    if numPlayers > 3:
    #        self.playerList.append(Player(4, "ship4", "missle4", (600, 700), 32, 32))

    #    self.enemyGrid = []
    #    self.missiles = []
    #    self.enemyCount = 50
    #    self.setGrid()
    #    self.level = 1
    #    self.playerList[self.clientPlayerNum].score = 0
    #    self.state = "multiGame"
    #    self.paused = False
    #    self.start = True
    #    self.startTime = pygame.time.get_ticks()

    #Creates the grid for the enemies in the game
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
        for player in self.playerList:
            self.screen.blit(self.sprites.getSprite(player.image), player.getPos())
        
        for missile in self.missiles:
            self.screen.blit(self.sprites.getSprite(missile.image), missile.getPos())
     
        for row in range(self.enemyRowCount):
            for column in range(self.enemyColumnCount):
                self.enemyGrid[row][column].anim.draw(self.screen, self.enemyGrid[row][column].getPos())

        self.screen.blit(self.font.render("Lives: " + str(self.playerList[self.clientPlayerNum].lives), True, pygame.Color(255,255,255)), (0, 670))
        self.screen.blit(self.font.render("Ammo: " + str(self.playerList[self.clientPlayerNum].missileCap - self.playerList[self.clientPlayerNum].missileCount), True, pygame.Color(255,255,255)), (0, 670 + self.fontsize))
        self.screen.blit(self.font.render("Score: " + str(self.playerList[self.clientPlayerNum].score), True, pygame.Color(255,255,255)),(0,670 + (self.fontsize * 2)))
        self.screen.blit(self.font.render("Level: " + str(self.level), True, pygame.Color(255,255,255)), (0, 670 - self.fontsize))

        if self.paused:
            for button in self.pauseButtons:
                button.draw()

    #Handles everything that needs to go on in the game
    def update(self):
        try:
            message, serverAddress = self.socket.clientSocket.recvfrom(2048)
            modifiedMessage = message.decode()
            print(modifiedMessage)
        except:
            print("Nada")

        if self.start:
            if pygame.time.get_ticks() >= self.startTime + 100:
                self.soundManager.playSound("Enemy_entrance.ogg")
                pygame.time.delay(2000)
                self.soundManager.playNewMusic("Space Invaders Theme.ogg", .2)
                self.start = False

        self.keyUpdate()
        #if not self.paused:
        self.backgroundUpdate()
        self.state = self.enemyUpdate()

        if self.checkState():
            return self.state
        
        self.checkMissiles()

        self.state = self.checkPlayerLives()
        if self.checkState():
            return self.state
        
        self.checkEnemyCount()

        if self.paused:
            return self.mouseUpdate()

        return self.state
    
    def togglePause(self):
        self.paused = not self.paused

    def checkState(self):
        return self.state != "multiGame"

    def checkPlayerLives(self):
        #if (self.playerList[self.clientPlayerNum].lives <= 0):
        #    return "Room"
        return "multiGame"

    def checkEnemyCount(self):
        if self.enemyCount == 0:
            self.enemyCount = 50
            self.nextLevel()

    '''Odd levels -> change speed; even levels -> change health'''
    def nextLevel(self):   
        self.enemyGrid = []
        self.level += 1

        if self.level == 5:
            self.soundManager.playSound("LevelUp.ogg")
            self.playerList[self.clientPlayerNum].image = "ship1upgrade2"    

        elif self.level == 10:
            self.soundManager.playSound("LevelUp.ogg")
            self.playerList[self.clientPlayerNum].image = "ship1upgrade3"

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
            self.playerList[self.clientPlayerNum].missileCap += 1 

    #Handles all of the keypresses (Movement, Shooting and pause)
    def keyUpdate(self):
        keys = pygame.key.get_pressed()
        
        if pygame.time.get_ticks() > self.nextKeyInput:
            if keys[pygame.K_ESCAPE]:
                self.togglePause()
                self.nextKeyInput = pygame.time.get_ticks() + self.keyDelay

        if not self.paused:
            if keys[pygame.K_a]:
                    if not ((self.playerList[self.clientPlayerNum].posx - self.playerList[self.clientPlayerNum].speed) <= 0):
                        self.playerList[self.clientPlayerNum].moveLeft()
                        self.socket.send("MOV:" + self.hostName + ":" + str(self.clientPlayerNum) + ":" + str((self.playerList[self.clientPlayerNum].posx, self.playerList[self.clientPlayerNum].posy)))


            if keys[pygame.K_d]:
                if not ((self.playerList[self.clientPlayerNum].posx + self.playerList[self.clientPlayerNum].speed + self.playerList[self.clientPlayerNum].imagew) >= self.screenw):
                    self.playerList[self.clientPlayerNum].moveRight()
                    self.socket.send("MOV:" + self.hostName + ":" + str(self.clientPlayerNum) +  ":" + str((self.playerList[self.clientPlayerNum].posx, self.playerList[self.clientPlayerNum].posy)))

            if pygame.time.get_ticks() > self.nextMissile:
                self.nextMissile = pygame.time.get_ticks() + self.missileDelay

                if keys[pygame.K_SPACE]:
                    if self.playerList[self.clientPlayerNum].missileCount < self.playerList[self.clientPlayerNum].missileCap:
                        self.missiles.append(self.playerList[self.clientPlayerNum].fire())
                        self.soundManager.playSound("Player_Shoot.ogg")

    #Only used in the pause menu, captures the clicks from the mouse on the pause screen 
    def mouseUpdate(self):
        for button in self.pauseButtons:
            button.checkHover(pygame.mouse.get_pos())

        if pygame.time.get_ticks() >= self.mouseNext:
            if pygame.mouse.get_pressed()[0]:
                for button in self.pauseButtons:
                    if button.checkClicked(pygame.mouse.get_pos()):
                        return button.click()
                                    
                self.mouseNext = pygame.time.get_ticks() + self.mouseDelay

        return "multiGame"

    def checkHit(self, numMissiles):
        for row in range(self.enemyRowCount):
            for column in range(self.enemyColumnCount):
                if self.enemyGrid[row][column].health != 0:
                    if self.enemyGrid[row][column].collider.colliderect(self.missiles[numMissiles].collider):
                        attacker = self.missiles.pop(numMissiles).owner
                        self.enemyGrid[row][column].health -= 1
                        self.socket.send("HIT:" + "ENEMY:" + str(row) + ":" + str(column))
                        self.playerList[self.clientPlayerNum].missileCount -= 1
                        if self.enemyGrid[row][column].health == 0 and not self.enemyGrid[row][column].dead:
                            self.enemyGrid[row][column].dead = True
                            self.socket.send("DEATH:" + "ENEMY:" + str(row) + ":" + str(column))
                            self.enemyGrid[row][column].anim = Animate(self.sprites.getSprite(self.enemyGrid[row][column].type[:6] + "DeathSpriteSheet"), 3, 3, 32, 32, 2, False)
                            self.enemyCount -= 1
                            if self.enemyGrid[row][column].type == "Alien4SpriteSheet":
                                self.playerList[self.clientPlayerNum].score += (100  * self.level) * 10
                           
                            elif self.enemyGrid[row][column].type != "Alien3SpriteSheet":
                                self.playerList[self.clientPlayerNum].score += (100  * self.level) * 2

                            else:
                                self.playerList[self.clientPlayerNum].score += 100 * self.level
                        return

    #Handles the effects of the missles from both players(1) and enemies(0)
    def checkMissiles(self):
        numMissiles = 0
        while numMissiles < len(self.missiles):
            self.missiles[numMissiles].update()

            attacker = self.missiles[numMissiles].owner
            #1 is the player's missle shots
            if attacker == 1:
                if ((self.missiles[numMissiles].posy - self.missiles[numMissiles].imageh) <= 0):
                    self.socket.send("SHOOT:" + str(self.clientPlayerNum))
                    self.missiles.pop(numMissiles)
                    self.playerList[self.clientPlayerNum].missileCount -= 1

                else:
                    self.checkHit(numMissiles)
            #0 is the enemy's missle shots                    
            elif attacker == 0:
                if (self.missiles[numMissiles].collider.colliderect(self.playerList[self.clientPlayerNum].collider)):
                    self.playerList[self.clientPlayerNum].lives -= 1
                    self.socket.send("HIT:" + str(self.clientPlayerNum))
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
                    if self.enemyGrid[row][column].health != 0 and (self.enemyGrid[row][column].posy + 32 >= 768 or (self.enemyGrid[row][column].posy + 32 > self.playerList[self.clientPlayerNum].posy and self.playerList[self.clientPlayerNum].posx < self.enemyGrid[row][column].posx < self.playerList[self.clientPlayerNum].posx + 64)) :
                        self.togglePause()

                        return "Menu"
                    
                    self.enemyGrid[row][column].anim.update()
                    
                    rNum2 = random.randint(1,self.enemyFireChance)
                    if rNum2 == 1:
                        if (self.enemyGrid[row][column].health != 0 and self.enemyGrid[row][column].missileCount < self.enemyGrid[row][column].missileCap):
                            self.socket.send("SHOOT:" + "ENEMY:" + str(row) + ":" + str(column))
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
        return "multiGame"

    #scrolls through the background
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
