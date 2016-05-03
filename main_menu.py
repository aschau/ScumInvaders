import pygame, os
from Button import Button
from textInput import textInput
from socket import *
from Connect import Connect
import select
import json

class Main_Menu():
        def __init__(self, screen, screenw, screenh, spriteList, soundManager):
            self.sprites = spriteList
            self.screen = screen
            self.screenw = screenw
            self.screenh = screenh
            self.soundManager = soundManager
            self.state = "Main"
            self.mainButtons = []
            self.mainButtons.append(Button(self.screen, self.sprites.getSprite("login"), self.sprites.getSprite("loginHighlighted"), 368, 350, 281, 68, "Login", 'Start Button.ogg', soundManager))
            self.mainButtons.append(Button(self.screen, self.sprites.getSprite("start"), self.sprites.getSprite("startHighlighted"), 368, 442, 281, 68, "Game", 'Start Button.ogg', soundManager))
            self.mainButtons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Exit", 'Exit.ogg', soundManager))

            self.fontsize = 30
            self.lobbyFontSize = 80
            self.roomFontSize = 50
            self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontsize)
            self.lobbyFont = pygame.font.Font(os.path.join('Fonts', 'BaconFarm.ttf'), self.lobbyFontSize)
            self.roomFont = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.roomFontSize)

            self.loginButtons = []
            self.ip = textInput(self.screen, "Server IP", (self.screenw/2 - 200, 30), (self.font.get_height() * 8), 50, 15)
            self.username = textInput(self.screen, "Username", (self.screenw/2 - 200, 130), (self.font.get_height() * 8), 50, 8)
            self.password = textInput(self.screen, "Password", (self.screenw/2 - 200, 230), (self.font.get_height() * 8), 50, 8, True)
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("login"), self.sprites.getSprite("loginHighlighted"), 368, 442, 281, 68, "Lobby", 'Start Button.ogg', soundManager))
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Main", 'Exit.ogg', soundManager))

            self.lobbyButtons = []

            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyCreateButton"), self.sprites.getSprite("LobbyCreateButtonHovered"), self.screenw - 283, 225, 280, 68, "Create", 'Start Button.ogg', soundManager))
            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyEjectButton"), self.sprites.getSprite("LobbyEjectButtonHovered"), self.screenw - 283, 425, 280, 68, "Main", 'Exit.ogg', soundManager))

            self.lobbyRoomButtons = []

            self.roomButtons = []

            self.roomButtons.append(Button(self.screen, self.sprites.getSprite("ready"), self.sprites.getSprite("readyhover"), 0, self.screenh - 90, 184, 85, "Ready", 'Start Button.ogg', soundManager))
            self.roomButtons.append(Button(self.screen, self.sprites.getSprite("exitbutton"), self.sprites.getSprite("exitbuttonhover"), 220*2, self.screenh - 90, 184, 85, "Lobby", 'Exit.ogg', soundManager))
            self.roomButtons.append(Button(self.screen, self.sprites.getSprite("startbuttondisable"), self.sprites.getSprite("startbuttondisable"), 220, self.screenh - 90, 184, 85, "multiGame", 'Start Button.ogg', self.soundManager, True))

            self.rooms = []
            self.currentRoom = None
            self.currentRoomLength = 0

            self.score = 0
            self.scoreButtons = []
            self.scoreButtons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Main", 'Exit.ogg', soundManager))
            
            self.mouseDelay = 100
            self.mouseNext = pygame.time.get_ticks()
            self.host = False

            #for server
            self.socket = Connect()
            self.socket.serverName = None
            self.socket.clientSocket.settimeout(5.0)
            self.loginStatus = ""
            self.player = 1

        def draw(self):
            if self.state == "Main":
                self.screen.blit(self.sprites.getSprite("titlescreen"), (0, 0))
                for button in self.mainButtons:
                    button.draw()

            elif self.state == "Login":
                self.screen.blit(self.sprites.getSprite("titlescreenbg"), (0, 0))
                self.ip.draw()
                self.username.draw()
                self.password.draw()

                if self.loginStatus == "Invalid Password":
                    self.screen.blit(self.font.render("Wrong Password. Try again.", True, pygame.Color(255,255,255)),(300,self.screenh/2 - 100))
                elif self.loginStatus == "No Server":
                    self.screen.blit(self.font.render("The server is unavailable.", True, pygame.Color(255,255,255)),(300,self.screenh/2 - 100))
                elif self.loginStatus == "Missing Field(s)":
                    self.screen.blit(self.font.render("Missing Field(s).", True, pygame.Color(255,255,255)),(self.screenw/2 - (len("Invalid Format.") * 30)/4,self.screenh/2 - 100))
                
                for button in self.loginButtons:
                    button.draw()

            elif self.state == "Lobby":
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.sprites.getSprite("LobbyRoomBackgroundOutline"), (5, 33))
                for button in range(len(self.lobbyRoomButtons)):
                    self.lobbyRoomButtons[button].draw()
                    self.screen.blit(self.lobbyFont.render(self.lobbyRoomButtons[button].function + "'s Room " + str(len(self.rooms[button].keys())-1) + "/4", True, pygame.Color(89, 89, 89)), (self.lobbyRoomButtons[button].posx + 25, self.lobbyRoomButtons[button].posy + 10))

                for button in self.lobbyButtons:
                    button.draw()

            elif self.state == "Room":
                self.screen.blit(self.sprites.getSprite("GameRoomBackground"), (0, 0))
                for button in self.roomButtons:
                    button.draw()

                playerNumber = 0
                for room in self.rooms:
                    if room["HOST"] == self.currentRoom:
                        for player, status in room.items():
                            if player != "HOST":
                                self.screen.blit(self.sprites.getSprite("RoomNameBox"), (20, 100 * (playerNumber + 1) + self.roomFontSize * playerNumber))
                                self.screen.blit(self.roomFont.render(player, True, pygame.Color(0,0,0)),(40, 100 * (playerNumber + 1) + self.roomFontSize * playerNumber))
                                if status == True:
                                    self.screen.blit(self.sprites.getSprite("readysign"), (self.screenw/2.2, 100 * (playerNumber + 1) + self.roomFontSize * playerNumber + 10))
                                else:
                                    self.screen.blit(self.sprites.getSprite("notreadysign"), (self.screenw/2.2, 100 * (playerNumber + 1) + self.roomFontSize * playerNumber + 10))
                                playerNumber += 1
                        break
            elif self.state == "Score":
                self.screen.blit(self.sprites.getSprite("titlescreenbg"), (0,0))
                for button in self.scoreButtons:
                    button.draw()
                self.screen.blit(self.font.render(str(self.score), True, pygame.Color(255,255,255)),(300,self.screenh/2 - 100))

        def mouseUpdate(self):
            if pygame.time.get_ticks() >= self.mouseNext:
                if pygame.mouse.get_pressed()[0]:
                    if self.state == "Main":
                        for button in self.mainButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()                  
                    
                    elif self.state == "Login":
                        for button in self.loginButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                if self.state == "Lobby":
                                    if self.ip.input != "" and self.username.input != "" and self.password.input != "":
                                        message = self.username.input + ":" + self.password.input
                                        self.socket.serverName = self.ip.input

                                        try:
                                            self.socket.send("LOG:" + message)
                                            modifiedMessage, serverAddress = self.socket.clientSocket.recvfrom(2048)
                                            self.loginStatus = ""
                                            if modifiedMessage.decode() == "Invalid Password":
                                                self.loginStatus = "Invalid Password"
                                                self.state = "Login"
                                            self.socket.clientSocket.settimeout(0.0)
                                        except:
                                            self.loginStatus = "No Server"
                                            self.state = "Login"
                                    else:
                                        self.state = "Login"
                                        self.loginStatus = "Missing Field(s)"
                                else:
                                    self.loginStatus = ""
                        
                        self.ip.checkClicked(pygame.mouse.get_pos())
                        self.username.checkClicked(pygame.mouse.get_pos())
                        self.password.checkClicked(pygame.mouse.get_pos())

                    elif self.state == "Lobby":
                        for button in self.lobbyRoomButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                self.socket.send("JOIN:" + self.state)
                                for room in range(len(self.rooms)): 
                                    if self.rooms[room]["HOST"] == self.state:
                                        self.currentRoom = self.rooms[room]["HOST"]
                                self.state = "Room"

                        for button in self.lobbyButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                if self.state == "Create":
                                    self.socket.send("CREATE")
                                    self.host = True
                                    self.state = "Room"
                                    self.currentRoom = self.username.input
                     ## Message == SCORE:playerScore
                    elif self.state == "Score":
                        modifiedMessage, serverAddress = self.socket.clientSocket.recvfrom(2048)
                        data = modifiedMessage.split(":")
                        if data[0] == "SCORE":
                            self.score = int(data[1])
                        if button.checkClicked(pygame.mouse.get_pos()):
                            self.state = button.click()

                    elif self.state == "Room":
                        for button in self.roomButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                if self.state == "Ready":
                                    self.socket.send("READY:"+self.currentRoom)
                                    self.state = "Room"

                                elif self.state == "Lobby":
                                    self.socket.send("LEAVE ROOM:" + self.currentRoom)
                                    self.currentRoom = None
                                    self.host = False

                                elif self.state == "multiGame":
                                    self.socket.send("START:" + self.currentRoom)
                                    #for room in self.rooms:
                                    #    if room["HOST"] == self.currentRoom:
                                    #        self.state = "multiGame" + str(self.currentRoomLength-1) + str(list(room.keys()).index(self.username.input))
                                    #        break
                                    self.state = "Room"
                                    
                    self.mouseNext = pygame.time.get_ticks() + self.mouseDelay
        
        def update(self):
            self.mouseUpdate()
            if self.state == "Main":
                for button in self.mainButtons:
                    button.checkHover(pygame.mouse.get_pos())
            
                return "Menu"

            elif self.state == "Login":
                for button in self.loginButtons:
                    button.checkHover(pygame.mouse.get_pos())

                self.ip.update()
                self.username.update()
                self.password.update()

                return "Menu"
            
            elif self.state == "Lobby":
                try:
                    self.socket.send("REFRESH")
                    message, serverAddress = self.socket.clientSocket.recvfrom(2048)
                    modifiedMessage = message.decode()
                    self.rooms = json.loads(modifiedMessage[6:])

                    lobbyRoomButtons = []
                    for room in range(len(self.rooms)):
                        lobbyRoomButtons.append(Button(self.screen, self.sprites.getSprite("LobbyRoomButtonTemplate"), self.sprites.getSprite("LobbyRoomButtonTemplateHovered"), 17, 43 + room*100, 700, 100, self.rooms[room]["HOST"], "Start Button.ogg", self.soundManager))

                    self.lobbyRoomButtons = lobbyRoomButtons
                 
                except:
                    print("Diddly")

                for button in self.lobbyRoomButtons:
                    button.checkHover(pygame.mouse.get_pos())

                for button in self.lobbyButtons:
                    button.checkHover(pygame.mouse.get_pos())
                return "Menu"

            elif self.state == "Room":
                try:
                    self.socket.send("REFRESH")
                    message, serverAddress = self.socket.clientSocket.recvfrom(2048)
                    modifiedMessage = message.decode()
                    if modifiedMessage.split(":")[0] == "Start":
                        players = json.loads(modifiedMessage.split(":")[1])
                        players.pop(players.index("HOST"))
                        for room in self.rooms:
                            if room["HOST"] == self.currentRoom:
                                return "multiGame" + str(self.currentRoomLength-1) + str(players.index(self.username.input))
                    else:
                        self.rooms = json.loads(modifiedMessage[6:])
                    
                        for room in self.rooms:
                            if room["HOST"] == self.currentRoom:
                                self.currentRoomLength = len(room)

                        if self.host:
                            for room in self.rooms:
                                if room["HOST"] == self.currentRoom:
                                    if False in room.values():
                                        self.roomButtons[-1].disabled = True
                                        self.roomButtons[-1].current = self.sprites.getSprite("startbuttondisable")
                                        self.roomButtons[-1].image = self.sprites.getSprite("startbuttondisable")
                                        self.roomButtons[-1].sImage = self.sprites.getSprite("startbuttondisable")

                                    else:
                                        self.roomButtons[-1].disabled = False
                                        #if self.roomButtons[-1].checkHover(pygame.mouse.get_pos()):
                                        #    self.roomButtons[-1].current = self.sprites.getSprite("startbuttonhover")
                                        #else:
                                        self.roomButtons[-1].current = self.sprites.getSprite("startbutton")
                                        self.roomButtons[-1].image = self.sprites.getSprite("startbutton")
                                        self.roomButtons[-1].sImage = self.sprites.getSprite("startbuttonhover")
                                                                                
                                    break

                except:
                    print("Diddly")

                for button in self.roomButtons:
                    button.checkHover(pygame.mouse.get_pos())
                return "Menu"

            else:
                return self.state

