import pygame
import time
from os.path import join, isfile

DISTANCE_THRESHOLD = 120
TANK_WIDTH = 64
TANK_HEIGHT = 64
ROOM_COVER = 16

class TankFishing(pygame.sprite.Sprite):
    def __init__(self, x, y, fish_per_second):
        self.rect = pygame.Rect(x + ROOM_COVER, y, 64, 196)
        self.color = (0, 0, 0)
        self.key_h_pressed = False
        self.fish_per_action = fish_per_second
        self.last_key_press_time = 0
        self.cooldown_time = 3
        self.loading_bar_active = False
        self.loading_start_time = 0
        self.image = pygame.image.load(join("Art", "tanks", "pond_for_fishing_lv1.png"))

    def draw(self, screen):
        #pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.image, self.rect)

    def handle_key_press(self):
        current_time = time.time()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_h]:
            if not self.key_h_pressed or current_time - self.last_key_press_time > self.cooldown_time:
                self.key_h_pressed = True
                self.last_key_press_time = current_time
                self.loading_bar_active = True
                self.loading_start_time = current_time

    def show_loading_bar(self, screen, money, player):

        BAR_WIDTH = 50
        BAR_HEIGHT = 10
        
        elapsed_time = time.time() - self.loading_start_time


        loading_bar_x = player.x_pos + (player.image.get_width() - BAR_WIDTH) // 2
        loading_bar_y = player.y_pos - BAR_HEIGHT - 10

        loading_bar_rect = pygame.Rect(loading_bar_x, loading_bar_y, BAR_WIDTH, BAR_HEIGHT)

        pygame.draw.rect(screen, (50, 50, 50), loading_bar_rect)

        progress_width = min(BAR_WIDTH, (elapsed_time / self.cooldown_time) * BAR_WIDTH)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(loading_bar_x, loading_bar_y, progress_width, BAR_HEIGHT))  # CHANGED: Use BAR_WIDTH and BAR_HEIGHT

        if elapsed_time >= self.cooldown_time:
            self.loading_bar_active = False
            money.balance += self.fish_per_action
            fishing_sound = pygame.mixer.Sound(join("sfx", "fishing.mp3"))
            fishing_sound.set_volume(0.5)
            fishing_sound.play()

    def loop(self, screen, player, money, font):
        self.draw(screen)
        if player.is_nearby(self, DISTANCE_THRESHOLD):
            self.handle_key_press()
            
            color = (0, 255, 0)
                
            self.draw_prompt(screen, font, color)
                
            if self.loading_bar_active:
                self.show_loading_bar(screen, money, player)
                player.lock = True
            else:
                player.lock = False

       
    def check_collision(self, player):
        player_rect = pygame.Rect(player.x_pos, player.y_pos, player.image.get_width(), player.image.get_height())
        return self.rect.colliderect(player_rect)

    def draw_prompt(self, screen, font, color):
        prompt_text_1 = f"This tank provides {self.fish_per_action} fish per action"
        prompt_text_2 = f"(Press H key to fish manually)"

        text_surface_1 = font.render(prompt_text_1, True, (255, 255, 255))
        text_surface_2 = font.render(prompt_text_2, True, (255, 255, 255))

        max_width = max(text_surface_1.get_width(), text_surface_2.get_width())
        total_height = text_surface_1.get_height() + text_surface_2.get_height() + 10
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

        screen.blit(text_surface_1, text_rect_1)
        screen.blit(text_surface_2, text_rect_2)
