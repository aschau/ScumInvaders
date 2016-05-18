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
            self.ip = textInput(self.screen, "Server IP", (50, 30), (self.font.get_height() * 8), 50, 15)
            self.port = textInput(self.screen, "Port", (300 + (self.font.get_height() * 8),  30), (self.font.get_height() * 5), 50, 5)
            self.username = textInput(self.screen, "Username", (self.screenw/2 - 200, 130), (self.font.get_height() * 8), 50, 8)
            self.password = textInput(self.screen, "Password", (self.screenw/2 - 200, 230), (self.font.get_height() * 8), 50, 8, True)
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("login"), self.sprites.getSprite("loginHighlighted"), 368, 442, 281, 68, "Lobby", 'Start Button.ogg', soundManager))
            self.loginButtons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Main", 'Exit.ogg', soundManager))

            self.mouseDelay = 50
            self.mouseNext = pygame.time.get_ticks()
            self.connected = False

            #for server
            self.socket = None
            self.loginStatus = ""

        def draw(self):
            if self.state == "Main":
                self.screen.blit(self.sprites.getSprite("titlescreen"), (0, 0))
                for button in self.mainButtons:
                    button.draw()

            elif self.state == "Login":
                self.screen.blit(self.sprites.getSprite("titlescreenbg"), (0, 0))
                self.ip.draw()
                self.port.draw()
                self.username.draw()
                self.password.draw()

                if self.loginStatus == "Invalid Password":
                    self.screen.blit(self.font.render("Wrong Password. Try again.", True, pygame.Color(255,255,255)),(300,self.screenh/2 - 100))
                elif self.loginStatus == "No Server":
                    self.screen.blit(self.font.render("Could not reach server. Wrong Info/Poor connection.", True, pygame.Color(255,255,255)),(100,self.screenh/2 - 100))
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
                                if self.state == "Menu":
                                    self.connected = False
                                    self.socket.send("STOP")

                                if self.state == "Lobby":
                                    if self.ip.input != "" and self.port.input != "" and self.username.input != "" and self.password.input != "":
                                        message = self.username.input + ":" + self.password.input

                                        try:
                                            if not self.connected:
                                                self.socket = Connect(self.ip.input, int(self.port.input))
                                                self.connected = True

                                            if self.connected:
                                                self.socket.send("LOG:" + message)
                                                modifiedMessage = None
                                                while modifiedMessage == None:
                                                    modifiedMessage = self.socket.receive()
                                                    
                                                modifiedMessage = modifiedMessage.split(":")

                                                self.loginStatus = ""
                                                if modifiedMessage[0] == "Invalid Password":
                                                    self.loginStatus = "Invalid Password"
                                                    self.state = "Login"

                                                elif modifiedMessage[0] == "Success":
                                                    self.connected = False
                                                    self.state = "Lobby"

                                                else:
                                                    self.state = "Login"

                                        except Exception as error:
                                            print(error)
                                            self.loginStatus = "No Server"
                                            self.state = "Login"

                                    else:
                                        self.state = "Login"
                                        self.loginStatus = "Missing Field(s)"
                                else:
                                    self.loginStatus = ""
                                    #self.loginPressed = False                  
                        
                        self.ip.checkClicked(pygame.mouse.get_pos())
                        self.port.checkClicked(pygame.mouse.get_pos())
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
                if self.connected and self.loginStatus == "No Server":
                    try:
                        self.socket.send("CHECKLOG")
                        
                        modifiedMessage = None
                        while modifiedMessage == None:
                            modifiedMessage = self.socket.receive()

                        modifiedMessage = modifiedMessage.split(":")

                        self.loginStatus = ""
                        if modifiedMessage[0] == "Invalid Password":
                            self.loginStatus = "Invalid Password"
                            self.state = "Login"
                    
                        elif modifiedMessage[0] == "Success":
                            self.loginStatus = ""
                            self.connected = False
                            self.state = "Lobby"

                    except Exception as error:
                        print(error)
                        self.loginStatus = "No Server"
                        self.state = "Login"

                for button in self.loginButtons:
                    button.checkHover(pygame.mouse.get_pos())

                self.ip.update()
                self.port.update()
                self.username.update()
                self.password.update()

                return "Menu"
            
            else:
                return self.state

