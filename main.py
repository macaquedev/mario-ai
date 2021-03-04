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
BG_IMAGE = pygame.image.load('bg_img.jpg')
MARIO = pygame.image.load('mario_still.png')
MARIO_RUN_0 = pygame.image.load('mario_run_0.png')
MARIO_RUN_1 = pygame.image.load('mario_run_1.png')
MARIO_RUN_2 = pygame.image.load('mario_run_2.png')
MARIO_JUMP = pygame.image.load('mario_jump.png')
LEVELS = {}

with open("levels.json") as f:
    LEVELS = json.load(f)

MUSHROOM = pygame.image.load('mushroom.png')

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
    def __init__(self):
        pass  # put your json stuff here

    def __init__(self, num):
        self.x = LEVELS[str(num)]["mushrooms"]["x"]
        self.y = LEVELS[str(num)]["mushrooms"]["y"]
        self.movement_width = LEVELS[str(num)]["mushrooms"]["movement_width"]


mario = Mario()


def draw_window(sc):
    sc.blit(BG_IMAGE, (bgX, 0))
    sc.blit(BG_IMAGE, (bgX2, 0))
    mario.draw()


while True:
    sc.fill((0, 0, 0))
    clock.tick(FPS)
    draw_window(sc)
    mario.move()
    if mario.x > 1920 / 2 - 75:
        bgX -= SCROLL_SPEED
        bgX2 -= SCROLL_SPEED
        mario.x = 1920 / 2 - 75
    if bgX < BG_IMAGE.get_width() * -1:
        bgX = BG_IMAGE.get_width() - 10
    if bgX2 < BG_IMAGE.get_width() * -1:
        bgX2 = BG_IMAGE.get_width() - 10

    pygame.display.update()
