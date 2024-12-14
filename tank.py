import pygame

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, price, mps, fpa):
        self.rect = pygame.Rect(x, y, 100, 100)
        self.color = (0, 0, 0)
        self.price = price
        self.mps = mps
        self.is_bought = 0
        self.old_mps = 0
        self.key_h_pressed = 0
        self.fish_per_action = fpa

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    def handle_key_press(self, money):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_h]:
            if not self.key_h_pressed:
                money.balance += self.fish_per_action
                self.key_h_pressed = True
        else:
            self.key_h_pressed = False
            
    def loop(self, screen, player, money, font):
        self.draw(screen)
        if player.is_nearby(self, 140):
            
            self.handle_key_press(money)
            
            if self.is_bought == 1:
                self.draw_info(screen, font, (0, 0, 0))
                return
            
            color = (0, 0, 0)
            if money.balance >= self.price:
                color = (0, 255, 0)
            else:
                color = (255, 0, 0)
                
            self.draw_buy_prompt(screen, font, color)
            
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_e] and money.balance > self.price:
                self.is_bought = 1
                print(self.mps)
                money.increase_money_per_second(self.mps)
                self.old_mps = self.mps
                self.mps = 0

    def check_collision(self, player):
        player_rect = pygame.Rect(player.x_pos, player.y_pos, player.image.get_width(), player.image.get_height())
        return self.rect.colliderect(player_rect)

    def draw_buy_prompt(self, screen, font, color):
        if self.is_bought == 0:

            prompt_text_1 = f"This tank provides {self.mps} fish per second"
            prompt_text_2 = f"Price: {self.price}"
            prompt_text_3 = f"(Press E key)"

            text_surface_1 = font.render(prompt_text_1, True, (255, 255, 255))
            text_surface_2 = font.render(prompt_text_2, True, (255, 255, 255))
            text_surface_3 = font.render(prompt_text_3, True, (255, 255, 255))

            max_width = max(text_surface_1.get_width(), text_surface_2.get_width(), text_surface_3.get_width())
            total_height = text_surface_1.get_height() + text_surface_2.get_height() + text_surface_3.get_height() + 20 
            prompt_rect = pygame.Rect(self.rect.x, self.rect.y - total_height, max_width + 20, total_height)

            pygame.draw.rect(screen, color, prompt_rect)

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

        info_box_rect = pygame.Rect(self.rect.x, self.rect.y - box_height - 10, box_width, box_height)
        pygame.draw.rect(screen, color, info_box_rect)
        text_rect = text_surface.get_rect(center=info_box_rect.center)
        screen.blit(text_surface, text_rect)
        
        print(f"Info Box position: {info_box_rect.x}, {info_box_rect.y}, Box size: {info_box_rect.width}x{info_box_rect.height}")