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
        self.tower_imgs = []
        # attack animation parameters
        self.attack_img = []
        self.attack_anno_start_angle = 45 #deg
        self.bullet_from_x = self.x
        self.bullet_from_y = self.y - self.height//2
        self.attack_time = 0.5 #time for bullet to fly

        self._load_offline_images()
        self.last_hit_timer = time()

        # Tower attributes
        self._range = [200,220,250]
        self._damage = [10,20,30]
        self.attack_interval = 1 #second
        self._price = [100, 200, 300]
        self._sell_price = [50, 100, 150]

    def _load_offline_images(self):
        img = super().load_img("archer_tower.png")
        self.tower_imgs.append(img)
        img = super().load_img("archer_tower_2.png")
        self.tower_imgs.append(img)
        img = super().load_img("archer_tower_3.png")
        self.tower_imgs.append(img)
        path_to_project = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
        attack_img = pygame.image.load(os.path.join(path_to_project, "assets", "towers", "archer_arrow.png"))
        # pygame image [width, height]
        attack_img = pygame.transform.rotate(attack_img,-45)
        attack_img = pygame.transform.scale(attack_img, (30,30))
        self.attack_img = attack_img

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

        """
        self._attack(enemies)

    def draw_attack_annotation(self,win,interval):
        self._draw_attack_annotation(win,interval,traj='parabola')