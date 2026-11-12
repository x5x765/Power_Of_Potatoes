import pygame
from json import load as json_load
from os import path


class SpriteWrapper(pygame.sprite.Sprite):
    def __init__(self, x:int, y:int, width:int, height:int, color = (0, 0, 0, 0),*,rect:pygame.Rect = None, image:pygame.Surface = None):
        super().__init__()
        
        if rect:
            self.rect = rect
        else:
            self.rect = pygame.Rect(x, y, width, height)

        if image:
            self.image = image
        else:
            self.image = pygame.Surface(rect.size, pygame.SRCALPHA).fill(color)

class Character:
    def __init__(self, characterName, physicsController):
        self.x = 0
        self.y = 0
        self.image = path.join
        self.physicsController = physicsController
        self.characterName = characterName
    
    def update_y(self):
        self.physicsController.calc_y(self.y)

class Level:
    def __init__(self, levelName):
        levelData = json_load(path.join("levels", levelName+".json"))
        levelImage = pygame.image.load(path.join("levels", "levelName"+".bmp"))
        self.rects = pygame.sprite.Group()
        for rectData in levelData:
            rect = SpriteWrapper(rectData["left"], rectData["top"], rectData["width"], rectData["height"])
            self.rects.add(rect)
