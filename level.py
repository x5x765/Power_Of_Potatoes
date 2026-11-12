from json import load as json_load
import helpers
import pygame
from os import path
pygame.init()

class Level:
    def __init__(self, levelName):
        levelData = json_load(path.join("levels", levelName+".json"))
        levelImage = pygame.image.load(path.join("levels", "levelName"+".bmp"))
        self.rects = pygame.sprite.Group()
        for rectData in levelData:
            rect = helpers.SpriteWrapper(rectData["left"], rectData["top"], rectData["width"], rectData["height"])
            self.rects.add(rect)
