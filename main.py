import pygame
import numpy
import pickle
from pygame.time import Clock

clock = Clock()

SPEED = 10
ANIMATION_SPEED = 5

pygame.init()
sc = pygame.display.set_mode((1920, 1080))

BG_IMAGE = pygame.image.load('bg_img.jpg')
MARIO = pygame.image.load('mario_still.png')
MARIO_RUN_0 = pygame.image.load('mario_run_0.png')
MARIO_RUN_1 = pygame.image.load('mario_run_1.png')
MARIO_RUN_2 = pygame.image.load('mario_run_2.png')
MARIO_JUMP = pygame.image.load('mario_jump.png')


class Mario:
    def __init__(self):
        self.img = MARIO
        self.x = 40
        self.y = 860
        self.animation_count = 0
        self.speed = SPEED
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
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
            self.animate()
        if keys[pygame.K_w]:
            self.img = MARIO_JUMP
            self.in_air = True
            if oy - self.y < 300 and self.can_jump:
                self.y -= SPEED
                self.speed = SPEED * 0.3
            else:
                self.can_jump = False
        if self.y > 850 or self.block_under:
            self.in_air = False
            self.speed = SPEED
            self.can_jump = True
        if not self.block_under and self.y < 860:
            self.y += SPEED / 2
        if self.y < 0:
            self.y += SPEED
            self.jump = False
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


mario = Mario()


def draw_window(sc):
    sc.blit(BG_IMAGE, (0, 0))
    mario.draw()


while True:
    sc.fill((0, 0, 0))
    clock.tick(30)
    draw_window(sc)
    mario.move()
    pygame.display.update()
