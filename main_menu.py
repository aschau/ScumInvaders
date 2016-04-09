import pygame
from button import Button

class Main_Menu():
        def __init__(self, screen, screenw, screenh, spriteList, soundManager):
            self.title = "ScumInvaders"
            self.sprites = spriteList
            self.screen = screen
            self.screenw = screenw
            self.screenh = screenh
            self.state = "Menu"
            self.buttons = []
            self.buttons.append(Button(self.screen, self.sprites.getSprite("start"), self.sprites.getSprite("startHighlighted"), 368, 442, 281, 68, "Game", 'Start Button.ogg', soundManager))
            self.buttons.append(Button(self.screen, self.sprites.getSprite("exit"), self.sprites.getSprite("exitHighlighted"), 368, 534, 281, 68, "Exit", 'Exit.ogg', soundManager))

        def draw(self):
            self.screen.blit(self.sprites.getSprite("titlescreen"), (0, 0))
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