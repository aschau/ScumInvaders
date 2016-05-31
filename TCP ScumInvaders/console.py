import os, pygame
from socket import *

class console:
    def __init__(self, screen, pos, boxw, boxh, fontSize):
        self.screen = screen
        self.pos = pos
        self.boxw = boxw
        self.boxh = boxh

        self.fontSize = fontSize
        self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontSize)
        self.color = pygame.Color(0, 0, 0)
        self.messageList = []
        self.messageListMax = 20

    def draw(self):
        for message in range(len(self.messageList)):
            self.screen.blit(self.font.render(self.messageList[message], True, self.color), (self.pos[0] + 5, self.pos[1] + 10 + (self.font.get_linesize() * message)))

    def update(self):
        while len(self.messageList) > self.messageListMax:
            self.messageList.pop(0)

    def addMessage(self, message):
        if self.font.size(message)[0] < self.boxw:
            self.messageList.append(message)

        else:
            modifiedMessage = message.split(" ")
            currentLine = ""
            for word in modifiedMessage:
                tempLine = " ".join([currentLine, word])
                if self.font.size(tempLine)[0] > self.boxw:
                    self.messageList.append(currentLine)
                    currentLine = " " + word

                else:
                    currentLine = tempLine

            if self.font.size(currentLine)[0] < self.boxw and currentLine != "":
               self.messageList.append(currentLine)
