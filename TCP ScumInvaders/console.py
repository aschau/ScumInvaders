import os, pygame
from socket import *

class console:
    def __init__(self, screen, pos, boxw, boxh, fontSize, maxLines, canEdit = False, hidden = False):
        self.screen = screen
        self.pos = pos
        self.boxw = boxw
        self.boxh = boxh
        self.fontSize = fontSize
        self.maxLines = maxLines
        self.canEdit = canEdit
        self.hidden = hidden

        self.messageList = []
        
        if self.canEdit:
            self.collider = pygame.Rect(pos[0], pos[1], boxw, boxh)
            self.selected = False
            self.messageList.append("")

        self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontSize)
        self.color = pygame.Color(0, 0, 0)
        
        

        self.keyDelay = 100
        self.nextKey = pygame.time.get_ticks()

    def draw(self):
        if not self.canEdit:
            if not self.hidden:
                for message in range(len(self.messageList)):
                    self.screen.blit(self.font.render(self.messageList[message], True, self.color), (self.pos[0] + 5, self.pos[1] + 10 + (self.font.get_linesize() * message)))
        
            else:
                for message in range(len(self.messageList)):
                    self.screen.blit(self.font.render("*" * len(self.messageList[message]), True, self.color), (self.pos[0] + 5, self.pos[1] + 10 + (self.font.get_linesize() * message)))
 
        else:
            if not self.hidden:
                if not self.selected:
                    for message in range(len(self.messageList)):
                        self.screen.blit(self.font.render(self.messageList[message], True, self.color), (self.pos[0] + 5, self.pos[1] + 10 + (self.font.get_linesize() * message)))

                else:
                    for message in range(len(self.messageList)):
                        temp = self.messageList[message]
                        if message == len(self.messageList)-1:
                            temp += "|"

                        self.screen.blit(self.font.render(temp, True, self.color), (self.pos[0] + 5, self.pos[1] + 10 + (self.font.get_linesize() * message)))

            else:
                if not self.selected:
                    for message in range(len(self.messageList)):
                        self.screen.blit(self.font.render("*" * len(self.messageList[message]), True, self.color), (self.pos[0] + 5, self.pos[1] + 10 + (self.font.get_linesize() * message)))

                else:
                    for message in range(len(self.messageList)):
                        temp = "*" * len(self.messageList[message])
                        if message == len(self.messageList)-1:
                            temp += "|"

                        self.screen.blit(self.font.render(temp, True, self.color), (self.pos[0] + 5, self.pos[1] + 10 + (self.font.get_linesize() * message)))

    def update(self):
        if not self.canEdit:
            while len(self.messageList) > self.maxLines:
                self.messageList.pop(0)

        else:
            if self.selected:
                if pygame.time.get_ticks() > self.nextKey:
                    if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                        self.messageList[-1] = self.messageList[-1][:-1]
                        if self.messageList[-1] == "" and len(self.messageList) > 1:
                            self.messageList.pop(-1)

                        self.nextKey = pygame.time.get_ticks() + self.keyDelay
            
                pygame.event.pump() 
                event = pygame.event.poll()
                if event.type == pygame.KEYDOWN:
                    if (len(self.messageList) < self.maxLines):
                        if event.unicode.isprintable():
                            if self.font.size(self.messageList[-1] + event.unicode)[0] < self.boxw:
                                self.messageList[-1] += event.unicode

                            else:
                                if event.unicode != " ":
                                    temp = self.messageList[-1]
                                    if temp.rfind(" ") != -1:
                                        self.messageList[-1] = temp[:temp.rfind(" ")]
                                        self.messageList.append(temp[temp.rfind(" ")+1:] + event.unicode)

                                else:
                                    self.messageList.append(event.unicode)

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

    def checkClicked(self, mousepos):
        if self.collider.collidepoint(mousepos):
            self.selected = True
            pygame.event.clear()
            return True
        
        else:
            self.selected = False
            return False