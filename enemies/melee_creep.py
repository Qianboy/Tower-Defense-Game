import pygame
import os
from enemies import Enemy


class MeleeCreep(Enemy):
    def __init__(self, log_level):
        self.width = 96
        self.height = 96
        super().__init__(log_level)

        creep_img = pygame.image.load(os.path.join("assets","enemies","melee_creep.png"))
        creep_img = pygame.transform.scale(creep_img, (self.width, self.height))
        self.imgs.append(creep_img)

        self.max_health = 30
        self.health = 30


