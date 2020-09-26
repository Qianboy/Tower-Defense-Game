import pygame
from towers import Tower
import os
import numpy as np
from time import time


class ArcherTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs = []
        self.archer_imgs = []
        self.archer_count = []
        self.draw_range = False
        img = super().load_img("archer_tower.png")
        self.tower_imgs.append(img)
        img = super().load_img("archer_tower_2.png")
        self.tower_imgs.append(img)
        img = super().load_img("archer_tower_3.png")
        self.tower_imgs.append(img)
        # Tower attributes
        self.range = 200
        self.damage = 10
        self.attack_interval = 1 #second
        self.last_hit_timer = time()

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
        Args:
            enemies:

        Returns:

        """
        if time() - self.last_hit_timer > self.attack_interval:
            self.inRange = False
            # shoot the closest enemy
            # TODO change policy to attack the very first enemy instead
            enemy_in_range = []
            for enemy in enemies:
                distance = np.linalg.norm([self.x - enemy.x, self.y - enemy.y])
                if distance < self.range:
                    self.inRange = True
                    enemy_in_range.append(enemy)

            if len(enemy_in_range):
                # Attack the enemy on the front
                # TODO enemy has attribute of life long
                life_max = 0
                front_enemy_index = 0
                for index, enemy in enumerate(enemy_in_range):
                    if enemy.life> life_max:
                        life_max = enemy.life
                        front_enemy_index = index
                attacked_enemy = enemy_in_range[front_enemy_index]
                attacked_enemy.hit(self.damage)

            self.last_hit_timer = time()
