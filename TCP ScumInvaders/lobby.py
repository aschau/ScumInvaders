import pygame, os
from Button import Button
import json
from console import console

class Lobby:
        def __init__(self, screen, screenw, screenh, spriteList, soundManager, username, socket):
            self.sprites = spriteList
            self.screen = screen
            self.screenw = screenw
            self.screenh = screenh
            self.soundManager = soundManager
            self.username = username
            self.socket = socket
            self.state = "Lobby"
            self.fontSize = 80
            self.font = pygame.font.Font(os.path.join('Fonts', 'BaconFarm.ttf'), self.fontSize)
            self.roomFontSize = 50
            self.roomFont = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.roomFontSize)
            
            self.lobbyButtons = []

            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyCreateButton"), self.sprites.getSprite("LobbyCreateButtonHovered"), self.screenw - 283, 225, 280, 68, "Create", '', soundManager))
            self.lobbyButtons.append(Button(self.screen, self.sprites.getSprite("LobbyEjectButton"), self.sprites.getSprite("LobbyEjectButtonHovered"), self.screenw - 283, 425, 280, 68, "Menu", '', soundManager))

            self.lobbyRoomButtons = []

            self.roomButtons = []

            self.roomButtons.append(Button(self.screen, self.sprites.getSprite("ready"), self.sprites.getSprite("readyhover"), 0, self.screenh - 90, 184, 85, "Ready", '', soundManager))
            self.roomButtons.append(Button(self.screen, self.sprites.getSprite("exitbutton"), self.sprites.getSprite("exitbuttonhover"), 220*2, self.screenh - 90, 184, 85, "Lobby", '', soundManager))
            self.roomButtons.append(Button(self.screen, self.sprites.getSprite("startbuttondisable"), self.sprites.getSprite("startbuttondisable"), 220, self.screenh - 90, 184, 85, "multiGame", '', self.soundManager, True))

            self.rooms = {}
            self.currentRoom = None

            self.chatroom = console(self.screen, (636, 11), 367, 514, 20, 20)
            self.chatbox = console(self.screen, (636, 537), 367, 174, 20, 6, True)

            self.score = 0
            self.scoreButtons = []
            self.scoreButtons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Room", '', soundManager))
            
            self.mouseDelay = 50
            self.mouseNext = pygame.time.get_ticks()
            self.host = False
            self.socket.send("REFRESH")

        def draw(self):
            if self.state == "Lobby":
                self.screen.fill((0, 0, 0))
                self.screen.blit(self.sprites.getSprite("LobbyRoomBackgroundOutline"), (5, 33))
                for button in self.lobbyRoomButtons:
                    if button.function in self.rooms:
                        button.draw()
                        self.screen.blit(self.font.render(button.function + "'s Room " + str(len(self.rooms[button.function])) + "/4", True, pygame.Color(89, 89, 89)), (button.posx + 25, button.posy + 10))

                for button in self.lobbyButtons:
                    button.draw()

            elif self.state == "Room":
                self.screen.blit(self.sprites.getSprite("GameRoomBackground"), (0, 0))
                self.chatroom.draw()
                self.chatbox.draw()

                for button in self.roomButtons:
                    button.draw()

                if self.currentRoom in self.rooms:
                    playerNumber = 0
                    for player, status in self.rooms[self.currentRoom].items():
                        if player != "HOST":
                            self.screen.blit(self.sprites.getSprite("RoomNameBox"), (20, 100 * (playerNumber + 1) + self.roomFontSize * playerNumber))
                            self.screen.blit(self.roomFont.render(player, True, pygame.Color(0,0,0)),(40, 100 * (playerNumber + 1) + self.roomFontSize * playerNumber))
                            if status[0] == False or status[1] == "Game":
                                self.screen.blit(self.sprites.getSprite("notreadysign"), (self.screenw/2.2, 100 * (playerNumber + 1) + self.roomFontSize * playerNumber + 10))
                        
                            else:
                                self.screen.blit(self.sprites.getSprite("readysign"), (self.screenw/2.2, 100 * (playerNumber + 1) + self.roomFontSize * playerNumber + 10))

                            playerNumber += 1
                        
            elif self.state == "Score":
                self.screen.blit(self.sprites.getSprite("titlescreenbg"), (0,0))
                self.screen.blit(self.font.render(str(self.score), True, pygame.Color(255,255,255)),(300,self.screenh/2 - 100))
                for button in self.scoreButtons:
                    button.draw()

        def update(self):
            self.mouseUpdate()
            if self.state == "Lobby":                    
                modifiedMessage = self.socket.receive()

                if modifiedMessage != "" and modifiedMessage != None:
                    self.socket.send("REFRESH")
                    if modifiedMessage[:5] == "Lobby":
                        self.rooms = json.loads(modifiedMessage[6:])

                        if self.currentRoom in self.rooms.keys():
                            self.state = "Room"
                        
                        lobbyRoomButtons = []
                        rooms = list(self.rooms.keys())
                        for room in range(len(rooms)):
                            lobbyRoomButtons.append(Button(self.screen, self.sprites.getSprite("LobbyRoomButtonTemplate"), self.sprites.getSprite("LobbyRoomButtonTemplateHovered"), 17, 43 + room*100, 700, 100, rooms[room], "Start Button.ogg", self.soundManager))

                        self.lobbyRoomButtons = lobbyRoomButtons
                
                for button in self.lobbyRoomButtons:
                    button.checkHover(pygame.mouse.get_pos())

                for button in self.lobbyButtons:
                    button.checkHover(pygame.mouse.get_pos())
                
                return "Lobby"
            
            elif self.state == "Score":
                for button in self.scoreButtons:
                    button.checkHover(pygame.mouse.get_pos())

                return "Lobby"

            elif self.state == "Room":
                #try:
                   
                modifiedMessage = self.socket.receive()

                if modifiedMessage != "" and modifiedMessage != None:
                    self.socket.send("REFRESH")
                    splitMessage = modifiedMessage.split(":")
                    if splitMessage[0] == "START":
                        players = json.loads(modifiedMessage.split(":")[1])
                        return "multiGame" + str(len(players)) + str(players.index(self.username.input))

                    elif splitMessage[0] == "ROOM":
                        self.currentRoom = splitMessage[1]
                        if splitMessage[1] == self.username.input:
                            self.host = True

                    elif splitMessage[0] == "CHAT":
                        self.chatroom.addMessage(modifiedMessage[5:])

                    elif modifiedMessage[:5] == "Lobby":
                        self.rooms = json.loads(modifiedMessage[6:])
                        if self.currentRoom in self.rooms:

                        #print(self.rooms)

                            if self.host:
                                statuses = list(self.rooms[self.currentRoom].values())
                                if [False, "Room"] in statuses or [False, "Game"] in statuses or [True, "Game"] in statuses:
                                    self.roomButtons[-1].disabled = True
                                    self.roomButtons[-1].current = self.sprites.getSprite("startbuttondisable")
                                    self.roomButtons[-1].image = self.sprites.getSprite("startbuttondisable")
                                    self.roomButtons[-1].sImage = self.sprites.getSprite("startbuttondisable")

                                else:
                                    self.roomButtons[-1].disabled = False
                                    self.roomButtons[-1].current = self.sprites.getSprite("startbutton")
                                    self.roomButtons[-1].image = self.sprites.getSprite("startbutton")
                                    self.roomButtons[-1].sImage = self.sprites.getSprite("startbuttonhover")
                                                                                
                #except Exception as error:
                #    print(error)

                for button in self.roomButtons:
                    button.checkHover(pygame.mouse.get_pos())

                self.chatroom.update()
                output = self.chatbox.update()
                if output != None:
                    self.chatroom.addMessage(self.username.input + ": " + output)
                    self.socket.send("CHAT:" + self.username.input + ": " + output)

                return "Lobby"

            else:
                return self.state


        def mouseUpdate(self):
            if pygame.time.get_ticks() >= self.mouseNext:
                if pygame.mouse.get_pressed()[0]:
                    if self.state == "Lobby":
                        for button in self.lobbyRoomButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                self.socket.send("JOIN:" + self.state)
                                self.currentRoom = self.state
                                self.state = "Room"

                        for button in self.lobbyButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                if self.state == "Create":
                                    self.socket.send("CREATE")
                                    self.host = True
                                    self.state = "Lobby"
                                    self.currentRoom = self.username.input
                
                    ## Message == SCORE:playerScore
                    elif self.state == "Score":
                        for button in self.scoreButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()

                    elif self.state == "Room":
                        for button in self.roomButtons:
                            if button.checkClicked(pygame.mouse.get_pos()):
                                self.state = button.click()
                                if self.state == "Ready":
                                    self.socket.send("READY")
                                    self.state = "Room"

                                elif self.state == "Lobby":
                                    self.socket.send("LEAVE ROOM")
                                    self.chatroom = console(self.screen, (636, 11), 367, 514, 20, 20)
                                    self.chatbox = console(self.screen, (636, 537), 367, 174, 20, 6, True)
                                    self.currentRoom = None
                                    self.host = False

                                elif self.state == "multiGame":
                                    self.socket.send("START")
                                    self.state = "Room"
                                    
                        self.chatbox.checkClicked(pygame.mouse.get_pos())

                    self.mouseNext = pygame.time.get_ticks() + self.mouseDelay