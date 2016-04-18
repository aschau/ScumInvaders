#their shit
import os, sys
import pygame
from pygame.locals import *

#our shit
from main_menu import Main_Menu
from Sprite_Manager import sprites
from soundManager import soundManager
from game import game

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
        self.running = True

        AllSprites = sprites("Sprites")
        AllSprites.loadAll()

        self.clock = pygame.time.Clock()
        self.state = "Menu"
        self.sounds = soundManager("Sound")
        self.mainMenu = Main_Menu(self.screen, self.width, self.height, AllSprites, self.sounds)
        self.game = game(self.screen, self.width, self.height, AllSprites, self.sounds)

        self.fontsize = 10
        self.font = pygame.font.Font(pygame.font.match_font('comicsansms'), self.fontsize)
        
    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            self.running = False

            if (self.state == "Menu"):
                self.mainMenu.draw()
                output = self.mainMenu.update()

                if output == "Exit":
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

            self.screen.blit(self.font.render(str(int(self.clock.get_fps())), True, pygame.Color(255,255,255)), (0, 0))	
            pygame.display.update()
            if (self.state != "Menu"):
                self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
	MainWindow = ScumInvaders()
	MainWindow.game_loop()
