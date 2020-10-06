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

        # attack animation parameters
        self.bullet_from_x = self.x - self.width // 2
        self.bullet_from_y = self.y - self.height // 2
        self.attack_time = 1.5 #time for bullet to fly

        # Tower attributes
        self._range = [500,600,700]
        self._damage = [50,70,100]
        self.attack_interval = 4 #second
        self._price = [100, 200, 300]
        self._sell_price = [50, 100, 150]

    def _load_offline_images(self):
        img = super().load_img("eagle_artillery.png")
        self.tower_imgs.append(img)
        path_to_project = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
        attack_img = pygame.image.load(os.path.join(path_to_project, "assets", "towers", "fire.png"))
        # pygame image [width, height]
        # attack_img = pygame.transform.rotate(attack_img, -45)
        attack_img = pygame.transform.scale(attack_img, (100, 100))
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
        :param enemies:
        :return:
        """
        self._attack(enemies)

    def draw_attack_annotation(self,win,interval):
        self._draw_attack_annotation(win,interval,traj='updown')