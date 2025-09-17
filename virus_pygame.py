import pygame, sys
from pygame.locals import *
import random
import plotly.express as px


pygame.init()

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
backgrounds      = px.colors.sequential.Viridis # [ WHITE, BLUE, WHITE, BLUE, BLUE ]
background_index = 0     # index of the currently used background

# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((400, 600))
# DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, 10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top < SCREEN_HEIGHT/1:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -7)
        if self.rect.bottom > 0:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,7)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-7, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(7, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

P1 = Player()
E1 = Enemy()
E2 = Enemy()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
    E1.move()
    E2.move()

    # Re-draw the screen background from the list after a delay
    time_now = pygame.time.get_ticks()
    if (time_now > background_time + background_delay):
        # switch to the next background
        background_time = time_now
        background_index += 1
        # if we're out of backgrounds, start back at the head of the list
        if (background_index >= len(backgrounds)):
            background_index = 0

    DISPLAYSURF.fill(backgrounds[ background_index ])
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)
    E2.draw(DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)