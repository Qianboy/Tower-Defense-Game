import pygame
import os
from enemies import Enemey

class Creep(Enemey):
    def __init__(self,x,y,log_level):
        super().__init__(x,y,log_level)
        self.imgs.append(pygame.image.load(os.path.join("assets","enemies","creep.png")))
