import pygame
import random
import sys
from player import Player
from obstacle import Obstacle
from bonus import Bonus, bonus_types

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Battle Run Duo")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

background_image = pygame.image.load("./images/background.png")
background_rect = background_image.get_rect()  


font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 50)
clock = pygame.time.Clock()

def draw_divider():
    pygame.draw.line(screen, BLACK, (0, screen_height//2), (screen_width, screen_height//2), 3)

def display_game_over(player_scores):
    screen.blit(background_image, (0, 0))  

    text = big_font.render("Fin du jeu !", True, BLACK)
    screen.blit(text, (screen_width // 2 - 120, 50))

    score_container_width = 400
    score_container_height = 150
    score_container_x = screen_width // 2 - score_container_width // 2
    score_container_y = 150  

    pygame.draw.rect(screen, WHITE, (score_container_x, score_container_y, score_container_width, score_container_height), 0)
    pygame.draw.rect(screen, BLACK, (score_container_x, score_container_y, score_container_width, score_container_height), 5)  # Border

    score_text1 = font.render(f"Score Joueur 1 : {player_scores[0]}", True, BLACK)
    score_text2 = font.render(f"Score Joueur 2 : {player_scores[1]}", True, BLACK)
    
    screen.blit(score_text1, (score_container_x + 20, score_container_y + 20))  
    screen.blit(score_text2, (score_container_x + 20, score_container_y + 60))  

    replay_text = font.render("Appuyez sur 'R' pour rejouer", True, BLACK)
    screen.blit(replay_text, (screen_width // 2 - 160, 250))

    pygame.display.flip()

def game_loop():
    player1 = Player(100, 200, 0, {"jump": pygame.K_w, "slide": pygame.K_s})
    player2 = Player(100, 500, screen_height//2, {"jump": pygame.K_UP, "slide": pygame.K_DOWN})
    
    obstacles1, obstacles2 = [], []
    bonuses1, bonuses2 = [], []

    spawn_timer1 = spawn_timer2 = 0
    bonus_timer1 = random.randint(200, 300)
    bonus_timer2 = random.randint(250, 350)

    run = True
    final_screen = False

    while run:
        clock.tick(60)
        screen.blit(background_image, (0, 0))        
        draw_divider()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if not final_screen:
            player1.update()
            player2.update()

            spawn_timer1 += 1
            spawn_timer2 += 1
            if spawn_timer1 > 90 and player1.alive:
                obstacle_y1 = player1.rect.y + 20  
                obstacles1.append(Obstacle(screen_width, obstacle_y1))
                spawn_timer1 = 0
            if spawn_timer2 > 90 and player2.alive:
                obstacle_y2 = player2.rect.y + 20  
                obstacles2.append(Obstacle(screen_width, obstacle_y2))
                spawn_timer2 = 0


            bonus_timer1 -= 1
            bonus_timer2 -= 1
            if bonus_timer1 <= 0:
                bonuses1.append(Bonus(screen_width, random.randint(screen_height//2 - 170, screen_height//2 - 100)))
                bonus_timer1 = random.randint(300, 400)
            if bonus_timer2 <= 0:
                bonuses2.append(Bonus(screen_width, random.randint(screen_height - 170, screen_height - 100)))
                bonus_timer2 = random.randint(300, 400)

            for ob in obstacles1: ob.update()
            for ob in obstacles2: ob.update()
            for b in bonuses1: b.update()
            for b in bonuses2: b.update()

            for ob in obstacles1:
                if player1.rect.colliderect(ob.rect) and player1.alive and not player1.shield:
                    player1.alive = False
            for ob in obstacles2:
                if player2.rect.colliderect(ob.rect) and player2.alive and not player2.shield:
                    player2.alive = False

            for b in bonuses1:
                if player1.rect.colliderect(b.rect):
                    player1.collect_bonus(b.kind)
                    bonuses1.remove(b)
            for b in bonuses2:
                if player2.rect.colliderect(b.rect):
                    player2.collect_bonus(b.kind)
                    bonuses2.remove(b)

            if player1.alive: player1.score += 1
            if player2.alive: player2.score += 1

            player1.draw(screen, GREEN)
            for ob in obstacles1: ob.draw(screen)
            for b in bonuses1: b.draw(screen)
            
            player2.draw(screen, BLUE)
            for ob in obstacles2: ob.draw(screen)
            for b in bonuses2: b.draw(screen)

            s1 = f"Score: {player1.score} | ⚔️ {player1.weapons} 🛡️ {player1.armors}"
            s2 = f"Score: {player2.score} | ⚔️ {player2.weapons} 🛡️ {player2.armors}"
            screen.blit(font.render(s1, True, BLACK), (10, 10))
            screen.blit(font.render(s2, True, BLACK), (10, screen_height//2 + 10))

            if not player1.alive:
                screen.blit(font.render("Game Over", True, RED), (screen_width - 200, 10))
            if not player2.alive:
                screen.blit(font.render("Game Over", True, RED), (screen_width - 200, screen_height//2 + 10))

            if not player1.alive and not player2.alive:
                final_screen = True

            pygame.display.flip()
        else:
            display_game_over((player1.score, player2.score))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_loop()

    pygame.quit()
    sys.exit()

game_loop()
