import pygame
import numpy
import pickle
from pygame.time import Clock
import json

# to-do:
# make mario slow down when jumping at the point where everything starts scrolling
# create platforms
# create enemies

pygame.init()
sc = pygame.display.set_mode((1920, 1080))

clock = Clock()
RUN_SPEED = 10
JUMP_SPEED = 20
SCROLL_SPEED = RUN_SPEED
ANIMATION_SPEED = 5
FPS = 30
BG_IMAGE = pygame.image.load('imgs/bg_img.jpg')
MARIO = pygame.image.load('imgs/mario_still.png')
MARIO_RUN_0 = pygame.image.load('imgs/mario_run_0.png')
MARIO_RUN_1 = pygame.image.load('imgs/mario_run_1.png')
MARIO_RUN_2 = pygame.image.load('imgs/mario_run_2.png')
MARIO_JUMP = pygame.image.load('imgs/mario_jump.png')
GOOMBA_0 = pygame.image.load('imgs/mushroom_0.png')
GOOMBA_1 = pygame.image.load('imgs/mushroom_1.png')
GOOMBA_DEAD = pygame.image.load('imgs/mushroom_dead.png')

LEVELS = {}

with open("levels.json") as f:
    LEVELS = json.load(f)

bgX = 0
bgX2 = BG_IMAGE.get_width()


class Mario:
    def __init__(self):
        self.img = MARIO
        self.x = 40
        self.y = 860
        self.animation_count = 0
        self.run_speed = RUN_SPEED
        self.jump_speed = JUMP_SPEED
        self.foo = 1
        self.bar = 1
        self.animation_speed = ANIMATION_SPEED
        self.in_air = False
        self.block_under = False
        self.can_jump = True

    def draw(self):
        sc.blit(self.img, (self.x, self.y))

    def move(self):
        oy = 860
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.run_speed
        if keys[pygame.K_d]:
            self.x += self.run_speed
            self.animate()
        if keys[pygame.K_w]:
            self.img = MARIO_JUMP
            self.in_air = True
            if oy - self.y < 300 and self.can_jump:
                self.y -= JUMP_SPEED
                self.run_speed = RUN_SPEED * 0.3
            else:
                self.can_jump = False
        if self.y > 850 or self.block_under:
            self.in_air = False
            self.run_speed = RUN_SPEED
            self.can_jump = True
        if not self.block_under and self.y < 860:
            self.y += JUMP_SPEED / 2
        if self.y < 0:
            self.y += JUMP_SPEED
            self.jump = False
        if self.x < 0:
            self.x = 0
        if keys[pygame.K_ESCAPE]:
            exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def animate(self):
        if not self.in_air:
            if self.animation_count == 2:
                self.foo = -1
            elif self.animation_count == 0:
                self.foo = 1
            if self.animation_count == 0:
                self.img = MARIO_RUN_0
            elif self.animation_count == 1:
                self.img = MARIO_RUN_1
            elif self.animation_count == 2:
                self.img = MARIO_RUN_2
            self.bar += 1
            if self.bar % self.animation_speed == 0:
                self.animation_count += self.foo


class Block:
    def __init__(self):
        pass


class Mushroom:
    def __init__(self, level, num):
        self.x = LEVELS[str(1)]["mushrooms"][num]["x"]
        self.y = LEVELS[str(1)]["mushrooms"][num]["y"]
        self.img = GOOMBA_0
        self.foo = 1
        self.bar = 1
        self.eggs = 1
        self.dead = False
        self.animation_count = 0
        self.animation_speed = ANIMATION_SPEED

    def draw(self):
        sc.blit(self.img, (self.x, self.y))

    def move(self):
        self.x -= 6
        self.animate()

    def animate(self):
        if self.animation_count == 1:
            self.foo = -1
        elif self.animation_count == 0:
            self.foo = 1
        if self.animation_count == 0:
            self.img = GOOMBA_0
        elif self.animation_count == 1:
            self.img = GOOMBA_1
        self.bar += 1
        if self.bar % self.animation_speed == 0:
            self.animation_count += self.foo

    def check_dead(self):
        if self.dead:
            self.y = 920
            self.img = GOOMBA_DEAD
            self.eggs += 1
            if self.eggs > 10:
                self.y = 2000


def collision(mario, mushroom):
    if abs(mario.x - mushroom.x) < 10 and mario.y > 800:
        if mario.y + mario.img.get_height() - 40 < mushroom.y:
            mushroom.dead = True
        else:
            mario.x = 40


mario = Mario()
mushroom0 = Mushroom(1, 1)
mushroom1 = Mushroom(1, 0)


def draw_window(sc):
    sc.blit(BG_IMAGE, (bgX, 0))
    sc.blit(BG_IMAGE, (bgX2, 0))
    mushroom1.draw()
    mushroom0.draw()
    mario.draw()


while True:
    sc.fill((0, 0, 0))
    clock.tick(FPS)
    draw_window(sc)
    mario.move()
    mushroom0.move()
    mushroom1.move()
    mushroom0.check_dead()
    mushroom1.check_dead()
    collision(mario, mushroom0)
    collision(mario, mushroom1)
    if mario.x > 1920 / 2 - 75:
        bgX -= SCROLL_SPEED
        bgX2 -= SCROLL_SPEED
        mario.x = 1920 / 2 - 75
    if bgX < BG_IMAGE.get_width() * -1:
        bgX = BG_IMAGE.get_width() - 10
    if bgX2 < BG_IMAGE.get_width() * -1:
        bgX2 = BG_IMAGE.get_width() - 10

    pygame.display.update()
