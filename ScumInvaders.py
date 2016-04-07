import os, sys
import pygame
from pygame.locals import *
from main_menu import Main_Menu
from Sprite_Manager import SpriteSheets
from soundManager import soundManager

if not pygame.font:
    print('Warning, fonts disabled')

if not pygame.mixer:
    print('Warning, sound disabled')

class ScumInvaders:
    def __init__(self):
        pygame.init()
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.running = True

        AllSprites = SpriteSheets("Sprites").loadAll()

        self.clock = pygame.time.Clock()
        self.state = "Menu"
        self.sounds = soundManager("Sound")
        self.mainMenu = Main_Menu(self.screen, self.width, self.height, AllSprites, self.sounds)

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
            
            self.screen.blit(self.font.render(str(int(self.clock.get_fps())), True, pygame.Color(255,255,255)), (0, 0))	
            pygame.display.update()
            self.clock.tick_busy_loop(60)
        
        pygame.quit()

if __name__ == "__main__":
	MainWindow = ScumInvaders()
	MainWindow.game_loop()
