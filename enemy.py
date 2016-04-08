from missle import Missle

class Enemy:
    def __init__(self, image, pos, imagew, imageh):
        self.image = image
        self.posx = pos[0]
        self.posy = pos[1]
        self.imagew = imagew
        self.imageh = imageh

    def fire(self):
        pass
        #return Missle(0, "missle1", (self.posx + (self.imagew - 18), self.posy - (self.imageh)), 8, 32)
    
    def getPos(self):
        return (self.posx, self.posy)