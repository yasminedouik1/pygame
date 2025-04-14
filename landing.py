import pygame
import sys
import os



from main import game_loop 

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Dash and Crash")
font = pygame.font.SysFont("poppins", 24)

background_image = pygame.image.load("./images/landing.jpg")
background_image = pygame.transform.scale(background_image, (800, 600))
button_rect = pygame.Rect(150, 275, 150, 60)

def landing_page():
    while True:
        screen.blit(background_image, (0, 0)) 
     
        pygame.draw.rect(screen, (208, 111, 39), button_rect, border_radius=10)
        text = font.render("Start Game", True, (255, 255, 255))
        screen.blit(text, (button_rect.x + 20, button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_loop()  
                    return  

        pygame.display.flip()

landing_page()
