import pygame
from Button import Button

class Main_Menu():
        def __init__(self, screen, screenw, screenh):
            self.title = "ScumInvaders"
            self.screen = screen
            self.screenw = screenw
            self.screenh = screenh
            self.buttons = []
            self.buttons.append(Button(self.screen, AllSprites["octo.png"], AllSprites["octo.png"], 0, 0, 32, 32))

        def draw(self):
            pass

        def update(self):
            return "Menu"