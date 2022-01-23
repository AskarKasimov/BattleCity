import time
import pygame
import sys
import os
import threading
import random

from enemy_tank import EnemyTank
from board import Board
from create_level import tile_width, tile_height, tile_images
from tank import Tank
from button import Button

clock = pygame.time.Clock()
FPS = 50


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Shot(pygame.sprite.Sprite):
    image = load_image("shot.png")

    def __init__(self, pos):
        super().__init__(shots)
        self.pos = pos
        self.image = Shot.image
        self.vx = 0
        self.vy = 0
        if self.pos == "up":
            self.rect = pygame.Rect(tank.rect.x + 10, tank.rect.y - 10, self.image.get_width(), self.image.get_height())
            Shot.image = pygame.transform.rotate(load_image("shot.png"), 90)
            self.vy = -3
        if self.pos == "down":
            self.rect = pygame.Rect(tank.rect.x + 10, tank.rect.y + 30, self.image.get_width(), self.image.get_height())
            Shot.image = pygame.transform.rotate(load_image("shot.png"), -90)
            self.vy = 3
        if self.pos == "left":
            self.rect = pygame.Rect(tank.rect.x - 10, tank.rect.y + 10, self.image.get_width(), self.image.get_height())
            Shot.image = pygame.transform.rotate(load_image("shot.png"), 180)
            self.vx = -3
        if self.pos == "right":
            self.rect = pygame.Rect(tank.rect.x + 30, tank.rect.y + 10, self.image.get_width(), self.image.get_height())
            Shot.image = pygame.transform.rotate(load_image("shot.png"), 0)
            self.vx = 3

    def update(self):
        if pygame.sprite.spritecollide(self, pygame.sprite.Group(list(filter(lambda x: board.board[x.rect[0] // tile_width][x.rect[1] // tile_height] == list(tile_images.keys()).index("Разрушаемая коробка") + 1, all_sprites))), True):
            self.kill()
        if pygame.sprite.spritecollide(self, pygame.sprite.Group(list(filter(lambda x: board.board[x.rect[0] // tile_width][x.rect[1] // tile_height] == list(tile_images.keys()).index("Кирпичная стена") + 1, all_sprites))), False):
            self.kill()
        if self.pos == "up":
            self.rect.y -= 2
        if self.pos == "down":
            self.rect.y += 2
        if self.pos == "left":
            self.rect.x -= 2
        if self.pos == "right":
            self.rect.x += 2
        if self.rect.x < -25 or self.rect.x > width + 25 or self.rect.y < -25 or self.rect.y > height + 25:
            self.kill()


def shoot(shots1, pos1, tank_shoots):
    if pos1 == "up" and not tank_shoots.is_collide_up or \
            pos1 == "down" and not tank_shoots.is_collide_down or \
            pos1 == "left" and not tank_shoots.is_collide_left \
            or pos1 == "right" and not tank_shoots.is_collide_right:
        shot = Shot(pos1)
        shots1.add(shot)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    button_start = Button(screen, 325, 500, "Играть")
    fon = pygame.transform.scale(load_image('start_screen.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 7)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == MYEVENTTYPE and button_start.is_checked():
                return
            button_start.update(event)
        button_start.render()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':

    pygame.init()
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)

    start_screen()

    all_sprites = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    tanks = pygame.sprite.Group()
    running = True

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 10)

    start = time.time()

    board = Board(14, 14, all_sprites, tile_width, tile_height, tile_images, screen, pattern="2.txt")
    board.render()

    tank = None
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if board.board[i][j] == list(tile_images.keys()).index("Точка спавна") + 1:
                tank = Tank(i * tile_width, j * tile_height, board, all_sprites, tanks)
                board.board[i][j] = 0
                board.render()

    tank = Tank((width - load_image("tankkk.png").get_width()) / 2, (height - load_image("tankkk.png").get_height()) / 2, board, all_sprites, tanks)\
        if not tank else tank
    tanks.add(tank)

    bot_tank = EnemyTank(100, 100, board, all_sprites, tanks)
    tanks.add(bot_tank)
    while running:
        all_sprites.remove(tank)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        tanks.draw(screen)
        shots.draw(screen)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_LEFT] and not tank.is_collide_left and not(keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                tank.pos = "left"
                tank.rect.x -= 1
                tank.image = pygame.transform.rotate(load_image("tankkk.png"), 90)
            if keys[pygame.K_RIGHT] and not tank.is_collide_right and not(keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                tank.pos = "right"
                tank.rect.x += 1
                tank.image = pygame.transform.rotate(load_image("tankkk.png"), -90)
            if keys[pygame.K_UP] and not tank.is_collide_up and not(keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN]):
                tank.pos = "up"
                tank.rect.y -= 1
                tank.image = pygame.transform.rotate(load_image("tankkk.png"), 0)
            if keys[pygame.K_DOWN] and not tank.is_collide_down and not(keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_LEFT]):
                tank.pos = "down"
                tank.rect.y += 1
                tank.image = pygame.transform.rotate(load_image("tankkk.png"), 180)
            if time.time() - start > 1 and keys[pygame.K_SPACE]:
                threading.Thread(target=shoot, args=(shots, tank.pos, tank)).start()
                start = time.time()
            if event.type == MYEVENTTYPE:
                for x in shots:
                    x.update()
            tank.update()
            bot_tank.update()
        pygame.display.flip()
    pygame.quit()
