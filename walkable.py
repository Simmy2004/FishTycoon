from os.path import join, isfile
import pygame
from PIL import Image

from block import BLOCK_HEIGHT, BLOCK_WIDTH

class Walkable:
    def __init__ (self, x, y, image_name):
        image = Image.open(join("Art", image_name))
        image_resized = image.resize((64, 64), Image.LANCZOS)
        self.image = pygame.image.fromstring(image_resized.tobytes(), image_resized.size, image_resized.mode)

       # self.image = pygame.image.load(join("Art", image_name))
        self.x_pos = x
        self.y_pos = y
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)

    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))
    
    def loop(self, screen, player, money, font):
        self.draw(screen)