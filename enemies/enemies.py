import pygame

class Enemey:
    imgs = []
    def __init__(self,x ,y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.health = 1
        self.path = []
        self.img = []

    def draw(self,win):
        """
        Draws the enemy with given images
        :param win:
        :return:
        """
        self.animation_count += 1
        self.img = Enemey.imgs[self.animation_count]
        if self.animation_count >= len(Enemey.imgs):
            self.animation_count = 0
        #draw
        win.blit(self.img,(self.x,self.y))
        self.move()

    def collide(self,x,y):
        """
        Returns if position has hit enemy
        :param x:
        :param y:
        :return: Bool
        """
        if x <= self.x +self.wdith and x >= self.x:
            if y <= self.y +self.height and y >= self.y:
                return True
        return False

    def move(self):
        """
        Move enemy following path
        :return: None
        """

    def hit(self):
        """
        Return if an enemey was dead
        :return:
        """
        self.health -= 1
        if self.health <= 0:
            return True