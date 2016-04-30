import pygame
import os

class textInput:
    #self.screen = screen
    #title = Username/Password/Etc.
    #pos = (x, y) = where the 
    #boxw, h = box width, height
    def __init__(self, screen, title, pos, boxw, boxh, maxLength, hidden = False):
        self.screen = screen
        self.title = title + ":"
        self.selected = False
        self.hidden = hidden
        self.fontsize = 30
        self.maxLength = maxLength
        self.colliderX = pos[0] + (self.fontsize * len(self.title)/1.5)
        self.collider = pygame.Rect(self.colliderX, pos[1], boxw, boxh)
        self.pos = pos
        self.boxw = boxw
        self.boxh = boxh
        self.font = pygame.font.Font(os.path.join('Fonts', 'nasalization-rg.ttf'), self.fontsize)
        self.input = ""
        self.keyDelay = 100
        self.nextKey = pygame.time.get_ticks()

    def draw(self):
        self.screen.blit(self.font.render(self.title, True, pygame.Color(255,255,255)), (self.pos[0], self.pos[1]))
        
        #if not self.selected:
        pygame.draw.rect(self.screen, (255, 255, 255), self.collider)

        #else:
        #    pygame.draw.rect(self.screen, (153, 51, 255), self.collider)
        
        if not self.hidden:
            if not self.selected:
                self.screen.blit(self.font.render(self.input, True, pygame.Color(0, 0, 0)), ((self.colliderX + self.fontsize/2), self.pos[1]))
            
            else:
                self.screen.blit(self.font.render(self.input + "|", True, pygame.Color(0, 0, 0)), ((self.colliderX + self.fontsize/2), self.pos[1]))
        else:
            if not self.selected:
                self.screen.blit(self.font.render("*" * len(self.input), True, pygame.Color(0, 0, 0)), ((self.colliderX + self.fontsize/2), self.pos[1]))
            
            else:
                self.screen.blit(self.font.render("*" * len(self.input) + "|", True, pygame.Color(0, 0, 0)), ((self.colliderX + self.fontsize/2), self.pos[1]))        

    def checkClicked(self, mousepos):
        if self.collider.collidepoint(mousepos):
            self.selected = True
            pygame.event.clear()
            return True
        
        else:
            self.selected = False
            return False
    
    def update(self):
        if self.selected:
            if pygame.time.get_ticks() > self.nextKey:
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    self.input = self.input[:-1]

                    self.nextKey = pygame.time.get_ticks() + self.keyDelay
            
            pygame.event.pump() 
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalnum() or event.unicode == ".":
                    if (len(self.input) < self.maxLength):
                        self.input += event.unicode
        
