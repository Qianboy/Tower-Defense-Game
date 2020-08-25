import pygame
import os
from enemies import Enemy


class Roshan(Enemy):
    def __init__(self, log_level):
        super().__init__(log_level)
        creep_img = pygame.image.load(os.path.join("assets","enemies","roshan.png"))
        self.width = int(1.5 * self.width)
        self.height = int(1.5 * self.height)
        creep_img = pygame.transform.scale(creep_img, (self.width, self.height))
        self.imgs.append(creep_img)

