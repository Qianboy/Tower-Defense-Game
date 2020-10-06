import pygame
from towers import Tower
import os
import numpy as np
from time import time

class CannonTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs = []
        self.archer_imgs = []
        self.archer_count = []
        self.tower_imgs = []
        self.attack_img = []
        self._load_offline_images()
        self.last_hit_timer = time()
        # attack animation parameters
        self.attack_time = 0.15
        self.bullet_from_x = self.x - self.width//3
        self.bullet_from_y = self.y + self.height // 4

        # Tower attributes
        self._range = [100,120,150]
        self._damage = [5,8,12]
        self.attack_interval = 0.3 #second
        self._price = [100, 200, 300]
        self._sell_price = [50, 100, 150]

    def _load_offline_images(self):
        img = super().load_img("cannon_2.png")
        img = pygame.transform.flip(img,True,False)
        self.tower_imgs.append(img)
        img = super().load_img("cannon_3.png")
        img = pygame.transform.flip(img,True,True)
        self.tower_imgs.append(img)
        path_to_project = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
        attack_img = pygame.image.load(os.path.join(path_to_project, "assets", "towers", "bullet.png"))
        # pygame image [width, height]
        self.attack_img = pygame.transform.scale(attack_img, (20,20))

    def draw(self, win):
        """
        Draw attack range as circle when the flag is true
        Args:
            win:

        Returns:

        """
        self._draw(win)

    def attack(self, enemies):
        """
        attacks an enemy in the enemy list, modifies the list
        Args:
            enemies:
        Returns:

        """
        self._attack(enemies)

    def draw_attack_annotation(self,win,interval):
        self._draw_attack_annotation(win,interval,traj='straight')