import pygame as pg
import random
import math

pg.init()

screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Battle in outer Space")
icon = pg.image.load("images/icon.png")
bg = pg.image.load("images/background.jpg")
pg.display.set_icon(icon)

# player
player = pg.image.load("images/spaceship.png")
player_x = 380
player_y = 520
direction = 0.0

# score
score = 0
font = pg.font.Font('freesansbold.ttf', 32)
go_font = pg.font.Font('freesansbold.ttf', 64)

score_x = 10
score_y = 10


def display_score(x, y):
    s = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(s, (x, y))


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
    screen.blit(bullet, (x + 14, y + 10))


def touch(bx, by, ex, ey):
    dist = math.sqrt(math.pow(bx - ex, 2) + math.pow(by - ey, 2))
    if dist < 28:
        return True
    return False


def game_over():
    s = go_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(s, (230, 220))


# enemy
total = 5
enemy = []
enemy_x = []
enemy_y = []
ex_dir = []
ey_dir = []
for i in range(total):
    enemy.append(pg.image.load("images/enemy.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(64, 150))
    ex_dir.append(0.4)
    ey_dir.append(0.0)


def enemy_fn(x, y, i):
    screen.blit(enemy[i], (x, y))


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
                direction = -0.5
            if event.key == pg.K_RIGHT:
                direction = 0.5
            if event.key == pg.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    attack(bullet_x, bullet_y)
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                direction = 0.0
    # player
    player_x += direction
    if player_x <= 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736

    # enemy
    for i in range(total):
        if enemy_y[i] > 400:
            for j in range(total):
                enemy_y[j] = 1000
            game_over()
            break

        enemy_x[i] += ex_dir[i]
        if enemy_x[i] <= 0:
            ex_dir[i] *= -1
            enemy_x[i] = 0
            enemy_y[i] += 30
        if enemy_x[i] >= 736:
            ex_dir[i] *= -1
            enemy_x[i] = 736
            enemy_y[i] += 30
        # checking whether the bullet had hit the target
        hit = touch(bullet_x, bullet_y, enemy_x[i], enemy_y[i])
        if hit:
            bullet_y = 520
            bullet_state = "ready"
            score += 1
            print(score)
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(64, 150)
        enemy_fn(enemy_x[i], enemy_y[i], i)

    # If attack
    if bullet_y <= 0:
        bullet_y = 520
        bullet_state = "ready"

    if bullet_state == "fire":
        attack(bullet_x, bullet_y)
        bullet_y -= b_move

    player_fn(player_x, player_y)
    display_score(score_x, score_y)
    pg.display.update()