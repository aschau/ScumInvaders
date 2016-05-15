import pygame, os
from Button import Button

class Lobby:
        def __init__(self, screen, screenw, screenh, spriteList, soundManager):
            self.sprites = spriteList
            self.screen = screen
            self.screenw = screenw
            self.screenh = screenh
            self.soundManager = soundManager
            self.state = "Lobby"
            self.fontSize = 80
            self.font = pygame.font.Font(os.path.join('Fonts', 'BaconFarm.ttf'), self.fontSize)
            
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

        def draw(self):
            if self.state == "Lobby":
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
                self.screen.blit(self.font.render(str(self.score), True, pygame.Color(255,255,255)),(300,self.screenh/2 - 100))
                for button in self.scoreButtons:
                    button.draw()

        def update(self):
            pass

        def mouseUpdate(self):
            if pygame.time.get_ticks() >= self.mouseNext:
                if pygame.mouse.get_pressed()[0]:
                  if self.state == "Lobby":
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
                    for button in self.scoreButtons:
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