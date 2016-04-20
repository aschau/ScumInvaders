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
            self.font = pygame.font.Font(pygame.font.match_font('comicsansms'), self.fontsize)
            self.loginButtons = []
            self.username = textInput(self.screen, "Username", (self.screenw/2 - 200, 100), self.fontsize * 8, 50, 8)
            self.password = textInput(self.screen, "Password", (self.screenw/2 - 200, 200), self.fontsize * 8, 50, 8, True)
            self.loginButtons.append(Button(screen, self.sprites.getSprite("login"), self.sprites.getSprite("loginHighlighted"), 368, 442, 281, 68, "Main", 'Start Button.ogg', soundManager))
            self.loginButtons.append(Button(screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Main", 'Exit.ogg', soundManager))

            self.mouseDelay = 100
            self.mouseNext = pygame.time.get_ticks()

            #for server
            self.serverName = 'localhost'
            self.port = 12000
            self.clientSocket = socket(AF_INET, SOCK_DGRAM)

        def draw(self):
            if self.state == "Main":
                self.screen.blit(self.sprites.getSprite("titlescreen"), (0, 0))
                for button in self.mainButtons:
                    button.draw()

            elif self.state == "Login":
                self.screen.blit(self.sprites.getSprite("titlescreenbg"), (0, 0))
                self.username.draw()
                self.password.draw()
                for button in self.loginButtons:
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
                                if self.state == "Main":
                                    message = self.username.input + ":" + self.password.input
                                    print(message)
                                    self.clientSocket.sendto(message.encode(), (self.serverName, self.port))
                                    modifiedMessage, serverAddress = self.clientSocket.recvfrom(2048)
                                    if modifiedMessage.decode() == "0": 
                                        print("Login success")
                                        self.screen.blit(self.font.render("Login is successful.", True, pygame.Color(255,255,255)),(400,self.screenh/2 - 70))
                                        pygame.time.delay(2000)
                                        #write on screen that login was successful
                                    elif modifiedMessage.decode() == "1":
                                        print("Login failed.")
                                        self.screen.blit(self.font.render("Login is successful.", True, pygame.Color(255,255,255)),(400,self.screenh/2 - 70))
                                        pygame.time.delay(2000)
                                        self.state = "Login"
                                        #write on screen that password was incorrect
                                    elif modifiedMessage.decode() == "2":
                                        print("New username")
                                        self.screen.blit(self.font.render("Login is successful.", True, pygame.Color(255,255,255)),(400,self.screenh/2 - 70))
                                        pygame.time.delay(5000)
                                        #write that new username was added   
                        
                        self.username.checkClicked(pygame.mouse.get_pos())
                        self.password.checkClicked(pygame.mouse.get_pos())
                                    
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

            else:
                return self.state

