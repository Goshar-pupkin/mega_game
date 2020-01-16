import pygame
import os
import sys
pygame.init()
fps = 60
size = 1200, 620
screen = pygame.display.set_mode(size)
running = True


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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global running

    button_start = Button((0, 0, 0), 475, 225, 250, 100, (0, 0, 0), text="START GAME")

    pygame.mixer.music.load(os.path.join('data', 'fon.mp3'))
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.05)

    fon = pygame.transform.scale(load_image('fon.jpg'), (size))

    screen.blit(fon, (0, 0))

    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.isOver(pos):
                    running = False

            if event.type == pygame.MOUSEMOTION:
                if button_start.isOver(pos):
                    button_start.colour = (71, 74, 81)
                    button_start.text_colour = (71, 74, 81)
                else:
                    button_start.colour = (0, 0, 0)
                    button_start.text_colour = (0, 0, 0)
        clock.tick(fps)
        pygame.display.flip()
        button_start.draw(screen, outline=10)


class Button:
    def __init__(self, colour, x, y, width, height, text_colour, text=""):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_colour = text_colour

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height), 5)

        else:
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont("comicsans", 40)
            text = font.render(self.text, 1, (self.text_colour))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

