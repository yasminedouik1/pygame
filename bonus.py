import pygame
import random

bonus_size = (50, 50)
bonus_speed = 5
bonus_types = ["shield", "weapon", "armor"]

images = {
    "shield": pygame.transform.scale(pygame.image.load("./images/shield.png"), bonus_size),
    "weapon": pygame.transform.scale(pygame.image.load("./images/weapon.jpg"), bonus_size),
    "armor": pygame.transform.scale(pygame.image.load("./images/armor.png"), bonus_size),
}

class Bonus:
    def __init__(self, x, y):
        self.kind = random.choice(bonus_types)
        self.rect = pygame.Rect(x, y, *bonus_size)
        self.image = images[self.kind]

    def update(self):
        self.rect.x -= bonus_speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
