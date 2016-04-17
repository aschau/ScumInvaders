import pygame

class textInput:
    #self.screen = screen
    #title = Username/Password/Etc.
    #pos = (x, y) = where the 
    #boxw, h = box width, height
    def __init__(self, screen, title, pos, boxw, boxh):
        self.screen = screen
        self.title = title + ":"
        self.fontsize = 30
        self.collider = pygame.Rect(pos[0] + (self.fontsize * len(self.title)/1.5), pos[1], boxw, boxh)
        self.pos = pos
        self.boxw = boxw
        self.boxh = boxh
        self.font = pygame.font.Font(pygame.font.match_font('comicsansms'), self.fontsize)

    def draw(self):
        self.screen.blit(self.font.render(self.title, True, pygame.Color(255,255,255)), (self.pos[0], self.pos[1]))
        pygame.draw.rect(self.screen, (255, 255, 255), self.collider)

    def update(self):
        pass
        