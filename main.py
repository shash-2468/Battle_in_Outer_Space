import sys

import pygame as pg
import random
import math
from pygame import mixer as mx


class BattleInOuterSpaceGame:
    def __init__(self):
        self.player_x = None
        self.player_y = None
        self.direction = None
        self.score = None
        self.score_x = None
        self.score_y = None
        self.bullet_x = None
        self.bullet_y = None
        self.b_move = None
        self.bullet_state = None
        self.total = None
        self.enemy = None
        self.enemy_x = None
        self.enemy_y = None
        self.ex_dir = None
        self.ey_dir = None
        self.run = None

        pg.init()
        mx.music.load('audio/background.wav')
        mx.music.play(-1)

        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Battle in outer Space")
        self.icon = pg.image.load("images/icon.png")
        self.bg = pg.image.load("images/background.jpg")
        pg.display.set_icon(self.icon)

        # player
        self.player = pg.image.load("images/spaceship.png")

        # score
        self.font = pg.font.Font('freesansbold.ttf', 32)
        self.go_font = pg.font.Font('freesansbold.ttf', 64)

        # bullet
        self.bullet = pg.image.load("images/bullet.png")

        self.init()

    def init(self):
        self.player_x = 380
        self.player_y = 520
        self.direction = 0.0

        self.score = 0

        self.score_x = 10
        self.score_y = 10

        self.bullet_x = 0
        self.bullet_y = 520
        self.b_move = 1
        self.bullet_state = "ready"

        # enemy
        self.total = 5
        self.enemy = []
        self.enemy_x = []
        self.enemy_y = []
        self.ex_dir = []
        self.ey_dir = []
        for i in range(self.total):
            self.enemy.append(pg.image.load("images/enemy.png"))
            self.enemy_x.append(random.randint(0, 736))
            self.enemy_y.append(random.randint(64, 150))
            self.ex_dir.append(0.4)
            self.ey_dir.append(0.0)

        self.run = True

    def display_score(self, x, y):
        s = self.font.render("Score: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(s, (x, y))

    def player_fn(self, x, y):
        self.screen.blit(self.player, (x, y))

    def enemy_fn(self, enemy, x, y):
        self.screen.blit(enemy, (x, y))

    def attack(self, x, y):
        self.bullet_state = "fire"
        self.screen.blit(self.bullet, (x + 14, y + 10))

    def game_over(self):
        s = self.go_font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(s, (230, 220))
        s = self.font.render("Press SPACE to play again", True, (255, 30, 0))
        self.screen.blit(s, (230, 280))
        self.run = False

    @staticmethod
    def touch(bx, by, ex, ey):
        dist = math.sqrt(math.pow(bx - ex, 2) + math.pow(by - ey, 2))
        if dist < 28:
            return True
        return False

    def exit(self):
        self.run = False
        sys.exit(0)

    def play(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit()

                if event.type == pg.KEYDOWN:
                    if self.run:
                        if event.key == pg.K_ESCAPE:
                            self.exit()
                        if event.key == pg.K_LEFT:
                            self.direction = -0.5
                        if event.key == pg.K_RIGHT:
                            self.direction = 0.5
                        if event.key == pg.K_SPACE:
                            if self.bullet_state == "ready":
                                self.bullet_x = self.player_x
                                bulSound = mx.Sound('audio/laser.wav')
                                bulSound.play()
                                self.attack(self.bullet_x, self.bullet_y)
                    elif event.key == pg.K_SPACE:
                        self.init()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        self.direction = 0.0

            if self.run:
                self.screen.fill((0, 0, 0))
                # background image
                self.screen.blit(self.bg, (0, 0))

                # player
                self.player_x += self.direction
                if self.player_x <= 0:
                    self.player_x = 0
                if self.player_x >= 736:
                    self.player_x = 736

                # enemy
                for i in range(self.total):
                    if self.enemy_y[i] > 400:
                        for j in range(self.total):
                            self.enemy_y[j] = 1000
                        self.game_over()
                        break

                    self.enemy_x[i] += self.ex_dir[i]
                    if self.enemy_x[i] <= 0:
                        self.ex_dir[i] *= -1
                        self.enemy_x[i] = 0
                        self.enemy_y[i] += 30
                    if self.enemy_x[i] >= 736:
                        self.ex_dir[i] *= -1
                        self.enemy_x[i] = 736
                        self.enemy_y[i] += 30
                    # checking whether the bullet had hit the target
                    hit = self.touch(self.bullet_x, self.bullet_y, self.enemy_x[i], self.enemy_y[i])
                    if hit:
                        explSound = mx.Sound('audio/explosion.wav')
                        explSound.play()
                        self.bullet_y = 520
                        self.bullet_state = "ready"
                        self.score += 1
                        print(self.score)
                        self.enemy_x[i] = random.randint(0, 736)
                        self.enemy_y[i] = random.randint(64, 150)
                    self.enemy_fn(self.enemy[i], self.enemy_x[i], self.enemy_y[i])

                # If attack
                if self.bullet_y <= 0:
                    self.bullet_y = 520
                    self.bullet_state = "ready"

                if self.bullet_state == "fire":
                    self.attack(self.bullet_x, self.bullet_y)
                    self.bullet_y -= self.b_move

                self.player_fn(self.player_x, self.player_y)
                self.display_score(self.score_x, self.score_y)
                pg.display.update()


if __name__ == "__main__":
    new_game = BattleInOuterSpaceGame()
    new_game.play()
