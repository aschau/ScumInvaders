import pygame
from Button import Button
from textInput import textInput

class login:
    def __init__(self, screen, screenw, screenh, spriteList, soundManager):
        self.screen = screen
        self.screenw = screenw
        self.screenh = screenh
        self.spriteList = spriteList
        self.soundManager = soundManager
        self.fontsize = 30
        self.username = textInput(self.screen, "Username", (self.screenw/2 - 200, 100), self.fontsize * 8, 50, 8)
        self.password = textInput(self.screen, "Password", (self.screenw/2 - 200, 200), self.fontsize * 8, 50, 8)
        self.buttons = []
        self.buttons.append(Button(screen, self.spriteList.getSprite("start"), self.spriteList.getSprite("startHighlighted"), 368, 442, 281, 68, "Room", 'Start Button.ogg', soundManager))
        self.buttons.append(Button(screen, self.spriteList.getSprite("exit"), self.spriteList.getSprite("exitHighlighted"), 368, 534, 281, 68, "Menu", 'Exit.ogg', soundManager))
        self.mouseDelay = 100
        self.mouseNext = pygame.time.get_ticks() + self.mouseDelay

    def draw(self):
        self.screen.blit(self.spriteList.getSprite("titlescreenbg"), (0, 0))
        self.username.draw()
        self.password.draw()
        for button in self.buttons:
                button.draw()
    
    def mouseUpdate(self):
        if pygame.time.get_ticks() >= self.mouseNext:
            if pygame.mouse.get_pressed()[0]:
                for button in self.buttons:
                    if button.checkClicked(pygame.mouse.get_pos()):
                        return button.click()
                
                self.username.checkClicked(pygame.mouse.get_pos())
                self.password.checkClicked(pygame.mouse.get_pos())

                self.mouseNext = pygame.time.get_ticks() + self.mouseDelay
            
        return "Login"

    def update(self):
        for button in self.buttons:
            button.checkHover(pygame.mouse.get_pos())

        self.username.update()
        self.password.update()
        return self.mouseUpdate()