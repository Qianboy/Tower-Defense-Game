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
        self.attack_anno_counter = 0
        self.attacked_enemy = []
        # mouse event trigger flag
        self.draw_range = False
        self.touched = False
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

    @property
    def tower_img(self):
        return self.tower_imgs[self.level - 1]

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

    def _draw(self, win):

        img = self.tower_imgs[self.level - 1]
        if self.touched:
            img = pygame.transform.scale(img, (int(1.2 * img.get_width()),int(1.2 * img.get_height())))
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))
        if self.draw_range:
            surface = pygame.Surface((self.range*4,self.range*4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (255, 0, 0, 80), (self.x, self.y), self.range, 0)
            win.blit(surface,(0,0))
        self.draw_attack_annotation(win,interval=self.attack_time)

    def click(self, x, y):
        """
        returns True if tower has been clicked
        :param x: int
        :param y: int
        :return: bool
        """
        if self.x + self.width//2 >= x > self.x - self.width//2:
            if self.y + self.height//2 >= y > self.y - self.height//2:
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

    def _attack(self,enemies):
        """
        Find the first enemies in the attack range and attack it
        Args:
            enemies:

        Returns:

        """
        attacked_flag = False
        if time() - self.last_hit_timer > self.attack_interval:
            enemy_in_range = []
            for enemy in enemies:
                distance = np.linalg.norm([self.x - enemy.x, self.y - enemy.y])
                if distance < self.range:
                    self.inRange = True
                    enemy_in_range.append(enemy)
            if len(enemy_in_range):
                age_max = 0
                front_enemy_index = 0
                for index, enemy in enumerate(enemy_in_range):
                    if enemy.age > age_max:
                        age_max = enemy.age
                        front_enemy_index = index
                self.attacked_enemy = enemy_in_range[front_enemy_index]
                attacked_flag = True
            self.last_hit_timer = time()
            if attacked_flag:
                self.attack_anno_counter += 1

    def _draw_attack_annotation(self,win,interval=0,traj='straight'):
        """

        Args:
            win:
            interval:
            traj: 'straight', 'parabola','updown'

        Returns:

        """
        #TODO change the time from contact to distance dependent
        if self.attack_anno_counter != 0:
            fps = 100 #from game class
            start_x = self.bullet_from_x
            start_y = self.bullet_from_y
            end_x = self.attacked_enemy.x #- self.attacked_enemy.width//3
            end_y = self.attacked_enemy.y# - self.attacked_enemy.height//3
            start_angle = 45 #deg
            end_angle = -80
            counter_max = fps * interval

            if self.attack_anno_counter < counter_max*0.9:
                angle = (end_angle - start_angle) * self.attack_anno_counter / counter_max + start_angle

                if traj == 'straight':
                    draw_x = (end_x - start_x) * self.attack_anno_counter / counter_max + start_x
                    draw_y = (end_y - start_y) * self.attack_anno_counter / counter_max + start_y
                    attack_img = self.attack_img

                elif traj == 'parabola':
                    draw_x = (end_x - start_x) * self.attack_anno_counter / counter_max + start_x
                    middle_x = (start_x + end_x) // 2
                    middle_y = (start_y + end_y) // 2 - 50
                    a, b, c = np.polyfit([start_x, middle_x, end_x], [start_y, middle_y, end_y], 2)
                    draw_y = draw_x**2 * a + draw_x * b + c
                    attack_img = pygame.transform.rotate(self.attack_img,angle)

                elif traj == 'updown':
                    if self.attack_anno_counter < counter_max*3//4:
                        draw_x = start_x
                        ratio = (1 - self.attack_anno_counter/counter_max*2)
                        draw_y = int(start_y * ratio)
                        attack_img = self.attack_img
                    else:
                        draw_x = end_x - self.attack_img.get_width()//2
                        ratio = (self.attack_anno_counter- counter_max*3//4) / counter_max * 4
                        draw_y = int((end_y + self.attacked_enemy.height) * ratio)
                        attack_img = pygame.transform.flip(self.attack_img,False,True)
                # offset for attack img with it
                win.blit(attack_img, (draw_x,draw_y))
                self.attack_anno_counter += 1
            else:
                self.attacked_enemy.hit(self.damage)
                self.attack_anno_counter = 0
                self.attacked_enemy = []


