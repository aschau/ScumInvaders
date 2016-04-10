import pygame

class Missle:
    def __init__(self, owner, image, pos, imagew, imageh, enemyRow = -1, enemyCol = -1):
        self.owner = owner
        self.image = image
        self.enemyRow = enemyRow
        self.enemyCol = enemyCol
        self.posx = pos[0]
        self.posy = pos[1]
        self.imagew = imagew
        self.imageh = imageh
        self.speed = 8
        self.collider = pygame.Rect(self.posx, self.posy, imagew, imageh)

    def update(self):
        if self.owner > 0:
            self.posy -= self.speed
            self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)
        else:
            self.posy += self.speed
            self.collider = pygame.Rect(self.posx, self.posy, self.imagew, self.imageh)

    def getEnemyPos(self):
        return (self.enemyRow, self.enemyCol)
    
    def getPos(self):
        return (self.posx, self.posy)