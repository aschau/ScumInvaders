import pygame, os
from Button import Button
from textInput import textInput
from socket import *
from Connect import Connect

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
            self.lobbyFontSize = 100
            self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontsize)
            self.lobbyFont = pygame.font.Font(os.path.join('Fonts', 'BaconFarm.ttf'), self.lobbyFontSize)

            self.loginButtons = []
            self.username = textInput(self.screen, "Username", (self.screenw/2 - 200, 100), self.fontsize * 8, 50, 8)
            self.password = textInput(self.screen, "Password", (self.screenw/2 - 200, 200), self.fontsize * 8, 50, 8, True)
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("login"), self.sprites.getSprite("loginHighlighted"), 368, 442, 281, 68, "Lobby", 'Start Button.ogg', soundManager))
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Main", 'Exit.ogg', soundManager))

            self.lobbyButtons = []

            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyCreateButton"), self.sprites.getSprite("LobbyCreateButtonHovered"), self.screenw - 283, 225, 280, 68, "Create", 'Start Button.ogg', soundManager))
            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyRefreshButton"), self.sprites.getSprite("LobbyRefreshButtonHovered"), self.screenw - 283, 325, 280,68, "Refresh", 'Start Button.ogg', soundManager))
            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyEjectButton"), self.sprites.getSprite("LobbyEjectButtonHovered"), self.screenw - 283, 425, 280, 68, "Main", 'Exit.ogg', soundManager))

            self.roomButtons = []

            self.roomButtons.append(Button(self.screen, self.sprites.getSprite("ready"), self.sprites.getSprite("readyhover"), 0, self.screenh - 90, 184, 85, "Ready", 'Start Button.ogg', soundManager))
            self.roomButtons.append(Button(self.screen, self.sprites.getSprite("exitbutton"), self.sprites.getSprite("exitbuttonhover"), 220*2, self.screenh - 90, 184, 85, "Lobby", 'Exit.ogg', soundManager))

            self.players = {}

            self.mouseDelay = 100
            self.mouseNext = pygame.time.get_ticks()

            #for server
            self.socket = Connect()
            self.socket.serverName = '169.234.45.226'
            self.socket.clientSocket.settimeout(1.0)
            self.loginStatus = "IDK"
            self.player = 1
            self.host = False

        def draw(self):
            if self.state == "Main":
                self.screen.blit(self.sprites.getSprite("titlescreen"), (0, 0))
                for button in self.mainButtons:
                    button.draw()

            elif self.state == "Login":
                self.screen.blit(self.sprites.getSprite("titlescreenbg"), (0, 0))
                self.username.draw()
                self.password.draw()

                if self.loginStatus == "Invalid Password":
                    self.screen.blit(self.font.render("Wrong Password. Try again.", True, pygame.Color(255,255,255)),(300,self.screenh/2 - 100))
                elif self.loginStatus == "No Server":
                    self.screen.blit(self.font.render("The server is unavailable.", True, pygame.Color(255,255,255)),(300,self.screenh/2 - 100))
                elif self.loginStatus == "Invalid Format":
                    self.screen.blit(self.font.render("Invalid Format.", True, pygame.Color(255,255,255)),(self.screenw/2 - (len("Invalid Format.") * 30)/4,self.screenh/2 - 100))
                
                for button in self.loginButtons:
                    button.draw()

            elif self.state == "Lobby":
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.sprites.getSprite("LobbyRoomBackgroundOutline"), (5, (768 - 704)/1.5 - 10))
                for button in self.lobbyButtons:
                    button.draw()

            elif self.state == "Room":
                self.screen.blit(self.sprites.getSprite("GameRoomBackground"), (0, 0))
                for button in self.roomButtons:
                    button.draw()

                playerNumber = 0
                for player, status in self.players.items():

                    self.screen.blit(self.sprites.getSprite("RoomNameBox"), (20, 100 * (playerNumber + 1) + self.lobbyFontSize * playerNumber))
                    self.screen.blit(self.lobbyFont.render(player, True, pygame.Color(0,0,0)),(40, 100 * (playerNumber + 1) + self.lobbyFontSize * playerNumber))
                    if status == True:
                        self.screen.blit(self.sprites.getSprite("readysign"), (self.screenw/2.2, 100 * (playerNumber + 1) + self.lobbyFontSize * playerNumber + 10))
                    else:
                        self.screen.blit(self.sprites.getSprite("notreadysign"), (self.screenw/2.2, 100 * (playerNumber + 1) + self.lobbyFontSize * playerNumber + 10))
                    playerNumber += 1

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
                                    if self.username.input != "" and self.password.input != "":
                                        message = self.username.input + ":" + self.password.input

                                        self.socket.send("LOG:" + message)
                                        try:
                                            modifiedMessage, serverAddress = self.socket.clientSocket.recvfrom(2048)
                                            self.loginStatus = ""
                                            if modifiedMessage.decode() == "Invalid Password":
                                                self.loginStatus = "Invalid Password"
                                                self.state = "Login"
                                        #write on screen that password was incorrect
                                        except:
                                            self.loginStatus = "No Server"
                                            self.state = "Login"
                                    else:
                                        self.state = "Login"
                                        self.loginStatus = "Invalid Format"
                                else:
                                    self.loginStatus = ""
                        
                        self.username.checkClicked(pygame.mouse.get_pos())
                        self.password.checkClicked(pygame.mouse.get_pos())

                    elif self.state == "Lobby":
                        for button in self.lobbyButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                if self.state == "Create":
                                    self.host = True

                                    self.roomButtons.append(Button(self.screen, self.sprites.getSprite("startbutton"), self.sprites.getSprite("startbuttonhover"), 220, self.screenh - 90, 184, 85, "Game", 'Start Button.ogg', self.soundManager))
                                    self.state = "Room"
                                    self.players[self.username.input] = False
                    
                    elif self.state == "Room":
                        for button in self.roomButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                if self.state == "Ready":
                                    self.players[self.username.input] = not self.players[self.username.input]
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

                self.username.update()
                self.password.update()

                return "Menu"
            
            elif self.state == "Lobby":
                for button in self.lobbyButtons:
                    button.checkHover(pygame.mouse.get_pos())
                return "Menu"

            elif self.state == "Room":
                for button in self.roomButtons:
                    button.checkHover(pygame.mouse.get_pos())
                return "Menu"

            else:
                return self.state

