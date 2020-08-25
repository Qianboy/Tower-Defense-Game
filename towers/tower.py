import pygame

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.price = [0,0,0]
        self.sell_price = [0,0,0]
        self.level = 1
        self.selected = False
        self.menu = None
        self.tower_imgs = []

    def draw(self, win):
        img = self.tower_imgs[self.level]
        win.blit(img,(self.x-img.get_width()//2, self.y-img.get_height()//2))

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