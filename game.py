import pygame
import os
import pickle
from enemies import RangedCreep, MeleeCreep, Roshan
from towers import ArcherTower, EagleTower, CannonTower
import logging
from time import time
import random
pygame.font.init()


class Game:
    def __init__(self):
        self.log_level = logging.INFO
        logging.basicConfig()
        self.logger = logging.getLogger('Game')
        self.logger.setLevel(self.log_level)

        # game attributes
        self.width = 900
        self.height = 600
        self.fps = 100
        self.win = pygame.display.set_mode((self.width,self.height))
        # comment this for develop
        self.enemies = [RangedCreep(self.log_level)]
        self.last_spawn_enemy_time = time()
        # x width, y height
        self.towers = [ArcherTower(x=100,y=100),EagleTower(x=250,y=200), CannonTower(x=500,y=450)]

        # UI stuff
        self.lifes = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("assets","bg.png"))
        self.bg = pygame.transform.scale(self.bg,(self.width,self.height))
        self.life_font = pygame.font.SysFont("comicsans",30)
        self.life_image = pygame.image.load(os.path.join("assets","frontend","heart.jpg"))
        self.money_font = pygame.font.SysFont("comicsans",30)
        self.money_image = pygame.image.load(os.path.join("assets","frontend","coin.png"))

    def _activate_mouse_touch_action(self,position):
        """
        make tower bigger when cursor is on the tower
        Args:
            position: [x,y]

        Returns:

        """
        for tower in self.towers:
            tower.touch(position[0], position[1])

    def _activate_mouse_click_action(self,position):
        """
        Check where the mouse clicked, for tower then the attack range will be displayed
        Args:
            position: [x,y]

        Returns:

        """
        # self.logger.debug('Pressed bottom is %s'%position)
        clicked_tower_index = 0
        for tower in self.towers:
            tower.click(position[0],position[1])

        for enemy in self.enemies:
            # TODO show enemy HP bar and info
            pass

    def _spawn_enemy(self,interval):
        if time() - self.last_spawn_enemy_time > interval:
            self.enemies.append(random.choice([RangedCreep(self.log_level),MeleeCreep(self.log_level),Roshan(self.log_level)]))
            self.last_spawn_enemy_time = time()

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(self.fps)
            self._spawn_enemy(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # if any mouse button is pressed
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # if the left button is pressed
                    if event.button == 1:
                        self._activate_mouse_click_action(event.pos)
                else:
                    self._activate_mouse_touch_action(pygame.mouse.get_pos())

            to_del = []
            for enemy in self.enemies:
                # works only for moving from left to right
                if enemy.reach_final:
                    self.lifes -= enemy.life
                    to_del.append(enemy)
                if enemy.health <= 0: 
                    to_del.append(enemy)
            for d in to_del:
                self.enemies.remove(d)
            to_del = []
            for tower in self.towers:
                if tower.sold:
                    to_del.append(tower)
                    self.money += tower.sell_price
                else:
                    tower.attack(self.enemies)
            for d in to_del:
                self.towers.remove(d)

            if self.lifes < 0:
                print('You Loser!!!')
                run = False
            self.draw()
        pygame.quit()

    def _draw_black_rectangle(self,start_x,length):
        """
        Draw transparent black rectangle for displaying numbers e.g., money, lifes
        Returns:

        """
        s = pygame.Surface((length, 30))  # the size of your rect
        s.set_alpha(200)  # alpha level
        s.fill((50, 50, 50))  # this fills the entire surface
        self.win.blit(s, (start_x, 10))  # (0,0) are the top-left coordinates

    def draw(self):
        self.win.blit(self.bg,(0,0))
        # draw enemies
        for enemy in self.enemies:
            enemy.draw(self.win)

        # draw towers
        for tower in self.towers:
            tower.draw(self.win)

        # draw life
        life_text = self.life_font.render(str(self.lifes), 1, (255, 255, 255))
        heart = pygame.transform.scale(self.life_image, (30, 30))
        start_heart_x = 15
        self._draw_black_rectangle(start_heart_x+15,length=45)
        self.win.blit(life_text, (start_heart_x + heart.get_width(), 14))
        self.win.blit(heart, (start_heart_x, 12))

        # draw money
        coin_text = self.money_font.render(str(self.money), 1, (255,255,255))
        coin = pygame.transform.scale(self.money_image, (30,30))
        start_coin_x = start_heart_x + life_text.get_width() +heart.get_width() + 10
        self._draw_black_rectangle(start_coin_x+15,length=55)
        self.win.blit(coin_text,(start_coin_x + coin.get_width(), 14))
        self.win.blit(coin,(start_coin_x,9))

        pygame.display.update()

    def develop(self):
        """
        for developers to capture path for enemies
        :return:
        """
        run = True
        clock = pygame.time.Clock()
        clicks = []
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicks.append(pos)

            self.win.blit(self.bg, (0, 0))
            for p in clicks:
                pygame.draw.circle(self.win,(255,0,0),(p[0],p[1]),5,0)
            with open(os.path.join('enemies','path.pkl'), 'wb') as f:
                pickle.dump(clicks, f)
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    # game.develop()
    game.run()
    # enemy = Enemy(1,1,1,1)