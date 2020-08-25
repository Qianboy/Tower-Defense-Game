import pygame
from towers import Tower

class ArcherTower(Tower):
    def __init__(self,x,y):
        super().__init__(self,x,y)
        self.tower_imgs = []
        self.archer_imgs = []
        self.archer_count = []

        creep_img = pygame.image.load(os.path.join("assets", "towers", "archer_tower.png"))

    def draw(self, win):
        super().draw(win)

    def attack(self, enemies):
        """
        attacks an enemy in the enemy list, modifies the list
        :param enemies:
        :return:
        """