import pygame
from Button import Button

class Main_Menu():
        def __init__(self, screen, screenw, screenh, spriteList, soundManager):
            self.title = "ScumInvaders"
            self.sprites = spriteList
            self.screen = screen
            self.screenw = screenw
            self.screenh = screenh
            self.state = "Menu"
            self.buttons = []
            self.buttons.append(Button(self.screen, self.sprites["start.png"], self.sprites["exit.png"], 368, 442, 281, 68, "Start", 'Start Button.ogg', soundManager))
            self.buttons.append(Button(self.screen, self.sprites["exit.png"], self.sprites["start.png"], 368, 534, 281, 68, "Exit", 'Exit.ogg', soundManager))

        def draw(self):
            self.screen.fill((0, 0, 0, 0))
            for button in self.buttons:
                button.draw()

        def mouseUpdate(self):
            if pygame.mouse.get_pressed()[0]:
                for button in self.buttons:
                    if button.checkClicked(pygame.mouse.get_pos()):
                        return button.click()
            
            return "Menu"

        def update(self):
            for button in self.buttons:
                button.checkHover(pygame.mouse.get_pos())

            return self.mouseUpdate()