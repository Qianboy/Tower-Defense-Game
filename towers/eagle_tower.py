import pygame
from towers import Tower
import os
import numpy as np
from time import time

class EagleTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs = []
        self.archer_imgs = []
        self.archer_count = []
        self.draw_range = False
        self.tower_imgs = []
        self._load_offline_images()
        self.last_hit_timer = time()

        # Tower attributes
        self._range = [500,600,700]
        self._damage = [50,70,100]
        self.attack_interval = 5 #second
        self._price = [100, 200, 300]
        self._sell_price = [50, 100, 150]

    def _load_offline_images(self):
        img = super().load_img("eagle_artillery.png")
        self.tower_imgs.append(img)

    def draw(self, win):
        """
        Draw attack range as circle when the flag is true
        Args:
            win:

        Returns:

        """
        super().draw(win)
        if self.draw_range:
            surface = pygame.Surface((self.range*4,self.range*4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (255, 0, 0, 80), (self.x, self.y), self.range, 0)
            win.blit(surface,(0,0))

    def attack(self, enemies):
        """
        attacks an enemy in the enemy list, modifies the list
        :param enemies:
        :return:
        """
        if time() - self.last_hit_timer > self.attack_interval:
            self._attack(enemies,self.range,self.damage)
            self.last_hit_timer = time()
