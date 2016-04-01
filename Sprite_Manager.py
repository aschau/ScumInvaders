import os, sys
import pygame

#Class to load spritesheet or parts of the spritesheet
class SpriteSheets():
    def __init__(self, folder):
        try:
            self.folder = folder
            os.path.isdir(self.folder)

        except os.error:
            print ('Unable to load sprites folder', folder)
            raise SystemExit

    def load(self, image):
        self.sheet = pygame.image.load(os.path.join(self.folder, image))

    def loadAll(self):
        self.all = {}
        for root, dirs, files in os.walk(self.folder):
           for image in files:
               if image[-3:] == "png":
                   self.all[image] = pygame.image.load(os.path.join(self.folder, image))
        return self.all

#animate sprites
class Animate():
    def __init__(self, image, frames, columns, imagew, imageh):

        #image = Spritesheet you want to use from "AllSprites" dictionary. ex: AllSprites['player.png]
        #frames = how many frames are in the sprite sheet.
        #columns = how many columns of sprites are in the sprite sheet.
        #rows = how many rows of sprites are in the sprite sheet.
        #imagew = image width, the sprites for now are all 32 width
        #imageh = image height, the sprites for now are all 32 height
        
        self.image = image 
        self.frame = -1
        self.currentFrame = -1
        self.frames = frames
        self.columns = columns
        self.row = 0
        self.clock = pygame.time.Clock()
        self.imagew = imagew
        self.imageh = imageh


    def update(self):
        self.frame += 1
        self.currentFrame += 1
        if self.currentFrame > self.columns:
            self.row += 1
            self.currentFrame = -1
        if self.frame > self.frames - 1:
            self.frame = -1
            self.row = 0;
            self.currentFrame = -1
        self.clock.tick(64)

    def draw(self, window,  x, y):
        #x, y are where on the screen you want the sprite to draw
        window.blit(self.image, (x, y), ((self.frame % self.columns) * self.imagew, self.row*imageh, self.imagew, self.imageh))
