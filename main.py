import pygame
import math
import random
from pygame import mixer

# setting
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("space invader")
clock = pygame.time.Clock()

backgroundImg = pygame.image.load(
    'assets/space_4_3.jpg')
bossImg = pygame.image.load(
    'assets/boss.png')
enemyImg = pygame.image.load(
    'assets/enemy.png')
bulletImg = pygame.image.load(
    'assets/bullet.png')
playerImg = pygame.image.load(
    'assets/player.png')
mixer.music.load(
    'assets/background.wav')
mixer.music.play(-1)
explosionSound = mixer.Sound(
    'assets/explosion.wav')
fireSound = mixer.Sound(
    'assets/laser.wav')

bnum = 8
run = True
speed = 4
FPS = 60
# function

def hit(x1, y1, x2, y2):
    dis = math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    if dis <= 40:
        return True
    else:
        return False


def waring(x1, y1, x2, y2):
    dis = math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
    if dis <= 100:
        return True
    else:
        return False


class Player:
    def __init__(self, input):
        self.X = 370
        self.Y = 480
        self.speed = input
        self.X_change = 0
        self.Y_change = 0

    def update(self):
        self.X += self.X_change
        self.Y += self.Y_change
        if self.X >= 700:
            self.X -= self.X_change
        if self.X <= 40:
            self.X -= self.X_change
        if self.Y >= 520:
            self.Y -= self.Y_change
        if self.Y <= 440:
            self.Y -= self.Y_change
        screen.blit(playerImg, (self.X, self.Y))

    def moveleft(self):
        self.X_change = -self.speed

    def moveright(self):
        self.X_change = self.speed

    def moveup(self):
        self.Y_change = -self.speed

    def movedown(self):
        self.Y_change = self.speed

    def xstop(self):
        self.X_change = 0

    def ystop(self):
        self.Y_change = 0


class Boss:
    def __init__(self, x, y, input):
        self.X = x
        self.Y = y
        self.X_change = input
        self.Y_change = input
        self.blood = 50

    def update(self):
        bloodtext = Text(20, 60, "Boss Blood : " + str(self.blood), 20)
        bloodtext.show()
        if self.blood > 0:
            self.X += self.X_change
            self.Y += self.Y_change
            if (self.X >= 700) or (self.X <= 40):
                self.X_change = - self.X_change
            if (self.Y <= 40) or (self.Y >= 200):
                self.Y_change = - self.Y_change
            screen.blit(bossImg, (self.X, self.Y))
        else:
            self.X = -20
            self.Y = -20
            over_text = Text(215, 250, "Game Over", 64)
            over_text.show()
            hint_text = Text(270, 360, "press \"1\" continue", 32)
            hint_text.show()
            mixer.music.stop()

    def restart(self):
        self.X = 370
        self.Y = 100
        self.blood = 50


class Enemy:
    def __init__(self, input):
        self.X = random.randint(40, 700)
        self.Y = random.randint(40, 200)
        self.X_change = input
        self.Y_change = input/2
        self.blood = 5

    def update(self):
        if self.blood > 0 and boss.blood > 0:
            self.X += self.X_change
            self.Y += self.Y_change
            if (self.X >= 700) or (self.X <= 40):
                self.X_change = -self.X_change
            if (self.Y <= 40) or (self.Y >= 200):
                self.Y_change = -self.Y_change
            screen.blit(enemyImg, (self.X, self.Y))
        else:
            self.X = -20
            self.Y = -20

    def restart(self):
        self.X = random.randint(40, 700)
        self.Y = random.randint(40, 200)
        self.blood = 5


class EList:
    def __init__(self, num, input):
        self.enemy = []
        self.num = num
        self.state = "alive"
        for i in range(self.num):
            self.enemy.append(Enemy(input))

    def restart(self):
        for i in range(self.num):
            self.enemy[i].restart()

    def die(self):
        self.state = "die"
        for i in range(self.num):
            if self.enemy[i].blood > 0:
                self.state = "alive"

    def update(self):
        self.die()
        for i in range(self.num):
            self.enemy[i].update()


class Bullet:
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.Y_change = speed*3
        self.state = "ready"

    def bullet(self, x, y):
        screen.blit(bulletImg, (x, y))


class Clip:
    def __init__(self, n, type):
        self.clip = []
        self.num = n
        self.remain = n
        self.type = type
        for i in range(n):
            self.clip.append(Bullet())

    def fire(self):

        for i in range(self.num):
            if self.clip[i].state == "ready":
                if self.type == "R":
                    self.clip[i].X = player.X + 15
                else:
                    self.clip[i].X = player.X - 15
                self.clip[i].Y = player.Y - 30
                self.clip[i].state = "fire"
                self.remain -= 1
                fireSound.play()
                break

    def position(self):
        for i in range(self.num):
            if self.clip[i].state == "fire":
                self.clip[i].Y -= self.clip[i].Y_change

    def reload(self):
        for i in range(self.num):
            if self.clip[i].Y <= 0:
                self.clip[i].state = "ready"
        self.remain = self.num

    def hitboss(self):
        for i in range(self.num):
            if hit(boss.X, boss.Y, self.clip[i].X, self.clip[i].Y) and enemy.state == "die":
                explosionSound.play()
                self.clip[i].X = -100
                self.clip[i].Y = -100
                boss.blood -= 10

    def warningboss(self):
        for i in range(self.num):
            if waring(boss.X, boss.Y, self.clip[i].X, self.clip[i].Y) and enemy.state == "die":
                boss.X = random.randint(40, 700)
                boss.Y = random.randint(40, 200)

    def hitenemy(self):
        for i in range(self.num):
            for j in range(enemy.num):
                if hit(enemy.enemy[j].X, enemy.enemy[j].Y, self.clip[i].X, self.clip[i].Y):
                    explosionSound.play()
                    self.clip[i].X = -100
                    self.clip[i].Y = -100
                    enemy.enemy[j].blood -= 10

    def update(self):
        self.position()
        self.hitenemy()
        self.hitboss()
        # self.warningboss()
        text = Text(20, 20, "子彈剩餘 : " + str(self.remain), 20)
        text.show()
        for i in range(self.num):
            if self.clip[i].state == "fire":
                self.clip[i].bullet(self.clip[i].X, self.clip[i].Y)

    def restart(self):
        self.remain = self.num
        for i in range(self.num):
            self.clip[i].state = "ready"


class Text:
    def __init__(self, x, y, input, large):
        self.X = x
        self.Y = y
        self.font = pygame.font.Font('C:\\Windows\\Fonts\\msjhbd.ttc', large)
        self.string = self.font.render(input, True, (255, 255, 255))

    def show(self):
        global screen
        screen.blit(self.string, (self.X, self.Y))


player = Player(speed)
boss = Boss(370, 100, speed/2)
enemy = EList(3, speed/2)
c1 = Clip(bnum, "R")
c2 = Clip(bnum, "L")
# Game Loop
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moveleft()
            if event.key == pygame.K_RIGHT:
                player.moveright()
            if event.key == pygame.K_UP:
                player.moveup()
            if event.key == pygame.K_DOWN:
                player.movedown()
            if event.key == pygame.K_SPACE:
                c1.fire()
                # c2.fire()
            if event.key == pygame.K_r:
                c1.reload()
                # c2.reload()
            if event.key == pygame.K_1 and boss.blood <= 0:
                boss.restart()
                c1.restart()
                # c2.restart()
                enemy.restart()
                mixer.music.play(-1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.xstop()
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.ystop()
    end_time = clock.get_time()
    screen.fill((0, 100, 255))
    screen.blit(backgroundImg, (0, 0))
    boss.update()
    enemy.update()
    player.update()
    c1.update()
    # c2.update()
    pygame.display.update()
