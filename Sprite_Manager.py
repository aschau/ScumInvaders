import os, sys
import pygame

#Class to load spritesheet or parts of the spritesheet
class sprites():
    def __init__(self, folder):
        self.all = {}
        try:
            self.folder = folder
            os.path.isdir(self.folder)

        except os.error:
            print ('Unable to load sprites folder', folder)
            raise SystemExit

    def load(self, image):
        self.sheet = pygame.image.load(os.path.join(self.folder, image + ".png")).convert_alpha()
        return self.sheet

    def loadAll(self):
        for root, dirs, files in os.walk(self.folder):
           for image in files:
               if image[-3:] == "png":
                   self.all[image] = pygame.image.load(os.path.join(self.folder, image)).convert_alpha()
    
    def getSprite(self, spriteName):
        return self.all[spriteName + ".png"]

    def getAll(self):
        return self.all

#animate sprites
class Animate():
    def __init__(self, image, frames, columns, imagew, imageh, ticks, loop = True):

        #image = Spritesheet you want to use from "AllSprites" dictionary. ex: AllSprites['player.png']
        #frames = how many frames are in the sprite sheet.
        #columns = how many columns of sprites are in the sprite sheet.
        #imagew = image width, the sprites for now are all 32 width
        #imageh = image height, the sprites for now are all 32 height
        
        self.image = image 
        self.frame = 0
        self.ticks = 0
        self.maxTicks = ticks
        self.currentFrame = 0
        self.frames = frames
        self.columns = columns
        self.row = 0
        self.imagew = imagew
        self.imageh = imageh
        self.loop = loop
        self.done = False


    def update(self):
        if not self.done:
            if self.ticks == self.maxTicks:
                if self.currentFrame >= self.columns-1:
                    self.row += 1
                    self.currentFrame = -1
            
                if self.frame >= self.frames-1:
                    if self.loop:
                        self.frame = -1
                        self.row = 0
                        self.currentFrame = -1
                    else:
                        self.done = True
                
                if not self.done:
                    self.frame += 1
                    self.currentFrame += 1

                    self.ticks = 0
        
            else:
               self.ticks += 1

    def draw(self, window, pos):
        #x, y are where on the screen you want the sprite to draw
        if not self.done:
            window.blit(self.image, (pos[0], pos[1]), ((self.frame % self.columns) * self.imagew, self.row*self.imageh, self.imagew, self.imageh))
