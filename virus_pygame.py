import pygame
from pygame.locals import *
import random
import numpy as np
import math
from matplotlib import pyplot as plt
from collections import Counter


# =============================================================================
# Global variables:
# =============================================================================

TIMEFRAMES = 200
NUM_POINTS = 600
DIMENSIONS = 400
INF_DISTANCE = 20
INF_PROB = .1
RECOVERY_TIME = 20
RECOVERY_RESET = 30
SPEED = 7

STATUS2COLOR = {
    "Sane": "slategrey",
    "Infected": "indianred",
    "Recovered": "darkseagreen"
}

# =============================================================================
# Initialise pygame:
# =============================================================================

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

