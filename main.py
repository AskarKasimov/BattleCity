import time
import pygame
import sys
import os
import threading
import random

from shot import Shot
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

    board = Board(14, 14, all_sprites, tile_width, tile_height, tile_images, screen, pattern="3.txt")
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

    bot_tank = EnemyTank(100, 100, board, all_sprites, tanks, tank, shots)
    tanks.add(bot_tank)
    while running:
        all_sprites.remove(tank)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        tanks.draw(screen)
        shots.draw(screen)
        for event in pygame.event.get():
            threading.Thread(target=bot_tank.update).start()
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
                threading.Thread(target=tank.shoot, args=(shots,)).start()
                start = time.time()
            if event.type == MYEVENTTYPE:
                for x in shots:
                    x.update(all_sprites, board)
            tank.update()
        pygame.display.flip()
    pygame.quit()
