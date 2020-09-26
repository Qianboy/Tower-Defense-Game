import pygame
import os
from enemies import Enemy
from time import time

class Roshan(Enemy):
    def __init__(self, log_level):
        self.width = 192
        self.height = 192
        super().__init__(log_level)
        creep_img = pygame.image.load(os.path.join("assets","enemies","roshan.png"))
        # self.width = int(1.5 * self.width)
        # self.height = int(1.5 * self.height)
        creep_img = pygame.transform.scale(creep_img, (self.width, self.height))
        self.imgs.append(creep_img)

        self.max_health = 100
        self.health = self.max_health
        self.spawn_time = time()
        self._life = 0

