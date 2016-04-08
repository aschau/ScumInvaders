import pygame
from player import Player
from enemy import Enemy
from button import Button

class game:
    def __init__(self, screen, screenw, screenh, spriteList, soundManager):
        self.sprites = spriteList
        self.screen = screen
        self.screenw = screenw
        self.screenh = screenh
        self.soundManager = soundManager
        
        enemyGrid = []
        enemyRowCount = 5
        enemyColumnCount = 11

        for row in range(enemyRowCount):
            enemyGrid.append([])
            for enemy in range(enemyColumnCount):
                enemyGrid[row].append(Enemy())

    def draw(self):
        self.screen.fill((0, 0, 0, 0))
     
    def update(self):
        return "Game"