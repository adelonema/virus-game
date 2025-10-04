import pygame, sys
from pygame.locals import *
import random, time
import plotly.express as px

#Initializing
pygame.init()

#Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Variables to manage the background change
background_delay = 800  # milliseconds
background_time  = 0     # when the background last changed
backgrounds      = px.colors.sequential.Viridis + px.colors.sequential.Viridis[-1::-1] # [ WHITE, BLUE, WHITE, BLUE, BLUE ]
background_index = 0     # index of the currently used background

# Screen information
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SPEED = 5

# Scoring
LIFEPOINTS = 2
HIGHSCORE = 0

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Super Mega Game")

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 140)
font_small = pygame.font.SysFont("Verdana", 60)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.speed = pygame.time.get_ticks()/3000 + 5
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        self.image = pygame.image.load("PowerUp.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.speed = pygame.time.get_ticks() / 3000 + 5
            self.rect.top = 0
            self.rect.center = (random.randint(30, SCREEN_WIDTH-30), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 720)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        playerspeed = pygame.time.get_ticks() / 5000 + 5
        if self.rect.top < SCREEN_HEIGHT/1:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -playerspeed)
        if self.rect.bottom > 0:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,playerspeed)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-playerspeed, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(playerspeed, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#Setting up Sprites
P1 = Player()
E1 = Enemy(10)
E2 = Enemy(12)
POWER_UP_1 = PowerUp(15)

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
enemies.add(E2)
powerups = pygame.sprite.Group()
powerups.add(POWER_UP_1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(E2)
all_sprites.add(POWER_UP_1)

# #Adding a new User event
# INC_SPEED = pygame.USEREVENT + 1
# pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:
    # Cycles through all events occuring
    for event in pygame.event.get():
        # if event.type == INC_SPEED:
        #     SPEED += 2

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # P1.move()
    # E1.move()
    # E2.move()
    # POWER_UP_1.move()

    # Re-draw the screen background from the list after a delay
    time_now = pygame.time.get_ticks()
    if time_now > background_time + background_delay:
        # switch to the next background
        background_time = time_now
        background_index += 1
        # if we're out of backgrounds, start back at the head of the list
        if background_index >= len(backgrounds):
            background_index = 0

    # Show life points in top left corner:
    DISPLAYSURF.fill(backgrounds[ background_index ])
    text_surface = font_small.render(f'Life: {LIFEPOINTS}', True, (0, 0, 0))
    DISPLAYSURF.blit(text_surface, dest=(0, 0))

    # Show score in top right corner:
    text_surface = font_small.render(f'Score: {int(time_now/10)}', True, (0, 0, 0))
    text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH, 0))
    DISPLAYSURF.blit(text_surface, text_rect)

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    # P1.draw(DISPLAYSURF)
    # E1.draw(DISPLAYSURF)
    # E2.draw(DISPLAYSURF)
    # POWER_UP_1.draw(DISPLAYSURF)

    # To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollide(P1, enemies, dokill=True):
        pygame.mixer.Sound('crash.wav').play()
        E1 = Enemy(time_now/3000 + 5)
        enemies.add(E1)
        all_sprites.add(E1)
        DISPLAYSURF.fill(RED)
        pygame.display.update()
        LIFEPOINTS -= 1
        if LIFEPOINTS == 0:
            for entity in all_sprites:
                entity.kill()
            CURRENTSCORE = int(time_now/10)
            HIGHSCORE_TEXT = open("highscore.txt")
            HIGHSCORE = int(HIGHSCORE_TEXT.read())
            HIGHSCORE_TEXT.close()
            game_over = font.render(f"GAME OVER", True, BLACK)
            game_over1 = font_small.render(f"This Game's Score: {CURRENTSCORE}", True, BLACK)
            game_over2 = font_small.render(f"Highscore: {HIGHSCORE}", True, BLACK)
            if HIGHSCORE < CURRENTSCORE:
                with open("highscore.txt", "w") as f:
                    f.write(f"{CURRENTSCORE}")
            text_rect = game_over.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 180))
            text_rect1 = game_over1.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
            text_rect2 = game_over2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200))
            DISPLAYSURF.blit(game_over, text_rect)
            DISPLAYSURF.blit(game_over1, text_rect1)
            DISPLAYSURF.blit(game_over2, text_rect2)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            sys.exit()

    if pygame.sprite.spritecollide(P1, powerups, dokill=True):
        POWER_UP_1 = PowerUp(time_now/3000 + 5)
        powerups.add(POWER_UP_1)
        all_sprites.add(POWER_UP_1)
        LIFEPOINTS += 1
        DISPLAYSURF.fill(GREEN)
        pygame.display.update()


    pygame.display.update()
    FramePerSec.tick(FPS)