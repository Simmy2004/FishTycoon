import pygame
from os.path import join, isfile
from os import listdir
from block import BLOCK_WIDTH, BLOCK_HEIGHT, Block
from money import Money
from tank_idle import TANK_WIDTH, TANK_HEIGHT, TankIdle
from tank_fishing import TankFishing
from math import sqrt
from PIL import Image

from pygame.sprite import Group

from walkable import Walkable

pygame.init()

VELOCITY = 6
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
        self.lock = False

    # Generates a rectangle by the player dimensions. Return if there is any collision
    def check_collision(self, collsionable):
        player_rect = pygame.Rect(self.x_pos, self.y_pos, self.image.get_width(), self.image.get_height())
        return collsionable.rect.colliderect(player_rect)
    
    # Checks if the distance between interactable object is less than a given threshold
    def is_nearby(self, collisionable, threshold):
        player_center = pygame.Rect(self.x_pos, self.y_pos, self.image.get_width(), self.image.get_height()).center
        collidable_center = collisionable.rect.center
        distance = sqrt((player_center[0] - collidable_center[0]) ** 2 + (player_center[1] - collidable_center[1]) ** 2)
        return distance < threshold

    # Moves the player by the given velocities.
    def move(self, x_vel, y_vel, collisionables):
        # Checks if the player is currently executing something
        if self.lock:
            return
        
        # If the player needs to stop in any direction because of a collision, velocity->0
        x_vel, y_vel = self.handle_collisions(collisionables, x_vel, y_vel)

        self.x_pos += x_vel
        self.y_pos += y_vel
        
    def loop(self, fps, collisionables, screen, font):
        self.move(self.x_vel, self.y_vel, collisionables)

    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))

    # Checks for any collisions and modifies velocity to 0 if encountered.
    def handle_collisions(self, collisionables, x_vel, y_vel):
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

        return x_vel, y_vel

# Loads the image and creates the background tile by tile, returning the grid, and the image used
def get_background(img_name):
    image = pygame.image.load(join("Art", img_name))
    _, _, width, height = image.get_rect()

    # tiles is an array of tuples (x_pos, y_pos)
    tiles = []
    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            position = (i * width, j * height)
            tiles.append(position)
    
    return tiles, image

# Checks for any input in the keyboard for movement.
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

def render_back_wall():
    upper_tiles = []
    down_tiles = []
    for i in range(WIDTH // TANK_WIDTH + 1):
        if i == 0:
            upper_tiles.append(Block(i * TANK_WIDTH, 0, join("Tiles", "BlueWall", "tile1.png")))
            down_tiles.append(Walkable(i * TANK_WIDTH, TANK_HEIGHT, join("Tiles", "BlueWall", "tile9.png")))
        elif i == WIDTH // TANK_WIDTH - 1:
            upper_tiles.append(Block(i * TANK_WIDTH, 0, join("Tiles", "BlueWall", "tile4.png")))
            down_tiles.append(Walkable(i * TANK_WIDTH, TANK_HEIGHT, join("Tiles", "BlueWall", "tile12.png")))
        else:
            upper_tile_number = "tile2.png" if (i % 2) == 1 else "tile3.png"
            down_tile_number = "tile10.png" if (i % 2) == 1 else "tile11.png"
    
            upper_tiles.append(Block(i * TANK_WIDTH, 0, join("Tiles", "BlueWall", upper_tile_number)))
            down_tiles.append(Walkable(i * TANK_WIDTH, TANK_HEIGHT, join("Tiles", "BlueWall", down_tile_number)))

    return upper_tiles, down_tiles

    

# Here i will define every object that can collide with the player.
def render_collisionables():
    upper_wall, down_wall = render_back_wall()
    collisionables = []
    walkables = []

    for wall_tile in upper_wall:
        collisionables.append(wall_tile)
    for wall_tile in down_wall:
        walkables.append(wall_tile)

   
    collisionables.append(TankFishing(WIDTH - TANK_WIDTH, TANK_HEIGHT + 50, 2)) 
    collisionables.append(TankIdle(WIDTH - TANK_WIDTH, 5 * TANK_HEIGHT, 5, 100))
    # collisionables.append(Tank(WIDTH - 2 * TANK_WIDTH, 9 * TANK_HEIGHT, 5, 100, 2))
    

    return collisionables, walkables

def main():
    running = True
    screen = pygame.display.set_mode((1280, 720))
    tiles, image = get_background("floor_tile_256x256.png")
    # starting positions and the file
    player = Player(300, 300, "main_icon_96x128.png")
    money = Money()
    font = pygame.font.Font(None, 20) 
    
    collisionables, walkables = render_collisionables()

    while running:
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        handle_keyboard_input(player)

        for tile in tiles:
            screen.blit(image, tile)

        for walkable in walkables:
            walkable.loop(screen, player, money, font)
        for collisionable in collisionables:
            collisionable.loop(screen, player, money, font)
            
        money.loop(MAX_FPS)
        money.render_balance(MAX_FPS, screen, font)
            
        player.loop(MAX_FPS, collisionables, screen, font)
        player.draw(screen)
       
        pygame.display.update()

    pygame.quit()



if __name__ == "__main__":
    main()