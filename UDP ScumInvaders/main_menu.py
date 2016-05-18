import pygame, os
from Button import Button
from textInput import textInput
from socket import *
from Connect import Connect
import select
import json
import sqlite3

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
            self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontsize)

            self.loginButtons = []
            self.ip = textInput(self.screen, "Server IP", (self.screenw/2 - 200, 30), (self.font.get_height() * 8), 50, 15)
            self.username = textInput(self.screen, "Username", (self.screenw/2 - 200, 130), (self.font.get_height() * 8), 50, 8)
            self.password = textInput(self.screen, "Password", (self.screenw/2 - 200, 230), (self.font.get_height() * 8), 50, 8, True)
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("login"), self.sprites.getSprite("loginHighlighted"), 368, 442, 281, 68, "Lobby", 'Start Button.ogg', soundManager))
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Main", 'Exit.ogg', soundManager))

            self.mouseDelay = 50
            self.mouseNext = pygame.time.get_ticks()
            self.loginPressed = False

            #for server
            self.socket = Connect()
            self.socket.serverName = None
            self.socket.clientSocket.settimeout(0.0)
            self.loginStatus = ""

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
                    self.screen.blit(self.font.render("Waiting for server. Double check info.", True, pygame.Color(255,255,255)),(300,self.screenh/2 - 100))
                elif self.loginStatus == "Missing Field(s)":
                    self.screen.blit(self.font.render("Missing Field(s).", True, pygame.Color(255,255,255)),(self.screenw/2 - (len("Invalid Format.") * 30)/4,self.screenh/2 - 100))
                
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
                                if self.state == "Lobby":
                                    self.loginPressed = True
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

                                        except:
                                            self.loginStatus = "No Server"
                                            self.state = "Login"

                                    else:
                                        self.state = "Login"
                                        self.loginStatus = "Missing Field(s)"
                                else:
                                    self.loginStatus = ""
                                    self.loginPressed = False                  
                        
                        self.ip.checkClicked(pygame.mouse.get_pos())
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
                if self.loginPressed:
                    try:
                        message = self.username.input + ":" + self.password.input
                        self.socket.send("LOG:" + message)
                        modifiedMessage, serverAddress = self.socket.clientSocket.recvfrom(2048)
                        self.loginStatus = ""
                
                        if modifiedMessage.decode() == "Invalid Password":
                            self.loginStatus = "Invalid Password"
                            self.state = "Login"
                    
                        elif modifiedMessage.decode() == "Success":
                            self.state = "Lobby"

                    except:
                        self.loginStatus = "No Server"
                        self.state = "Login"

                for button in self.loginButtons:
                    button.checkHover(pygame.mouse.get_pos())

                self.ip.update()
                self.username.update()
                self.password.update()

                return "Menu"
            
            else:
                return self.state

