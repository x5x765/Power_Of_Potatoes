import pygame
pygame.init()


class Character:
    def __init__(self, physicsController):
        self.rect = image.get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
        self.physicsController = physicsCon