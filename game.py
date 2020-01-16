import pygame
import os
import start
from random import choice
pygame.init()
fps = 60
size = 1200, 620
screen = pygame.display.set_mode(size)
running = True
clock = pygame.time.Clock()
all_units = pygame.sprite.Group()

damage = 20
lines = [0, 104, 208, 312, 416, 520]


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class hp:
    def __init__(self, max_hp_sh, speed_sh, wall):
        self.max_hp_shita = max_hp_sh
        self.hp_shita = max_hp_sh
        self.speed_update = speed_sh
        self.hp_wall = wall
        self.break_shit = False

    def damage(self, kol):
        if self.hp_shita > 0:
            self.hp_shita -= kol
            if self.hp_shita <= 0:
                self.hp_shita = 0
                self.break_shit = True
        else:
            self.hp_wall -= kol
            if self.hp_wall <= 0:
                print('end game')

    def voss_shita(self):
        if self.break_shit:
            self.hp_shita = -50
            self.break_shit = False
        self.hp_shita += self.speed_update / 60
        if self.hp_shita >= self.max_hp_shita:
            self.hp_shita = self.max_hp_shita


base = hp(200, 5, 400)


class tank(pygame.sprite.Sprite):
    image = load_image("tank.png")
    image_boom = load_image("tank_boom.png")

    def __init__(self, hp, damage, group, line):
        super().__init__(group)
        self.hp = hp
        self.damage = damage
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = lines[line]

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.hp -= damage
            if self.hp <= 0:
                self.image = self.image_boom
                self.speed = -3000
        self.rect.x -= self.speed / 60
        if self.rect.x > 1200:
            self.speed = 0


for i in range(5):
    tank(20, 30, all_units, i)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            all_units.update(event)
    screen.fill(pygame.Color('black'))
    all_units.draw(screen)
    all_units.update()
    clock.tick(fps)
    pygame.display.flip()
