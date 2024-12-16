import pygame
import time
from os.path import join, isfile

DISTANCE_THRESHOLD = 120
TANK_WIDTH = 64
TANK_HEIGHT = 64

BASE_UPGRADE_COST = [[10, 150, 400], [2000, 3000, 5000], [10000, 15000, 20000]]
BASE_UPGRADE = [[9, 30, 50], [150, 200, 250], [1000, 1500, 2500]]
MAX_LEVEL = 3

class RodUpgrade(pygame.sprite.Sprite):
    def __init__(self, x, y, tank):
        self.rect = pygame.Rect(x, y, 64, 64)
        self.color = (0, 0, 0)
        self.price = 0
        self.flash_text_start_time = 0
        self.upgrade_level = 0
        self.last_flash_time = 0
        self.manual_tank = tank
        
        self.last_keypress_time = 0
        self.key_cooldown = 0.5 

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def loop(self, screen, player, money, font):
        self.draw(screen)
        if player.is_nearby(self, DISTANCE_THRESHOLD):
            color = (0, 255, 0)

            if self.upgrade_level == MAX_LEVEL:
                self.draw_info(screen, font, (0, 0, 0))
                return

            if money.balance < self.price:
                color = (255, 0, 0)

            self.draw_buy_prompt(screen, font, color, player)

            keys = pygame.key.get_pressed()
            current_time = time.time()

            if keys[pygame.K_e] and current_time - self.last_keypress_time > self.key_cooldown:
                self.last_keypress_time = current_time

                self.price = BASE_UPGRADE_COST[player.level][self.upgrade_level]
                
                if money.balance >= self.price:
                    money.balance -= self.price
                    # print(self.upgrade_level)
                    purchase_sound = pygame.mixer.Sound(join("sfx", "confirmed_purchase.mp3"))
                    purchase_sound.set_volume(0.5)
                    purchase_sound.play()
                    self.manual_tank.fish_per_action += BASE_UPGRADE[player.level][self.upgrade_level]
                    self.upgrade_level += 1
                    
                else:
                    not_money_sound = pygame.mixer.Sound(join("sfx", "not_enough_money_2.mp3"))
                    not_money_sound.set_volume(0.5)
                    not_money_sound.play()
                    self.flash_text = True
                    self.flash_text_start_time = current_time
                    self.flash_text_color = (255, 0, 0)


       
    def check_collision(self, player):
        player_rect = pygame.Rect(player.x_pos, player.y_pos, player.image.get_width(), player.image.get_height())
        return self.rect.colliderect(player_rect)

    def draw_buy_prompt(self, screen, font, color, player):
        if self.upgrade_level < MAX_LEVEL:
            if hasattr(self, "flash_text") and self.flash_text:
                
                if self.flash_text_start_time == 0:
                    self.flash_text_start_time = time.time()
                
                elapsed_time = time.time() - self.flash_text_start_time

                if elapsed_time >= 0.75:
                    self.flash_text = False
                    self.flash_text_start_time = 0
                    self.flash_text_color = (255, 255, 255)

                elif time.time() - self.last_flash_time >= 0.1:
                    self.flash_text_color = (
                        (255, 255, 255) if self.flash_text_color == (255, 0, 0) else (255, 0, 0)
                    )
                    self.last_flash_time = time.time()
            else:
                self.flash_text_color = (255, 255, 255)

            text_color = self.flash_text_color if hasattr(self, "flash_text") and self.flash_text else (255, 255, 255)

            prompt_text_1 = f"{BASE_UPGRADE[player.level][self.upgrade_level]} more fish when manually fishing!"
            prompt_text_2 = f"Price: {BASE_UPGRADE_COST[player.level][self.upgrade_level]}"
            prompt_text_3 = f"(Press E key to buy upgrade)"

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

    def draw_info(self, screen, font, color):
        info_text = f"Manual fishing tank has max upgrades!"

        text_surface = font.render(info_text, True, (255, 255, 255))
        box_width = text_surface.get_width() + 20
        box_height = text_surface.get_height() + 20

        info_box_rect = pygame.Rect(0, 0, box_width, box_height)

        info_box_rect.centerx = self.rect.centerx
        info_box_rect.bottom = self.rect.top - 10

        screen_width, screen_height = screen.get_size()
        if info_box_rect.left < 0:
            info_box_rect.left = 10
        if info_box_rect.right > screen_width:
            info_box_rect.right = screen_width - 10
        if info_box_rect.top < 0:
            info_box_rect.top = 10

        pygame.draw.rect(screen, color, info_box_rect)
        text_rect = text_surface.get_rect(center=info_box_rect.center)
        screen.blit(text_surface, text_rect)

        # print(f"Info Box position: {info_box_rect.x}, {info_box_rect.y}, Box size: {info_box_rect.width}x{info_box_rect.height}")

