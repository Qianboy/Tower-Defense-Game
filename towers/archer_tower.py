import pygame
from towers import Tower
import os
import numpy as np

class ArcherTower(Tower):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.tower_imgs = []
        self.archer_imgs = []
        self.archer_count = []

        tower_img = pygame.image.load(os.path.join("assets", "towers", "archer_tower.png"))
        tower_img = pygame.transform.scale(tower_img, (self.width, self.height))
        self.tower_imgs.append(tower_img)

        # Tower attributes
        self.range = 100

    def draw(self, win):
        super().draw(win)
        # if self.archer_count >= len(self.archer_imgs):
        #     self.archer_count = 0
        # archer = self.archer_count[self.archer_count]
        # win.blit(archer,((self.x+self.width//2 - archer.get_width()//2),
        #                  (self.y+self.height//2 - archer.get_height()//2)))

        # draw range circle TODO buggy here
        surface = pygame.Surface((self.range*4,self.range*4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (255, 0, 0, 80), (self.x, self.y), self.range, 0)
        pygame.draw.line(surface, (0,255,0,80), (self.x-10, self.y),(self.x+10, self.y),2)
        win.blit(surface,(self.x - self.range,self.y - self.range))

    def attack(self, enemies):
        """
        attacks an enemy in the enemy list, modifies the list
        :param enemies:
        :return:
        """
        self.inRange = False
        # shoot the closest enemy
        # TODO change policy to attack the very first enemy instead
        enemy_closest = []
        for enemy in enemies:
            distance = np.linalg.norm([self.x - enemy.x,self.y - enemy.y])
            if distance < self.range:
                self.inRange = True
                enemy_closest.append(enemy)
