import os, sys
import pygame
from pygame.locals import *
import resources

if not pygame.font:
    print('Warning, fonts disabled')

if not pygame.mixer:
    print('Warning, sound disabled')

class ScumInvaders:
    def __init__(self):
        pygame.init()
        self.width = resources.width
        self.height = resources.height
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.clock = pygame.time.Clock()

        self.fontsize = 10
        self.font = pygame.font.Font(pygame.font.match_font('comicsansms'), self.fontsize)

    def game_loop(self):
        while resources.running:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                            resources.running = False
            
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.font.render(str(int(self.clock.get_fps())), True, pygame.Color(255,255,255)), (0, 0))	
            self.screen.blit(resources.AllSprites["octo.png"], (100, 500))		
            pygame.display.update()
            self.clock.tick_busy_loop(60)
        
        pygame.quit()

if __name__ == "__main__":
	MainWindow = ScumInvaders()
	MainWindow.game_loop()
