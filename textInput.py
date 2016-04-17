import pygame

class textInput:
    #self.screen = screen
    #title = Username/Password/Etc.
    #pos = (x, y) = where the 
    #boxw, h = box width, height
    def __init__(self, screen, title, pos, boxw, boxh, maxLength):
        self.screen = screen
        self.title = title + ":"
        self.selected = False
        self.fontsize = 30
        self.maxLength = maxLength
        self.collider = pygame.Rect(pos[0] + (self.fontsize * len(self.title)/1.5), pos[1], boxw, boxh)
        self.pos = pos
        self.boxw = boxw
        self.boxh = boxh
        self.font = pygame.font.Font(pygame.font.match_font('comicsansms'), self.fontsize)
        self.input = ""

    def draw(self):
        self.screen.blit(self.font.render(self.title, True, pygame.Color(255,255,255)), (self.pos[0], self.pos[1]))
        pygame.draw.rect(self.screen, (255, 255, 255), self.collider)
        self.screen.blit(self.font.render(self.input, True, pygame.Color(0, 0, 0)), (self.pos[0] + (self.fontsize * len(self.title)/1.5 + self.fontsize), self.pos[1]))

    def checkClicked(self, mousepos):
        if self.collider.collidepoint(mousepos):
            self.selected = True
            return True
        
        else:
            self.selected = False
            return False
    
    def update(self):
        if self.selected:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.unicode.isalpha():
                        if (len(self.input) < self.maxLength):
                            self.input += event.unicode

                    elif event.key == pygame.K_BACKSPACE:
                        self.input = self.input[:-1]
        