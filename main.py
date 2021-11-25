import pygame as pg
import random

pg.init()

screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Battle in outer Space")
icon = pg.image.load("images/icon.png")
bg = pg.image.load("images/background.jpg")
pg.display.set_icon(icon)

# player
player = pg.image.load("images/spaceship.png")
px = 380
py = 520
dir = 0.0


def player_fn(x, y):
    screen.blit(player, (x, y))


# bullet
bullet = pg.image.load("images/bullet.png")
bullet_x = 0
bullet_y = 520
b_move = 1
bullet_state = "ready"


def attack(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


# enemy
enemy = pg.image.load("images/enemy.png")
epx = random.randint(0, 736)
epy = random.randint(64, 150)
exdir = 0.3
eydir = 0.0


def enemy_fn(x, y):
    screen.blit(enemy, (x, y))


# Game
run = True
while run:
    screen.fill((0, 0, 0))
    # background image
    screen.blit(bg, (0, 0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                dir = -0.5
            if event.key == pg.K_RIGHT:
                dir = 0.5
            if event.key == pg.K_SPACE:
                attack(px, bullet_y)
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                dir = 0.0
    # player
    px += dir
    if px <= 0:
        px = 0
    if px >= 736:
        px = 736

    # enemy
    epx += exdir
    if epx <= 0:
        exdir *= -1
        epx = 0
        epy += 30
    if epx >= 736:
        exdir *= -1
        epx = 736
        epy += 30

    # If attack
    if bullet_state == "fire":
        attack(px, bullet_y)
        bullet_y -= b_move

    player_fn(px, py)
    enemy_fn(epx, epy)
    pg.display.update()
