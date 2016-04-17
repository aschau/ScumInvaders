import pygame
from Button import Button

class login:
    def __init__(self, screen, screenw, screenh, spriteList, soundManager):
        self.screen = screen
        self.screenw = screenw
        self.screenh = screenh
        self.spriteList = spriteList
        self.soundManager = soundManager
        self.launch = Button(screen, self.spriteList.getSprite("start"), self.spriteList.getSprite("startHighlighted"), 368, 442, 281, 68, "Room", 'Start Button.ogg', soundManager)
