import pygame, os
from Button import Button
from textInput import textInput
from socket import *

class Main_Menu():
        def __init__(self, screen, screenw, screenh, spriteList, soundManager):
            self.sprites = spriteList
            self.screen = screen
            self.screenw = screenw
            self.screenh = screenh
            self.state = "Main"
            self.mainButtons = []
            self.mainButtons.append(Button(self.screen, self.sprites.getSprite("login"), self.sprites.getSprite("loginHighlighted"), 368, 350, 281, 68, "Login", 'Start Button.ogg', soundManager))
            self.mainButtons.append(Button(self.screen, self.sprites.getSprite("start"), self.sprites.getSprite("startHighlighted"), 368, 442, 281, 68, "Game", 'Start Button.ogg', soundManager))
            self.mainButtons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Exit", 'Exit.ogg', soundManager))

            self.fontsize = 30
            self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontsize)
            self.loginButtons = []
            self.username = textInput(self.screen, "Username", (self.screenw/2 - 200, 100), self.fontsize * 8, 50, 8)
            self.password = textInput(self.screen, "Password", (self.screenw/2 - 200, 200), self.fontsize * 8, 50, 8, True)
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("login"), self.sprites.getSprite("loginHighlighted"), 368, 442, 281, 68, "Lobby", 'Start Button.ogg', soundManager))
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Main", 'Exit.ogg', soundManager))

            self.lobbyButtons = []

            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyCreateButton"), self.sprites.getSprite("LobbyCreateButtonHovered"), self.screenw - 300, 175, 280, 68, "Create", 'Start Button.ogg', soundManager))
            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyJoinButton"), self.sprites.getSprite("LobbyJoinButtonHovered"), self.screenw - 300, 275, 280, 68, "Room", 'Start Button.ogg', soundManager))
            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyRefreshButton"), self.sprites.getSprite("LobbyRefreshButtonHovered"), self.screenw - 300, 375, 280,68, "Refresh", 'Start Button.ogg', soundManager))
            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyEjectButton"), self.sprites.getSprite("LobbyEjectButtonHovered"), self.screenw - 300, 475, 280, 68, "Main", 'Exit.ogg', soundManager))


            self.mouseDelay = 100
            self.mouseNext = pygame.time.get_ticks()

            #for server
            self.serverName = 'localhost'
            self.port = 12000
            self.clientSocket = socket(AF_INET, SOCK_DGRAM)

            self.loginStatus = "IDK"
            self.player = 1

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
                for button in self.loginButtons:
                    button.draw()

            elif self.state == "Lobby":
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.sprites.getSprite("LobbyRoomBackground"), (5, (768 - 704)/1.5))
                for button in self.lobbyButtons:
                    button.draw()

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
                                    message = self.username.input + ":" + self.password.input
                                    print(message)
                                    try:
                                        self.clientSocket.sendto(message.encode(), (self.serverName, self.port))
                                        modifiedMessage, serverAddress = self.clientSocket.recvfrom(2048)
                                        if modifiedMessage.decode() == "Invalid Password":
                                            print("Login failed.")
                                            self.loginStatus = "Invalid Password"
                                            self.state = "Login"
                                        #write on screen that password was incorrect
                                    except:
                                        self.loginStatus = "No Server"
                                        self.state = "Login"

                                    
                        
                        self.username.checkClicked(pygame.mouse.get_pos())
                        self.password.checkClicked(pygame.mouse.get_pos())

                    elif self.state == "Lobby":
                        for button in self.lobbyButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                    
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

            else:
                return self.state

