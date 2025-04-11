import pygame

obstacle_size = (50, 50)
obstacle_speed = 7
RED = (255, 0, 0)

class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, *obstacle_size)

    def update(self):
        self.rect.x -= obstacle_speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)
