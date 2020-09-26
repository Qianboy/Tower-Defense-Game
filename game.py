import pygame
import os
import pickle
from enemies import Enemy, RangedCreep, MeleeCreep, Roshan
from towers import Tower, ArcherTower, EagleTower, CannonTower
import logging
from time import time
import random

class Game:
    def __init__(self):
        self.log_level = logging.DEBUG
        logging.basicConfig()
        self.logger = logging.getLogger('Game')
        self.logger.setLevel(self.log_level)
        self.width = 900
        self.height = 600
        self.win = pygame.display.set_mode(((self.width,self.height)))
        # comment this for develop
        self.enemies = [RangedCreep(self.log_level)]
        self.last_spawn_enemy_time = time()
        # x width, y height
        self.towers = [ArcherTower(x=100,y=100),EagleTower(x=200,y=200), CannonTower(x=500,y=400)]
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("assets","bg.png"))
        self.bg = pygame.transform.scale(self.bg,(self.width,self.height))

    def _activate_mouse_click_action(self,position):
        """
        Check where the mouse clicked, for tower then the attack range will be displayed
        Args:
            position: [x,y]

        Returns:

        """
        # self.logger.debug('Pressed bottom is %s'%position)
        for tower in self.towers:
            if tower.click(position[0],position[1]):
                tower.draw_range = not tower.draw_range
                break
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
            clock.tick(100)
            self._spawn_enemy(5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                # if any mouse button is pressed
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # if the left button is pressed
                    if event.button == 1:
                        self._activate_mouse_click_action(event.pos)
            to_del = []
            for enemy in self.enemies:
                # works only for moving from left to right
                if enemy.reach_final or enemy.health < 0:
                    to_del.append(enemy)
            for d in to_del:
                self.enemies.remove(d)

            for tw in self.towers:
                tw.attack(self.enemies)
            self.draw()
        pygame.quit()

    def draw(self):
        self.win.blit(self.bg,(0,0))
        # draw enemies
        for enemy in self.enemies:
            enemy.draw(self.win)

        # draw towers
        for tower in self.towers:
            tower.draw(self.win)
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