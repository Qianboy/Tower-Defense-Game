import pygame
import numpy as np
import pickle
import logging


class Enemy:
    def __init__(self, log_level):
        # position
        logging.basicConfig()
        self.logger = logging.getLogger('Enemy')
        self.logger.setLevel(log_level)
        self.width = 90
        self.height = 90
        self.vel = 1
        self.animation_count = 0
        self.health = 1
        # load saved via points for path
        with open('path.pkl', 'rb') as f:
            self.path = pickle.load(f)
        # create init point outside of window so enemy will walk into the window
        self.x, self.y = [self.path[0][0] - self.width,self.path[0][1]]
        self.target_viapoint_index = 0
        self.imgs = []
        self.reach_final = 0
        self.flip = 0

    def draw(self,win):
        """
        # Draws the enemy with given images
        :param win:
        :return:
        """
        self.img = self.imgs[self.animation_count]
        if self.flip:
            draw_img = pygame.transform.flip(self.img, True, False)
        else:
            draw_img = self.img
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        self.logger.debug('Draw enemy at position of [%s,%s]'%(self.x, self.y))
        win.blit(draw_img, (self.x-self.width//2, self.y-self.height//2))
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

    @staticmethod
    def _check_if_reach_next_target(current_pos,last_target,next_target):
        """
        check if the next target is reached (passed)
        :param current_pos: [x,y]
        :param last_target: [x,y]
        :param next_target: [x,y]
        :return:
        """
        distance = np.linalg.norm([current_pos[0]-last_target[0],
                                   current_pos[1]-last_target[1]])
        length = np.linalg.norm([next_target[0]-last_target[0],
                                 next_target[1]-last_target[1]])
        if distance > length:
            return True
        else:
            return False

    def move(self):
        """
        Move enemy following path
        :return: None
        """
        x1,y1 = self.path[self.target_viapoint_index-1]
        x2,y2 = self.path[self.target_viapoint_index]
        distance = np.linalg.norm([x2-x1,y2-y1])
        angle = np.arctan((y2-y1)/(x2-x1+ 0.0001))
        move_x = self.vel * np.abs(np.cos(angle))
        move_y = self.vel * np.abs(np.sin(angle))
        self.logger.debug('next move goes in direction of %s x and %s y'%(np.sign(x2-x1),np.sign(y2-y1)))
        x_new, y_new = [self.x + np.sign(x2-x1) * move_x,
                        self.y + np.sign(y2-y1) * move_y]
        # flipping enemy if it goes backwards
        mark_straight_line_x_error = 5
        if x2 < x1 - mark_straight_line_x_error:
            # original image needs flip once
            self.flip = 0
        else:
            self.flip = 1

        if self._check_if_reach_next_target([x_new,y_new],
                                            last_target=[x1,y1],
                                            next_target=[x2,y2]):
            self.x,self.y = x2,y2
            self.target_viapoint_index += 1
            if self.target_viapoint_index >= len(self.path):
                self.reach_final = 1
        else:
            self.x, self.y = x_new, y_new

    def hit(self):
        """
        Return if an enemy was dead
        :return:
        """
        self.health -= 1
        if self.health <= 0:
            return True