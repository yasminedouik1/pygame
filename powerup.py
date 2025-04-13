import pygame

class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.type = "shield"
        self.color = (255, 215, 0)  

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
