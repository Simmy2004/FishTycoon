import pygame
from os.path import join, isfile

class Door:
    def __init__(self, x, y):
        self.image = pygame.image.load(join("Art", "Tiles", "door.png"))
        self.x_pos = x
        self.y_pos = y
    
    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))

