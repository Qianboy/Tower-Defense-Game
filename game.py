import pygame
import os
import pickle
from enemies import Enemy, RangedCreep, MeleeCreep, Roshan
import logging

class Game:
    def __init__(self):
        log_level = logging.DEBUG
        logging.basicConfig()
        self.logger = logging.getLogger('Game')
        self.logger.setLevel(log_level)
        self.width = 900
        self.height = 600
        self.win = pygame.display.set_mode(((self.width,self.height)))
        # comment this for develop
        self.enemies = [MeleeCreep(log_level=log_level),
                        RangedCreep(log_level=log_level),
                        Roshan(log_level=log_level)]
        self.towers = []
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("assets","bg.png"))
        self.bg = pygame.transform.scale(self.bg,(self.width,self.height))

    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(100)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            to_del = []
            for enemy in self.enemies:
                # works only for moving from left to right
                if enemy.reach_final:
                    to_del.append(enemy)
            for d in to_del:
                self.enemies.remove(d)

            self.draw()
        pygame.quit()

    def draw(self):
        self.win.blit(self.bg,(0,0))
        # draw enemies
        for enemy in self.enemies:
            enemy.draw(self.win)
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