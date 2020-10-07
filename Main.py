import pygame
import neat
import time
import os
import random

pygame.font.init()
WIN_WIDTH = 500
WIN_HEIGHT = 800

SPRITE_BIRDS = [pygame.transform.scale2x(pygame.image.load(r"C:\Users\david\Desktop\Python\AI Flappy Bird\imgs\bird1.png")),
                pygame.transform.scale2x(pygame.image.load(r"C:\Users\david\Desktop\Python\AI Flappy Bird\imgs\bird2.png")),
                pygame.transform.scale2x(pygame.image.load(r"C:\Users\david\Desktop\Python\AI Flappy Bird\imgs\bird3.png"))]

SPRITE_PIPE = pygame.transform.scale2x(pygame.image.load(r"C:\Users\david\Desktop\Python\AI Flappy Bird\imgs\pipe.png"))
SPRITE_BASE = pygame.transform.scale2x(pygame.image.load(r"C:\Users\david\Desktop\Python\AI Flappy Bird\imgs\base.png"))
SPRITE_BG = pygame.transform.scale2x(pygame.image.load(r"C:\Users\david\Desktop\Python\AI Flappy Bird\imgs\bg.png"))

FONT_STATS = pygame.font.SysFont("comicsans", 50)


class Bird:
    SPRITES = SPRITE_BIRDS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.SPRITES[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5 * self.tick_count ** 2 #TODO: UNDERSTAND
        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.SPRITES[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.SPRITES[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.SPRITES[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.SPRITES[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.SPRITES[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.SPRITES[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft =  (self.x, self.y)).center) #TODO: UNDERSTAND
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__ (self, x):
        self.x = x
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(SPRITE_PIPE, False, True)
        self.PIPE_BOTTOM = SPRITE_PIPE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False

class Base:
    VEL = 5
    WIDTH = SPRITE_BASE.get_width()
    SPRITE = SPRITE_BASE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.SPRITE, (self.x1, self.y))
        win.blit(self.SPRITE, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score):
    win.blit(SPRITE_BG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = FONT_STATS.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)
    pygame.display.update()

def main():
    bird1 = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(700)]
    score = 0
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird1.move()
        remove = []
        add_pipe = False
        for pipe in pipes:
            if pipe.collide(bird1):
                pass
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            if not pipe.passed and pipe.x < bird1.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(700))

        if len(remove) > 0:
            for x in remove:
                pipes.remove(x)

        base.move()
        draw_window(win,bird1,pipes,base,score)

    pygame.quit()
    quit()

main()



