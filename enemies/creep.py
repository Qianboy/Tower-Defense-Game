import pygame
import os
from enemies import Enemey

class Creep(Enemey):
    def __init__(self,log_level):
        super().__init__(log_level)
        creep_img = pygame.image.load(os.path.join("assets","enemies","creep.png"))
        creep_img = pygame.transform.scale(creep_img, (self.width, self.height))
        self.imgs.append(creep_img)

