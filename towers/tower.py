import pygame
import os
import numpy as np
import cv2
from time import time

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 96
        self.height = 96
        self.level = 1
        self.selected = False
        self.menu = None
        self.tower_imgs = []

    @property
    def price(self):
        return self._price[self.level - 1]

    @property
    def sell_price(self):
        return self._sell_price[self.level - 1]

    @property
    def range(self):
        return self._range[self.level - 1]

    @property
    def damage(self):
        return self._damage[self.level - 1]

    def load_img(self,image_name):
        """
        load images by pygame and scale it to width of 64
        Args:
            image_name: string

        Returns: tower_img[Surface]: loaded pygame image

        """
        path_to_project = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
        image = cv2.imread(os.path.join(path_to_project,"assets", "towers", image_name))
        # image [height, width]
        scale = image.shape[0]//self.height
        tower_img = pygame.image.load(os.path.join(path_to_project,"assets", "towers", image_name))
        # pygame image [width, height]
        tower_img = pygame.transform.scale(tower_img, (image.shape[1]//scale, image.shape[0]//scale))
        return tower_img

    def draw(self, win):

        img = self.tower_imgs[self.level - 1]
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))

    def click(self, x, y):
        """
        returns True if tower has been clicked
        :param x: int
        :param y: int
        :return: bool
        """
        if self.x + self.width >= x > self.x:
            if self.y + self.height >= y > self.y:
                return True
        return False

    def sell(self):
        """
        call to sell the tower, returns sell price
        :return: int
        """
        return self.sell_price[self.level - 1]

    def upgrade(self):
        """
        upgrades the tower for a given cost
        :return:
        """
        self.level += 1

    def get_upgrade_cost(self):
        """
        returns the upgrade cost, if 0 then cannot upgrade anymore
        :return:
        """
        return self.price[self.level-1]

    def move(self,x,y):
        self.x = x
        self.y = y

    def _attack(self,enemies, range, damage):
        """
        Find the first enemies in the attack range and attack it
        Args:
            enemies:

        Returns:

        """

        enemy_in_range = []
        for enemy in enemies:
            distance = np.linalg.norm([self.x - enemy.x, self.y - enemy.y])
            if distance < range:
                self.inRange = True
                enemy_in_range.append(enemy)
        if len(enemy_in_range):
            age_max = 0
            front_enemy_index = 0
            for index, enemy in enumerate(enemy_in_range):
                if enemy.age > age_max:
                    age_max = enemy.life
                    front_enemy_index = index
            attacked_enemy = enemy_in_range[front_enemy_index]
            attacked_enemy.hit(damage)
