import pygame
import time
from os.path import join, isfile
from os import listdir

DISTANCE_THRESHOLD = 120
TANK_WIDTH = 64
TANK_HEIGHT = 64
ROOM_COVER = 16
FISHERMAN_COUNT = 0

def load_sprite_sheets(dir, width, height):
    path = join("Art", dir)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for  image in images:
        sprite_sheet = pygame.image.load(join(path, image))

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0 , width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(surface)
        
        all_sprites[image] = sprites
    
    return all_sprites

class TankIdle(pygame.sprite.Sprite):
    SPRITES = load_sprite_sheets("fishermanSprites", 80, 120)
    ANIMATION_DELAY = 10
    
    def __init__(self, x, y, price, money_per_second, level, fisherman):
        self.rect = pygame.Rect(x - ROOM_COVER, y, 64, 64)
        self.color = (0, 0, 0)
        self.price = price
        self.mps = money_per_second
        self.flash_text_start_time = 0
        self.is_bought = 0
        self.old_mps = 0
        self.last_flash_time = 0
        self.fisherman = fisherman
        self.animation_count = 0

        if (level == 1):
            self.image = pygame.image.load(join("Art", "tanks", "idle_tank_lv1.png"))
        elif (level == 2):
            self.image = pygame.image.load(join("Art", "tanks", "idle_tank_lv2.png"))
        else:
            self.image = pygame.image.load(join("Art", "tanks", "idle_tank_lv3.png"))
        
        self.key_cooldown = 0.5
        self.last_keypress_time = 0

    def update_spritesheet(self):
        if (self.fisherman == 1):
            sprite_sheet_name = "idle_fisherman1.png"
        elif (self.fisherman == 2):
            sprite_sheet_name = "idle_fisherman2.png"
        else:
            sprite_sheet_name = "idle_fisherman3.png"

        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)

        self.sprite = sprites[sprite_index]
        self.animation_count += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if (self.is_bought):
            (x, y) = self.rect.topleft
            screen.blit(self.sprite, (x - 80, y - 25))

    def loop(self, screen, player, money, font):
        self.draw(screen)
        self.update_spritesheet()
        if player.is_nearby(self, DISTANCE_THRESHOLD):

            color = (0, 255, 0)

            if self.is_bought == 1:
                self.draw_info(screen, font, (0, 0, 0))
                return

            if money.balance < self.price:
                color = (255, 0, 0)                
            
            self.draw_buy_prompt(screen, font, color)

            keys = pygame.key.get_pressed()
            current_time = time.time()

            if keys[pygame.K_e] and current_time - self.last_keypress_time > self.key_cooldown:
                self.last_keypress_time = current_time

                if money.balance >= self.price:
                    purchase_sound = pygame.mixer.Sound(join("sfx", "confirmed_purchase.mp3"))
                    purchase_sound.set_volume(0.2)
                    purchase_sound.play()
                    
                    self.is_bought = 1
                    money.balance -= self.price
                    # print(self.mps)
                    money.increase_money_per_second(self.mps)
                    self.old_mps = self.mps
                    self.mps = 0
                else:
                    not_money_sound = pygame.mixer.Sound(join("sfx", "not_enough_money_2.mp3"))
                    not_money_sound.set_volume(0.2)
                    not_money_sound.play()
                    self.flash_text = True
                    self.flash_text_start_time = time.time()
                    self.flash_text_color = (255, 0, 0)


       
    def check_collision(self, player):
        player_rect = pygame.Rect(player.x_pos, player.y_pos, player.image.get_width(), player.image.get_height())
        return self.rect.colliderect(player_rect)

    def draw_buy_prompt(self, screen, font, color):
        if self.is_bought == 0:
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

            prompt_text_1 = f"This tank provides {self.mps} fish per second with fisherman"
            prompt_text_2 = f"Price: {self.price}"
            prompt_text_3 = f"(Press E key to buy fisherman)"

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
        info_text = f"This tank provides {self.old_mps} fish per second"

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

