import pygame
import os
from random import choice
from start import start_screen

start_screen()

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
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


pygame.init()
pygame.mixer.init()

snd_dir = os.path.join(os.path.dirname(__file__), 'data')
shot_sound = pygame.mixer.Sound(os.path.join('data', 'Shot.wav'))
reload_sound = pygame.mixer.Sound(os.path.join('data', 'reload.wav'))

tank_shot = pygame.mixer.Sound(os.path.join('data', 'tank_shot.wav'))
fps = 60
size = 1200, 620
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

all_units = pygame.sprite.Group()
weapon = pygame.sprite.Group()
bullets = pygame.sprite.Group()

damage = 20
lines = [0, 104, 208, 312, 416, 520]
shot = True


class hp:
    def __init__(self, max_hp_sh, speed_sh, wall):
        self.max_hp_shita = max_hp_sh
        self.hp_shita = max_hp_sh
        self.speed_update = speed_sh
        self.hp_wall = wall
        self.break_shit = False

    def damage(self, kol):
        global running
        if self.hp_shita > 0:
            self.hp_shita -= kol
            if self.hp_shita <= 0:
                self.hp_shita = 0
                self.break_shit = True
        else:
            self.hp_wall -= kol
            if self.hp_wall <= 0:
                print('end game')
                running = False
                start_screen()

    def voss_shita(self):
        if self.break_shit:
            self.hp_shita = -50
            self.break_shit = False
        self.hp_shita += self.speed_update / 60
        if self.hp_shita >= self.max_hp_shita:
            self.hp_shita = self.max_hp_shita


base = hp(200, 5, 400)

class bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bullet.png'), (75, 100))

    def __init__(self, y, group):
        super().__init__(group)

        self.rect = self.image.get_rect()
        self.rect.y = y - 40
        self.speed = 20
        self.rect.x = 420

    def update(self):
        self.rect.x += self.speed

class gun(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('gun.png'), (200, 100))

    def __init__(self, damage, y, group):
        super().__init__(group)

        self.damage = damage
        self.rect = self.image.get_rect()
        self.rect.y = y - 40
        self.rect.x = 250

    def update(self, y):
        self.rect.y = y - 40

class tank(pygame.sprite.Sprite):
    image = load_image("tank.png")
    image_boom = load_image("tank_boom.png")
    image_stop = load_image("tank-stop.png")

    def __init__(self, hp, damage, group, line):
        super().__init__(group)
        self.hp = hp
        self.damage = damage
        self.speed = 15
        self.reloadspeed = fps * 5
        self.rect = self.image.get_rect()
        self.rect.x = 1200
        self.rect.y = lines[line]
        self.attak = False
        self.schet = 0

    def update(self, *args):
        global shot
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            if shot:
                self.hp -= damage
                shot_sound.play()
                shot = False
            else:
                reload_sound.play()
                shot = True
            if self.hp <= 0:
                self.image = self.image_boom
                self.speed = -3000
                self.attak = False
        self.rect.x -= self.speed / 60
        if self.rect.x < 400:
            self.image = self.image_stop
            self.rect.x = 400
            self.speed = 0
            self.attak = True
        if self.attak:
            if self.schet % self.reloadspeed == 0:
                tank_shot.play()
                base.damage(self.damage)
            self.schet += choice([1, 0, 2])
        if self.rect.x > 1200:
            self.speed = 0


running = True

gun(100, pygame.mouse.get_pos()[1], weapon)
for i in range(5):
    tank(20, 30, all_units, i)
fon = pygame.transform.scale(load_image('fon_1.jpg'), (950, 633))
base_image = pygame.transform.scale(load_image('base.jpg'), (232, 620))
screen.blit(base_image, (0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            weapon.update(pygame.mouse.get_pos()[1])

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet(pygame.mouse.get_pos()[1], bullets)
            all_units.update(event)
    screen.blit(fon, (232, 0))
    weapon.draw(screen)
    bullets.draw(screen)
    bullets.update()
    all_units.draw(screen)
    all_units.update()
    clock.tick(fps)
    pygame.display.flip()
