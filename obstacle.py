import pygame
import random

obstacle_size = (35, 30)
bomb_size = (30, 40)
obstacle_speed = 5

rock_images = [
    pygame.transform.scale(pygame.image.load("images/obstacles/rock1.png"), obstacle_size),
    pygame.transform.scale(pygame.image.load("images/obstacles/rock3.png"), obstacle_size),
    pygame.transform.scale(pygame.image.load("images/obstacles/bomb.png"), bomb_size),

]

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, *obstacle_size)
        self.image = random.choice(rock_images)  

    def update(self):
        self.rect.x -= obstacle_speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
