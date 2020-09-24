import pygame
import os
from enemies import Enemy


class RangedCreep(Enemy):
    def __init__(self, log_level):
        self.width = 96
        self.height = 96
        super().__init__(log_level)
        creep_img = pygame.image.load(os.path.join("assets","enemies","ranged_creep.png"))
        creep_img = pygame.transform.scale(creep_img, (self.width, self.height))
        self.imgs.append(creep_img)

        self.max_health = 20
        self.health = 20

