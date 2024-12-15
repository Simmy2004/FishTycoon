from math import sqrt
import time
import pygame
from os.path import join, isfile

DISTANCE_THRESHOLD = 120

class Door:
    def __init__(self, x, y, price, final_door):
        self.image = pygame.image.load(join("Art", "Tiles", "door.png"))
        self.x_pos = x
        self.y_pos = y
        self.rect = pygame.Rect(x, y, 64, 100)
        self.price = price
        self.final_door = final_door
        self.fade = False
    
    def draw(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))

    def loop(self, screen, player, money, font):
        self.draw(screen)

        # Gets the player center and calculates the distance between the player and the door.
        player_center = pygame.Rect(player.x_pos, player.y_pos, player.image.get_width(), player.image.get_height()).center
        collidable_center = self.rect.center
        distance = sqrt((player_center[0] - collidable_center[0]) ** 2 + (player_center[1] - collidable_center[1]) ** 2)

        if (distance < DISTANCE_THRESHOLD - 20):
            color = (0, 255, 0)
            self.draw_buy_prompt(screen, font, color)

            if money.balance < self.price:
                color = (255, 0, 0)  

            self.draw_buy_prompt(screen, font, color)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_e] and self.final_door and money.balance >= self.price:
                
                print()
            elif keys[pygame.K_e] and money.balance >= self.price:
                self.fade = True
          


    def draw_buy_prompt(self, screen, font, color):
      
        prompt_text_1 = f"This Door lets you travel to the next location"
        prompt_text_2 = f"Next location is: Torino - Price 1.000$"
        prompt_text_3 = f"(Press E to travel to Torino)"


        text_color = (255, 255, 255)
        text_surface_1 = font.render(prompt_text_1, True, (255, 255, 255))
        text_surface_2 = font.render(prompt_text_2, True, text_color)
        text_surface_3 = font.render(prompt_text_3, True, text_color)
            
        max_width = max(
            text_surface_1.get_width(),
            text_surface_2.get_width(),
            text_surface_3.get_width(),
        )
        total_height = (
            text_surface_1.get_height()
            + text_surface_2.get_height()
            + text_surface_3.get_height()
            + 20
        )
        prompt_rect = pygame.Rect(0, 0, max_width + 20, total_height)

        prompt_rect.centerx = self.rect.centerx
        prompt_rect.bottom = self.rect.top - 10

        screen_width, screen_height = screen.get_size()
        if prompt_rect.left < 0:
            prompt_rect.left = 10
        if prompt_rect.right > screen_width:
            prompt_rect.right = screen_width - 10
        if prompt_rect.top < 0:
            prompt_rect.top = 10
                
        box_surface = pygame.Surface((prompt_rect.width, prompt_rect.height), pygame.SRCALPHA)
        box_surface.fill((color[0], color[1], color[2], 100)) 
        screen.blit(box_surface, prompt_rect.topleft)

        text_rect_1 = text_surface_1.get_rect(center=(prompt_rect.centerx, prompt_rect.top + 10))
        text_rect_2 = text_surface_2.get_rect(center=(prompt_rect.centerx, text_rect_1.bottom + 10))
        text_rect_3 = text_surface_3.get_rect(center=(prompt_rect.centerx, text_rect_2.bottom + 10))

        screen.blit(text_surface_1, text_rect_1)
        screen.blit(text_surface_2, text_rect_2)
        screen.blit(text_surface_3, text_rect_3)

