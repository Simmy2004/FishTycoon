import pygame

class Money(pygame.sprite.Sprite):
    def __init__(self):
        self.money_per_second = 1
        self.balance = 0
        self.counter = 0

    def increase_money_per_second(self, to_add):
        self.money_per_second += to_add

    def loop(self, fps):
        self.counter = self.counter + 1
        if self.counter == fps:
            self.counter = 0
            self.balance += self.money_per_second
        print(self.balance)
    def render_balance(self, fps, screen, font):
        box_size = (100, 20)
        transparent_surface = pygame.Surface(box_size, pygame.SRCALPHA)
        
        box_color = (0, 0, 0, 200)
        transparent_surface.fill(box_color)

        text_color = (255, 255, 255)
        balance_text = font.render(f"${self.balance}", True, text_color)
        text_rect = balance_text.get_rect(center=(box_size[0] // 2, box_size[1] // 2))

        transparent_surface.blit(balance_text, text_rect)

        screen.blit(transparent_surface, (0, 0))