import pygame
from towers import Tower
import os
import numpy as np


class CannonTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs = []
        self.archer_imgs = []
        self.archer_count = []
        self.draw_range = False
        img = super().load_img("cannon_2.png")
        self.tower_imgs.append(img)
        img = super().load_img("cannon_3.png")
        self.tower_imgs.append(img)
        self.range = 500

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
        self.inRange = False
        # shoot the closest enemy
        # TODO change policy to attack the very first enemy instead
        enemy_in_range = []
        for enemy in enemies:
            distance = np.linalg.norm([self.x - enemy.x,self.y - enemy.y])
            if distance < self.range:
                self.inRange = True
                enemy_in_range.append(enemy)

        # Attack the enemy on the front
        # TODO enemy has attribute of life long
        # enemy = enemy_in_range[0]
