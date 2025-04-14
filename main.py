import pygame
import random
import sys
from player import Player
from obstacle import Obstacle
from bonus import Bonus

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Crash & Dash")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

background_image = pygame.image.load("./images/background.png")
background_rect = background_image.get_rect()

weapon_image = pygame.transform.scale(pygame.image.load("./images/weapon.png"), (20, 20))
money_image = pygame.transform.scale(pygame.image.load("./images/money.png"), (20, 20))


font = pygame.font.SysFont("poppins", 21, bold=True)
clock = pygame.time.Clock()

def draw_divider():
    pygame.draw.line(screen, BLACK, (0, screen_height // 2), (screen_width, screen_height // 2), 2)


game_over_background = pygame.image.load("./images/game over.jpg")
game_over_background = pygame.transform.scale(game_over_background, (800, 600)) 

def display_game_over(player_scores, player_weapons, player_money):
   
    screen.blit(game_over_background, (0, 0)) 
   
    score_text1 = font.render(f"Score Player 1: {player_scores[0]} | {player_weapons[0]} | {player_money[0]}", True, BLACK)
    score_text2 = font.render(f"Score Player 2: {player_scores[1]} | {player_weapons[1]} | {player_money[1]}", True, BLACK)

    screen.blit(score_text1, (265, 240))
    screen.blit(score_text2, (265, 305))

    replay_text = font.render("Press 'R' to Replay", True, BLACK)
    screen.blit(replay_text,(300, 410))

    pygame.display.flip()  


def game_loop():
 
    GROUND_OFFSET = 160 
    top_zone_top = 0      
    bottom_zone_top = top_zone_top + GROUND_OFFSET + 120  
    player1 = Player(100, top_zone_top + GROUND_OFFSET, top_zone_top, 
                    {"jump": pygame.K_w, "slide": pygame.K_s}, 
                    "./images/player1.png")
    player2 = Player(100, bottom_zone_top + GROUND_OFFSET, bottom_zone_top, 
                    {"jump": pygame.K_UP, "slide": pygame.K_DOWN}, 
                    "./images/player2.png")
    
    obstacles1, obstacles2 = [], []
    bonuses1, bonuses2 = [], []

    spawn_timer1 = spawn_timer2 = 0
    bonus_timer1 = random.randint(200, 300)
    bonus_timer2 = random.randint(250, 350)

    run = True
    final_screen = False

    while run:
        clock.tick(65)
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
                obstacles1.append(Obstacle(screen_width, player1.rect.y + 20))
                spawn_timer1 = 0
            if spawn_timer2 > 90 and player2.alive:
                obstacles2.append(Obstacle(screen_width, player2.rect.y + 20))
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

            player1.draw(screen)
            for ob in obstacles1: ob.draw(screen)
            for b in bonuses1: b.draw(screen)
            
            player2.draw(screen)
            for ob in obstacles2: ob.draw(screen)
            for b in bonuses2: b.draw(screen)

            s1 = f"Score: {player1.score} | Weapons : {player1.weapons} Money : {player1.money}"
            s2 = f"Score: {player2.score} | Weapons : {player2.weapons} Money : {player2.money}"
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
            display_game_over((player1.score, player2.score), (player1.weapons, player2.weapons), (player1.money, player2.money))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game_loop()

    pygame.quit()
    sys.exit()


