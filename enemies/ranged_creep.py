import pygame
import os
from enemies import Enemy
from time import time

class RangedCreep(Enemy):
    def __init__(self, log_level):
        self.width = 48
        self.height = 48
        super().__init__(log_level)
        creep_img = pygame.image.load(os.path.join("assets","enemies","ranged_creep.png"))
        creep_img = pygame.transform.scale(creep_img, (self.width, self.height))
        self.imgs.append(creep_img)

        self.max_health = 20
        self.health = self.max_health
        self.spawn_time = time()
        self._age = 1

        self._life = 1 # life cost when reaching destination


