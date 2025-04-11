import pygame
import random

bonus_size = (30, 30)
bonus_speed = 5
bonus_types = ["shield", "weapon", "armor"]

colors = {
    "shield": (0, 255, 255),
    "weapon": (128, 0, 128),
    "armor": (150, 150, 150),
}

class Bonus:
    def __init__(self, x, y):
        self.kind = random.choice(bonus_types)
        self.rect = pygame.Rect(x, y, *bonus_size)

    def update(self):
        self.rect.x -= bonus_speed

    def draw(self, screen):
        pygame.draw.rect(screen, colors[self.kind], self.rect)
