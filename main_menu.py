import pygame
from Button import Button

class Main_Menu():
        def __init__(self, screen, screenw, screenh, spriteList):
            self.title = "ScumInvaders"
            self.sprites = spriteList
            self.screen = screen
            self.screenw = screenw
            self.screenh = screenh
            self.buttons = []
            self.buttons.append(Button(self.screen, self.sprites["start.png"], self.sprites["start.png"], 368, 442, 281, 68))
            self.buttons.append(Button(self.screen, self.sprites["exit.png"], self.sprites["exit.png"], 368, 534, 281, 68))

        def draw(self):
            self.screen.fill((0, 0, 0, 0))
            for button in self.buttons:
                button.draw()

        def mouseUpdate(self):
            if pygame.mouse.get_pressed()[0]:
                for button in self.buttons:
                    button.check(pygame.mouse.get_pos(), True)

        def update(self):
            for button in self.buttons:
                button.check(pygame.mouse.get_pos())

            return "Menu"