#their stuff
import os, sys
import pygame
from pygame.locals import *

#our stuff
from main_menu import Main_Menu
from Sprite_Manager import sprites
from soundManager import soundManager
from game import game
from multiplayer import multiGame
from lobby import Lobby
#server stuff
from socket import *

#in case gg no has fonts/sound
if not pygame.font:
    print('Warning, fonts disabled')

if not pygame.mixer:
    print('Warning, sound disabled')

'''
initializes the game window and sets the scenes 
game loop can be found here
self.clock -> to set frames per seconds so it isn't infinitely fast
'''
class ScumInvaders:
    def __init__(self):
        pygame.init()
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.screen.blit(sprites("Sprites").load("Loading"), (0, 0))
        pygame.display.update()
        self.running = True

        self.AllSprites = sprites("Sprites")
        self.AllSprites.loadAll()

        self.clock = pygame.time.Clock()
        self.state = "Menu"
        self.sounds = soundManager("Sound")
        self.mainMenu = Main_Menu(self.screen, self.width, self.height, self.AllSprites, self.sounds)
        self.game = game(self.screen, self.width, self.height, self.AllSprites, self.sounds)
        
        self.lobby = None
        self.multiGame = None

        self.fontsize = 10
        self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontsize)

        pygame.event.set_blocked(pygame.NOEVENT)
        
    def game_loop(self):
        while self.running:

            pygame.event.pump()
            if pygame.event.peek(pygame.QUIT):
                    self.running = False

            if (self.state == "Menu"):
                self.mainMenu.draw()
                self.state = self.mainMenu.update()

                if self.state == "Exit":
                    self.running = False
                
                elif self.state == "Lobby":
                    self.mainMenu.state = "Login"
                    self.lobby = Lobby(self.screen, self.width, self.height, self.AllSprites, self.sounds, self.mainMenu.username, self.mainMenu.socket)
                    self.sounds.playNewMusic('lobby (Final).ogg')


                elif self.state == "Game":
                    self.game.reset()
            
            elif (self.state == "Lobby"):
                self.lobby.draw()
                output = self.lobby.update()
                if "multiGame" in output:
                    self.screen.blit(self.AllSprites.getSprite("Loading"), (0, 0))
                    self.state = "multiGame"
                    self.multiGame = multiGame(self.screen, self.width, self.height, self.AllSprites,\
                        self.sounds, int(output[-2]), int(output[-1]), self.mainMenu.ip.input, self.lobby.currentRoom, self.lobby.socket)

                else:
                    if output == "Menu":
                        self.sounds.playNewMusic('mainMenu.ogg')
                        self.mainMenu.socket.send("STOP")
                        self.mainMenu.state = "Login"
                        self.mainMenu.connected = False
                        self.mainMenu.loginPressed = False
                        self.mainMenu.loginStatus = ""

                    self.state = output

            elif (self.state == "Game"):
                self.game.draw()
                self.state = self.game.update()

                if self.state == "Exit":
                    self.running = False
            
                elif self.state == "Menu":
                    self.mainMenu.state = "Main"
                    self.sounds.playNewMusic('mainMenu.ogg')

            elif (self.state == "multiGame"):
                self.multiGame.draw()
                self.state = self.multiGame.update()

                if self.state == "Exit":
                    self.running = False

                elif self.state == "Score":
                    self.state = "Lobby"
                    self.lobby.state = "Score"
                    self.lobby.score = self.multiGame.playerList[self.multiGame.clientPlayerNum].score
                    self.sounds.playNewMusic('mainMenu.ogg')
                    
                elif self.state == "Lobby":
                    self.lobby.state = "Room"
                    self.sounds.playNewMusic('lobby (Final).ogg')

            self.screen.blit(self.font.render(str(int(self.clock.get_fps())), True, pygame.Color(255,255,255)), (0, 0))	
            pygame.display.update()
            self.clock.tick(60)
        
        try:
            self.mainMenu.socket.send("STOP")
            pygame.quit()

        except:
            pass

if __name__ == "__main__":
    MainWindow = ScumInvaders()
    MainWindow.game_loop()
