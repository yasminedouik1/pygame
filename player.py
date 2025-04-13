import pygame

player_width = 90
player_height = 90
slide_height = 60

class Player:
    def __init__(self, x, y, zone_top, controls, image_base_path):
        self.default_y = y
        self.rect = pygame.Rect(x, y, player_width, player_height)
        self.zone_top = zone_top
        self.controls = controls
        self.jump = False
        #fl vertical axis l player yatlaa l -15
        self.jump_vel = -18
        self.vel_y = 0
        self.score = 0
        self.alive = True
        self.is_sliding = False
        self.slide_timer = 0
        self.shield = False
        self.shield_timer = 0
        self.weapons = 0
        self.money = 0


        self.image1 = pygame.image.load(image_base_path.replace(".png", ".1.png"))
        self.image2 = pygame.image.load(image_base_path.replace(".png", ".2.png"))
        

        self.image_shield1 = pygame.image.load(image_base_path.replace(".png", ".3.png"))
        self.image_shield2 = pygame.image.load(image_base_path.replace(".png", ".4.png"))
        

        self.image_dead = pygame.image.load(image_base_path.replace(".png", ".5.png"))  # For dead state

        self.image_slide = pygame.image.load(image_base_path.replace(".png", ".slide.png"))
        self.image_slide_shield = pygame.image.load(image_base_path.replace(".png", ".slide_shield.png"))


        self.image_slide = pygame.transform.scale(self.image_slide, (player_width, slide_height))
        self.image_slide_shield = pygame.transform.scale(self.image_slide_shield, (player_width, slide_height))

        self.image1 = pygame.transform.scale(self.image1, (player_width, player_height))
        self.image2 = pygame.transform.scale(self.image2, (player_width, player_height))
        self.image_shield1 = pygame.transform.scale(self.image_shield1, (player_width, player_height))
        self.image_shield2 = pygame.transform.scale(self.image_shield2, (player_width, player_height))
        self.image_dead = pygame.transform.scale(self.image_dead, (100, 100))
        self.current_image = self.image1
        self.image_timer = 0
        self.image_switch_delay = 30  


        self.death_timer = 0

    def update(self):
        if self.alive:
            keys = pygame.key.get_pressed()

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

            # Handle sliding

            if keys[self.controls["slide"]] and not self.jump:
                self.rect.height = slide_height
                self.rect.y = self.default_y + (player_height - slide_height)
                self.is_sliding = True
                if self.shield:
                    self.current_image = self.image_slide_shield
                else:
                    self.current_image = self.image_slide
            else:
                if not self.jump:
                    self.rect.height = player_height
                    self.rect.y = self.default_y
                    self.is_sliding = False

            # Animate run
            if not self.is_sliding:  
                self.image_timer += 1
                if self.image_timer >= self.image_switch_delay:
                    self.image_timer = 0
                    if not self.shield:
                        self.current_image = self.image2 if self.current_image == self.image1 else self.image1
                    else:
                        self.current_image = self.image_shield2 if self.current_image == self.image_shield1 else self.image_shield1

        if self.shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield = False
                self.current_image = self.image1

        if not self.alive:
            self.current_image = self.image_dead

            # Track time for image change to player1.6 (after 3 seconds)
            #if self.death_timer == 0:
                #This function returns the number of milliseconds since the game started.
               # self.death_timer = pygame.time.get_ticks()  # Set the time of death

            # After 3 seconds, change to player1.6
           # if pygame.time.get_ticks() - self.death_timer >= 3000:
             #   self.current_image = self.image_dead

    def draw(self, screen, color=None):
        screen.blit(self.current_image, self.rect.topleft)
        if self.shield:
            pygame.draw.rect(screen, (0, 0, 0), self.rect.inflate(10, 10), 3)

    def collect_bonus(self, kind):
        if not self.alive:
            return 

        if kind == "shield":
            self.shield = True
            self.shield_timer = 300  
            self.current_image = self.image_shield1  
        elif kind == "weapon":
            self.weapons += 1
        elif kind == "armor":
            self.money += 1


    def die(self):
        self.alive = False  
        self.death_timer = 0  