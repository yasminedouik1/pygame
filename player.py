import pygame

player_width = 50
player_height = 50
slide_height = 30

class Player:
    def __init__(self, x, y, zone_top, controls):
        self.default_y = y
        self.rect = pygame.Rect(x, y, player_width, player_height)
        self.zone_top = zone_top
        self.controls = controls
        self.jump = False
        self.jump_vel = -15
        self.vel_y = 0
        self.score = 0
        self.alive = True
        self.is_sliding = False
        self.slide_timer = 0
        self.shield = False
        self.shield_timer = 0
        self.weapons = 0
        self.armors = 0

    def update(self):
        if self.alive:
            keys = pygame.key.get_pressed()

            # Gestion du saut
            if keys[self.controls["jump"]] and not self.jump and not self.is_sliding:
                self.jump = True
                self.vel_y = self.jump_vel
            if self.jump:
                self.rect.y += self.vel_y
                self.vel_y += 1
                ground = self.zone_top + 200
                if self.rect.y >= ground:
                    self.rect.y = ground
                    self.jump = False

            # Gestion du slide
            if keys[self.controls["slide"]] and not self.jump:  # Si la touche slide est enfoncée et pas en train de sauter
                self.rect.height = slide_height  # Réduit la hauteur pour le slide
                self.rect.y = self.default_y + (player_height - slide_height)  # Déplace le joueur vers le bas
                self.is_sliding = True
            else:
                if not self.jump:  # Only reset if not jumping
                    self.rect.height = player_height  # Remet la hauteur originale du joueur
                    self.rect.y = self.default_y  # Remet le joueur à sa position de départ
                    self.is_sliding = False

        # Bouclier
        if self.shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield = False

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)
        if self.shield:
            pygame.draw.rect(screen, (0, 255, 255), self.rect.inflate(10, 10), 3)

    def collect_bonus(self, kind):
        if kind == "shield":
            self.shield = True
            self.shield_timer = 180  # 3 sec à 60 FPS
        elif kind == "weapon":
            self.weapons += 1
        elif kind == "armor":
            self.armors += 1
