import pygame
from os.path import join, isfile
from os import listdir
from money import Money
from tank import Tank
from math import sqrt

from pygame.sprite import Group

pygame.init()

VELOCITY = 5
WIDTH = 1280
HEIGHT = 720
MAX_FPS = 60
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name):
        self.x_vel = 0
        self.y_vel = 0
        self.x_pos = x
        self.y_pos = y
        self.image = pygame.image.load(join("Art", image_name))

    def check_collision(self, collsionable):
        player_rect = pygame.Rect(self.x_pos, self.y_pos, self.image.get_width(), self.image.get_height())
        return collsionable.rect.colliderect(player_rect)
    
    
    def is_nearby(self, collisionable, threshold):
        
        player_center = pygame.Rect(self.x_pos, self.y_pos, self.image.get_width(), self.image.get_height()).center
        collidable_center = collisionable.rect.center
        distance = sqrt((player_center[0] - collidable_center[0]) ** 2 + (player_center[1] - collidable_center[1]) ** 2)
        return distance < threshold

    def move(self, x_vel, y_vel, collisionables):
        
        player_rect = pygame.Rect(self.x_pos, self.y_pos, self.image.get_width(), self.image.get_height())
        if x_vel != 0:

            future_rect = player_rect.move(x_vel, 0)
            for collisionable in collisionables:
                collidable_rect = collisionable.rect 
                if future_rect.colliderect(collidable_rect):
                    if x_vel > 0:
                        self.x_pos = collidable_rect.left - player_rect.width
                    elif x_vel < 0:
                        self.x_pos = collidable_rect.right
                    x_vel = 0

        if y_vel != 0:
            future_rect = player_rect.move(0, y_vel) 
            for collisionable in collisionables:
                collidable_rect = collisionable.rect

                if future_rect.colliderect(collidable_rect):
                    if y_vel > 0:
                        self.y_pos = collidable_rect.top - player_rect.height
                    elif y_vel < 0:
                        self.y_pos = collidable_rect.bottom
                    y_vel = 0
        self.x_pos += x_vel
        self.y_pos += y_vel
        
    def loop(self, fps, collisionables, screen, font):
        self.move(self.x_vel, self.y_vel, collisionables)

    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))


def get_background(img_name):
    image = pygame.image.load(join("Art", img_name))
    _, _, width, height = image.get_rect()

    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            position = (i * width, j * height)
            tiles.append(position)
    
    return tiles, image

def handle_keyboard_input(player):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    player.y_vel = 0

    if keys[pygame.K_UP]:
        player.y_vel = -VELOCITY
        if player.y_pos == 0:
            player.y_vel = 0

    if keys[pygame.K_DOWN]:
        player.y_vel = VELOCITY
        if player.y_pos >= HEIGHT - 64:
            player.y_vel = 0

    if keys[pygame.K_RIGHT]:
        player.x_vel = VELOCITY
        if player.x_pos >= WIDTH - 64:
            player.x_vel = 0

    if keys[pygame.K_LEFT]:
        player.x_vel = -VELOCITY   
        if player.x_pos == 0:
            player.x_vel = 0


def main():
    running = True
    screen = pygame.display.set_mode((1280, 720))
    tiles, image = get_background("floor_tile_256x256.png")
    # starting positions and the file
    player = Player(300, 300, "main_icon_96x128.png")
    money = Money()
    font = pygame.font.Font(None, 20) 
    
    tank = Tank(700, 300, 5, 100, 2)
    collisionables = [tank]

    while running:
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        handle_keyboard_input(player)
        player.loop(MAX_FPS, collisionables, screen, font)

        for tile in tiles:
            screen.blit(image, tile)

        player.draw(screen)
        money.loop(MAX_FPS)
        money.render_balance(MAX_FPS, screen, font)
        tank.loop(screen, player, money, font)
        pygame.display.update()

    pygame.quit()



if __name__ == "__main__":
    main()