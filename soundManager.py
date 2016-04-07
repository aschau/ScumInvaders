import pygame
import os

class soundManager:
    def __init__(self, folder):
        try:
            self.folder = folder
            os.path.isdir(self.folder)

        except os.error:
            print ('Unable to load sound folder', folder)
            raise SystemExit

        self.all = {}
        self.loadAll()

        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        self.music = pygame.mixer.music.load(os.path.join(self.folder, 'Space Invaders Main Menu.ogg'))
        pygame.mixer.music.set_volume(.3)
        pygame.mixer.music.play(-1)

    def loadAll(self):
        for root, dirs, files in os.walk(self.folder):
            for sound in files:
                if sound[-3:] == "ogg":
                    new_sound = pygame.mixer.Sound(os.path.join(self.folder, sound))
                    new_sound.set_volume(1)
                    self.all[sound] = new_sound
    
    def playCurrentMusic(self):
        pygame.mixer.music.play(-1)

    def playSound(self, file):
        self.all[file].play()