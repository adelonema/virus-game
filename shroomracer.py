import pygame, sys
from pygame.locals import *
import random, time
import plotly.express as px
import pandas as pd

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
font = pygame.font.SysFont("Verdana", 140, bold=True)
font_small = pygame.font.SysFont("Verdana", 60)
font_tiny = pygame.font.SysFont("Verdana", 30)

# Different sprite classes:
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


# Main game class:
class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.gameStateManager = GameStateManager('start')
        self.start = Start(self.screen, self.gameStateManager)
        self.level = Level(self.screen, self.gameStateManager)
        self.endscreen = Endscreen(self.screen, self.gameStateManager)

        self.states = {'start': self.start, 'level': self.level, 'endscreen': self.endscreen}

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if event.type == pygame.KEYDOWN:
                #     self.gameStateManager.set_state('level')
            self.states[self.gameStateManager.get_state()].run()

            pygame.display.update()
            FramePerSec.tick(FPS)


class Level:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        global background_index, background_time, LIFEPOINTS
        time_now = pygame.time.get_ticks()
        if time_now > background_time + background_delay:
            # switch to the next background
            background_time = time_now
            background_index += 1
            # if we're out of backgrounds, start back at the head of the list
            if background_index >= len(backgrounds):
                background_index = 0

        # Draw background
        DISPLAYSURF.fill(backgrounds[background_index])

        # Show life points in top left corner:
        text_surface = font_small.render(f'Life: {LIFEPOINTS}', True, (0, 0, 0))
        DISPLAYSURF.blit(text_surface, dest=(0, 0))

        # Show score in top right corner:
        text_surface = font_small.render(f'Score: {int(time_now / 10)}', True, (0, 0, 0))
        text_rect = text_surface.get_rect(topright=(SCREEN_WIDTH, 0))
        DISPLAYSURF.blit(text_surface, text_rect)

        # Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

        # Pick up power ups:
        if pygame.sprite.spritecollide(P1, powerups, dokill=True):
            POWER_UP_1 = PowerUp(time_now / 3000 + 5)
            powerups.add(POWER_UP_1)
            all_sprites.add(POWER_UP_1)
            LIFEPOINTS += 1
            DISPLAYSURF.fill(GREEN)
            pygame.display.update()

        # To be run if collision occurs between Player and Enemy
        if pygame.sprite.spritecollide(P1, enemies, dokill=True):
            pygame.mixer.Sound('crash.wav').play()
            E1 = Enemy(time_now / 3000 + 5)
            enemies.add(E1)
            all_sprites.add(E1)
            DISPLAYSURF.fill(RED)
            pygame.display.update()
            LIFEPOINTS -= 1
            if LIFEPOINTS == 0:
                for entity in all_sprites:
                    entity.kill()

                # write game score to temp files:
                with open("temp_score.txt", "w") as f:
                    f.write(f"{time_now / 10}")
                
                self.gameStateManager.set_state('endscreen')

class Start:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        self.display.fill('navajowhite')

        font_start = pygame.font.SysFont("Verdana", 60, italic=True)
        font_start_big = pygame.font.SysFont("Verdana", 80, bold=True)
        text_start = font_start.render("Welcome to the", True, BLACK)
        text_upcenter = text_start.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 180))
        DISPLAYSURF.blit(text_start, text_upcenter)
        text_start2 = font_start_big.render("SHROOM RACER!", True, "darkred")
        text_center = text_start2.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        DISPLAYSURF.blit(text_start2, text_center)
        text_keypress = font_tiny.render("Press <e> to start the game...", True, BLACK)
        text_bottom = text_keypress.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 270))
        DISPLAYSURF.blit(text_keypress, text_bottom)
        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            self.gameStateManager.set_state('level')

class Endscreen:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        self.display.fill('palegreen')

        # read temp files for game score and highscore:
        with open("temp_score.txt", "r") as f:
            CURRENTSCORE = f.read()
        with open("highscore.txt", "r") as f:
            HIGHSCORE = f.read()
        
        # # Writing empty data to scoretable
        # data = {"player": "<empty slot>",
        #         "score": [0] * 10}
        # scoretable = pd.DataFrame(data)
        # scoretable.to_csv("scoretable.csv")
        # # with open("scoretable.txt", "w") as f:
        # #     f.write(f"{scoretable}")

        # # Read previous scores:
        # scoretable = pd.read_csv("scoretable.csv", index_col=0)
        #
        # # Add new highscore to table, sort values and cut off after 10 entries:
        # scoretable.loc[len(scoretable)] = ["PLAYER", CURRENTSCORE]
        # scoretable = scoretable.sort_values(by="score", ascending=False)
        # scoretable = scoretable.iloc[0:10, :]
        #
        # scoretable.to_csv("scoretable.csv")

        if HIGHSCORE < CURRENTSCORE:
            user_text = ''
            input_caption = font.render(user_text, True, BLACK)
            input_rect = input_caption.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            DISPLAYSURF.blit(input_caption, input_rect)

            with open("highscore.txt", "w") as f:
                f.write(f"{CURRENTSCORE}")

        game_over = font.render(f"GAME OVER", True, BLACK)
        text_upcenter = game_over.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 180))
        DISPLAYSURF.blit(game_over, text_upcenter)

        game_score = font_small.render(f"This Game's Score: {CURRENTSCORE}", True, BLACK)
        text_midcenter = game_score.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
        DISPLAYSURF.blit(game_score, text_midcenter)

        game_highscore = font_small.render(f"Highscore: {HIGHSCORE}", True, BLACK)
        text_downcenter = game_highscore.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 200))
        DISPLAYSURF.blit(game_highscore, text_downcenter)

        game_cueend = font_tiny.render("Press <e> to exit, press <ENTER> to play again...", True, BLACK)
        text_lowestcenter = game_cueend.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 400))
        DISPLAYSURF.blit(game_cueend, text_lowestcenter)

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            pygame.quit()
            sys.exit()
        elif keys[pygame.K_RETURN]:
            LIFEPOINTS = 2
            self.gameStateManager.set_state('level')

# used this video for the GameStateManager setup: https://www.youtube.com/watch?v=r0ixaTQxsUI
class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

# def scoretable(CURRENTSCORE):
#

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

if __name__ == '__main__':
    game = Main()
    game.run()
