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
                output = self.mainMenu.update()

                #main menu returns multiplayer_number of players_player number
                #multiGame gets that spliced
                if "multiGame" in output:
                    self.screen.blit(self.AllSprites.getSprite("Loading"), (0, 0))
                    self.state = "multiGame"
                    self.multiGame = multiGame(self.screen, self.width, self.height, self.AllSprites, self.sounds, int(output[-2]), int(output[-1]))

                elif output == "Exit":
                    self.running = False

                else:
                    self.state = output
                    if output == "Game":
                        self.game.reset()

            elif (self.state == "Game"):
                self.game.draw()
                output = self.game.update()

                if output == "Exit":
                    self.running = False
            
                else:
                    self.state = output
                    if output == "Menu":
                        self.mainMenu.state = "Main"
                        self.sounds.playNewMusic('mainMenu.ogg')

            elif (self.state == "multiGame"):
                self.multiGame.draw()
                output = self.multiGame.update()

                if output == "Exit":
                    self.running = False
            
                else:
                    self.state = output
                    if output == "Menu":
                        self.mainMenu.state = "Main"
                        self.sounds.playNewMusic('mainMenu.ogg')

            self.screen.blit(self.font.render(str(int(self.clock.get_fps())), True, pygame.Color(255,255,255)), (0, 0))	
            pygame.display.update()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
	MainWindow = ScumInvaders()
	MainWindow.game_loop()
