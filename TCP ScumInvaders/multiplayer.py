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
from missile import Missile
import json
import sqlite3

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

    def __init__(self, screen, screenw, screenh, spriteList, soundManager, numPlayers, clientPlayerNum, ip, hostName, socket):
        self.sprites = spriteList
        self.hostName = hostName
        self.clientPlayerNum = clientPlayerNum
        self.numPlayers = numPlayers
        self.screen = screen
        self.screenw = screenw 
        self.screenh = screenh
        self.soundManager = soundManager
        self.playerList = []
        self.playerList.append(Player(0, "ship1", "missile1", (300, 700), 32, 32))
        if numPlayers > 1:
            self.playerList.append(Player(1, "ship2", "missile2", (400, 700), 32, 32))

        if numPlayers > 2:
            self.playerList.append(Player(2, "ship3", "missile3", (500, 700), 32, 32))

        if numPlayers > 3:
            self.playerList.append(Player(3, "ship4", "missile4", (600, 700), 32, 32))
        
        self.paused = False
        self.start = True
        self.level = 1

        self.background = "GameBackground"
        self.background2 = "GameBackground"
        self.enemyGrid = []
        self.serverGridInfo = {}
        self.enemyRowCount = 5

        self.enemyColumnCount = 10
        self.enemyCount = 50

        #self.player.score = 0

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
        self.pauseButtons.append(Button(screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 330, 281, 68, "Lobby", 'Exit.ogg', soundManager))
        
        self.mouseDelay = 100
        self.mouseNext = pygame.time.get_ticks()

        self.serverReady = False
        random.seed(datetime.now())
        self.startTime = pygame.time.get_ticks()

        #for server
        self.socket = socket

    #Creates the grid for the enemies in the game
    def setGrid(self, speed = 16, health = 1):
        rNums = self.serverGridInfo["TYPES"]
        for row in range(self.enemyRowCount):
            self.enemyGrid.append([])
            for column in range(self.enemyColumnCount):
                rnum = rNums[row][column]
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
      
        if self.serverReady:
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

        message = self.socket.receive()

        #if "ENEMYGRID" in modifiedMessage:
        #    data = json.loads(modifiedMessage[10:])
        #    self.readGrid(data)

        modifiedMessage = message.split(":")
        #print(modifiedMessage)
        if message[:4] == "GRID":
            self.serverGridInfo = json.loads(message[5:])
            self.setGrid()

        if modifiedMessage[0] == "GAMESTART":
            self.serverReady = True

        elif modifiedMessage[0]  == "MOV":
            if int(modifiedMessage[1]) != self.clientPlayerNum:
                self.playerList[int(modifiedMessage[1])].posx = int(modifiedMessage[2])


        elif modifiedMessage[0] == "SHOOT":
            if int(modifiedMessage[3]) != self.clientPlayerNum:
                self.missiles.append(Missile(int(modifiedMessage[3]), self.playerList[int(modifiedMessage[3])].missileImage, (int(modifiedMessage[1]) + self.playerList[int(modifiedMessage[3])].imagew - 18, int(modifiedMessage[2]) - self.playerList[int(modifiedMessage[3])].imageh),8, 32)) #(self.playerList[int(modifiedMessage[3])].posx + (self.playerList[int(modifiedMessage[3])].imagew - 18), self.playerList[int(modifiedMessage[3])].posy - (self.playerList[int(modifiedMessage[3])].imageh)), 8, 32))


        elif modifiedMessage[0] == "HIT":
            if modifiedMessage[2] == "ENEMY":
                self.enemyGrid[int(modifiedMessage[3])][int(modifiedMessage[4])].health -= 1
                if self.enemyGrid[int(modifiedMessage[3])][int(modifiedMessage[4])].health == 0 and not self.enemyGrid[int(modifiedMessage[3])][int(modifiedMessage[4])].dead:
                    self.enemyGrid[int(modifiedMessage[3])][int(modifiedMessage[4])].dead = True
                    #self.socket.send("DEATH:" + self.hostName + ":" + "ENEMY:" + str(row) + ":" + str(column))
                    self.enemyGrid[int(modifiedMessage[3])][int(modifiedMessage[4])].anim = Animate(self.sprites.getSprite(self.enemyGrid[int(modifiedMessage[3])][int(modifiedMessage[4])].type[:6] + "DeathSpriteSheet"), 3, 3, 32, 32, 2, False)
                    self.enemyCount -= 1

        if self.serverReady:
            if self.start:
                if pygame.time.get_ticks() >= self.startTime + 100:
                    self.soundManager.playSound("Enemy_entrance.ogg")
                    pygame.time.delay(2000)
                    self.soundManager.playNewMusic("ScumInvadersTheme(Final).ogg", .2)
                    self.start = False

            self.state = self.enemyUpdate()

            if self.checkState():
                return self.state
            self.checkEnemyCount()


        
        self.keyUpdate()
        self.backgroundUpdate()
        self.checkMissiles()
        self.state = self.checkPlayerLives()

        if self.checkState():
            return self.state

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
        #return "multiGame"
        if (self.playerList[self.clientPlayerNum].lives <= 0):
            self.socket.send("SCORE:" + self.hostName + ":" + str(self.playerList[self.clientPlayerNum].score))
            return "Score"
        return "multiGame"

    def checkEnemyCount(self):
        if self.enemyCount == 0:
            self.enemyCount = 50
            self.nextLevel()

    '''Odd levels -> change speed; even levels -> change health'''
    def nextLevel(self):   
        self.enemyGrid = []
        if self.clientPlayerNum == 0:
            self.socket.send("SETGRID:" + self.hostName + ":" + str(self.enemyRowCount) + ":" + str(self.enemyColumnCount))
        
        tryGrid = True
        while tryGrid:
            try:

                self.socket.send("GETGRIDTYPES:" + self.hostName)
                modifiedMessage = self.socket.receive()
                modifiedMessage = message.decode().split(":")
                if modifiedMessage[0] == "GRID":
                    self.setGrid(modifiedMessage[1:])
                    tryGrid = False
            except:
                tryGrid = True
        self.level += 1

        if self.level == 5:
            self.soundManager.playSound("LevelUp.ogg")

            for player in range(len(self.playerList)):
                self.playerList[player].image = "ship" + str(player+1) + "upgrade2"    

        elif self.level == 10:
            self.soundManager.playSound("LevelUp.ogg")
            
            for player in range(len(self.playerList)):
                self.playerList[player].image = "ship" + str(player+1) + "upgrade3"

        if self.level % 2 == 0:
            if self.enemyFireChance > 20:
                self.enemyFireChance -= 2;
            self.setGrid(modifiedMessage[1:], 16 + self.level/2, self.level/2)
        else: 
            self.setGrid(modifiedMessage[1:], 16 + (self.level -1)/2, self.level//2 + 1)
            
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

                    self.socket.send("MOV:" + self.hostName + ":" + str(self.clientPlayerNum) + ":" + str(self.playerList[self.clientPlayerNum].posx))


            if keys[pygame.K_d]:
                if not ((self.playerList[self.clientPlayerNum].posx + self.playerList[self.clientPlayerNum].speed + self.playerList[self.clientPlayerNum].imagew) >= self.screenw):
                    self.playerList[self.clientPlayerNum].moveRight()

                    self.socket.send("MOV:" + self.hostName + ":" + str(self.clientPlayerNum) + ":" + str(self.playerList[self.clientPlayerNum].posx))

            if pygame.time.get_ticks() > self.nextMissile:
                self.nextMissile = pygame.time.get_ticks() + self.missileDelay

                if keys[pygame.K_SPACE]:
                    if self.playerList[self.clientPlayerNum].missileCount < self.playerList[self.clientPlayerNum].missileCap:
                        self.socket.send("SHOOT:" + self.hostName + ":" + str(self.playerList[self.clientPlayerNum].posx) + ":" + str(self.playerList[self.clientPlayerNum].posy) + ":" + str(self.clientPlayerNum))
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

                if self.enemyGrid[row][column].health > 0:
                    if self.enemyGrid[row][column].collider.colliderect(self.missiles[numMissiles].collider):
                        attacker = self.missiles.pop(numMissiles).owner
                        if attacker == self.clientPlayerNum:
                            self.enemyGrid[row][column].health -= 1
                            self.socket.send("HIT:" + self.hostName + ":" + "ENEMY:" + str(row) + ":" + str(column))
                            self.playerList[attacker].missileCount -= 1
                            if self.enemyGrid[row][column].health == 0 and not self.enemyGrid[row][column].dead:
                                self.enemyGrid[row][column].dead = True
                                #self.socket.send("DEATH:" + self.hostName + ":" + "ENEMY:" + str(row) + ":" + str(column))
                                self.enemyGrid[row][column].anim = Animate(self.sprites.getSprite(self.enemyGrid[row][column].type[:6] + "DeathSpriteSheet"), 3, 3, 32, 32, 2, False)
                                self.enemyCount -= 1
                                if self.enemyGrid[row][column].type == "Alien4SpriteSheet":
                                    self.playerList[self.clientPlayerNum].score += (100  * self.level) * 10

                                elif self.enemyGrid[row][column].type != "Alien3SpriteSheet":
                                    self.playerList[self.clientPlayerNum].score += (100  * self.level) * 2

                                else:
                                    self.playerList[self.clientPlayerNum].score += 100 * self.level
                            return
                        

    #Handles the effects of the missiles from both players(1) and enemies(-1)
    def checkMissiles(self):
        numMissiles = 0
        while numMissiles < len(self.missiles):
            self.missiles[numMissiles].update()

            attacker = self.missiles[numMissiles].owner

            #1 is the player's missile shots

            if attacker == self.clientPlayerNum:
                if ((self.missiles[numMissiles].posy + self.missiles[numMissiles].imageh) <= 0):
                    #self.socket.send("SHOOT:" + self.hostName + ":" + str(self.clientPlayerNum))
                    self.missiles.pop(numMissiles)
                    self.playerList[attacker].missileCount -= 1

                else:
                    self.checkHit(numMissiles)

            #-1 is the enemy's missile shots                    
            elif attacker == -1:
                if (self.missiles[numMissiles].collider.colliderect(self.playerList[self.clientPlayerNum].collider)):
                    self.playerList[self.clientPlayerNum].lives -= 1
                    self.socket.send("HIT:" + str(self.clientPlayerNum))
                    enemyGridPos = self.missiles.pop(numMissiles).getEnemyPos()
                    self.enemyGrid[enemyGridPos[0]][enemyGridPos[1]].missileCount -= 1

                elif ((self.missiles[numMissiles].posy) >= self.screenh):
                    enemyGridPos = self.missiles.pop(numMissiles).getEnemyPos()
                    self.enemyGrid[enemyGridPos[0]][enemyGridPos[1]].missileCount -= 1

            numMissiles += 1

    def enemyUpdate(self):
        if pygame.time.get_ticks() > self.nextEnemyMove:
            self.nextEnemyMove = pygame.time.get_ticks() + self.enemyDelay

            for row in range(self.enemyRowCount):
                for column in range(self.enemyColumnCount):

                    if (self.enemyGrid[row][column].posy + 32 >= 768 or (self.enemyGrid[row][column].posy + 32 > self.playerList[self.clientPlayerNum].posy and self.playerList[self.clientPlayerNum].posx < self.enemyGrid[row][column].posx < self.playerList[self.clientPlayerNum].posx + 64)) :
                        self.togglePause()

                        return "Menu"
                    
                    self.enemyGrid[row][column].anim.update()
                    
                    rNum2 = random.randint(1,self.enemyFireChance)
                    if rNum2 == 1:

                        if (self.enemyGrid[row][column].health > 0 and self.enemyGrid[row][column].missileCount < self.enemyGrid[row][column].missileCap):
                            #self.socket.send("SHOOT:" + "ENEMY:" + str(row) + ":" + str(column))
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
