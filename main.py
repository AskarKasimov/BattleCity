import time
import pygame
import sys
import os
import threading
import random
import datetime as dt

from Tools.scripts.pep384_macrocheck import dprint

from enemy_tank import EnemyTank
from board import Board
from create_level import tile_width, tile_height, tile_images
from tank import Tank
from button import Button
from shot import Shot

start_time = dt.datetime.now()
clock = pygame.time.Clock()
FPS = 50
score = 0
lvl = 1
enemies = 1


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def shoot(shots1, pos1, tank_shoots):
    shot = Shot(pos1, shots1, tank_shoots)
    shots1.add(shot)


def start_screen():
    global lvl, enemies
    pygame.display.set_caption('PyTanks – Запуск')
    button_start = Button(screen, 325, 650, "Играть")
    button_left = Button(screen, 100, 350, "Предудыщий")
    button_right = Button(screen, 500, 350, "Следующий")
    button_less = Button(screen, 120, 500, "Меньше")
    button_more = Button(screen, 530, 500, "Больше")
    fon = pygame.transform.scale(load_image('start_screen.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 7)

    font = pygame.font.Font(None, 40)
    text = font.render("Уровень:", False, (143, 20, 2))
    text_x = width // 2 - text.get_width() // 2
    text_y = 300
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 40)
    text = font.render("Количество врагов:", False, (143, 20, 2))
    text_x = width // 2 - text.get_width() // 2
    text_y = 450
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 40)
    text = font.render(str(lvl), False, (143, 20, 2))
    text_x = width // 2 - text.get_width() // 2
    text_y = 350
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 40)
    text = font.render(str(enemies), False, (143, 20, 2))
    text_x = width // 2 - text.get_width() // 2
    text_y = 500
    screen.blit(text, (text_x, text_y))
    while True:
        levels = len(os.listdir(path="levels"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MYEVENTTYPE and button_start.is_checked():
                return
            if event.type == MYEVENTTYPE and button_right.is_checked():
                if lvl < levels:
                    font = pygame.font.Font(None, 40)
                    text = font.render(str(lvl), False, (0, 0, 0))
                    text_x = width // 2 - text.get_width() // 2
                    text_y = 350
                    screen.blit(text, (text_x, text_y))

                    lvl += 1

                    font = pygame.font.Font(None, 40)
                    text = font.render(str(lvl), False, (143, 20, 2))
                    text_x = width // 2 - text.get_width() // 2
                    text_y = 350
                    screen.blit(text, (text_x, text_y))
                button_right.checked = False
            if event.type == MYEVENTTYPE and button_left.is_checked():
                if lvl > 1:
                    font = pygame.font.Font(None, 40)
                    text = font.render(str(lvl), False, (0, 0, 0))
                    text_x = width // 2 - text.get_width() // 2
                    text_y = 350
                    screen.blit(text, (text_x, text_y))

                    lvl -= 1

                    font = pygame.font.Font(None, 40)
                    text = font.render(str(lvl), False, (143, 20, 2))
                    text_x = width // 2 - text.get_width() // 2
                    text_y = 350
                    screen.blit(text, (text_x, text_y))
                button_left.checked = False

            if event.type == MYEVENTTYPE and button_more.is_checked():
                if enemies < 10:
                    font = pygame.font.Font(None, 40)
                    text = font.render(str(enemies), False, (0, 0, 0))
                    text_x = width // 2 - text.get_width() // 2
                    text_y = 500
                    screen.blit(text, (text_x, text_y))

                    enemies += 1

                    font = pygame.font.Font(None, 40)
                    text = font.render(str(enemies), False, (143, 20, 2))
                    text_x = width // 2 - text.get_width() // 2
                    text_y = 500
                    screen.blit(text, (text_x, text_y))
                button_more.checked = False
            if event.type == MYEVENTTYPE and button_less.is_checked():
                if enemies > 1:
                    font = pygame.font.Font(None, 40)
                    text = font.render(str(enemies), False, (0, 0, 0))
                    text_x = width // 2 - text.get_width() // 2
                    text_y = 500
                    screen.blit(text, (text_x, text_y))

                    enemies -= 1

                    font = pygame.font.Font(None, 40)
                    text = font.render(str(enemies), False, (143, 20, 2))
                    text_x = width // 2 - text.get_width() // 2
                    text_y = 500
                    screen.blit(text, (text_x, text_y))
                button_less.checked = False

            button_start.update(event)
            button_left.update(event)
            button_right.update(event)
            button_less.update(event)
            button_more.update(event)
        button_start.render()
        button_left.render()
        button_right.render()
        button_less.render()
        button_more.render()
        pygame.display.flip()
        clock.tick(FPS)


def the_end():
    pygame.display.set_caption('PyTanks – Проигрыш')
    button_start = Button(screen, 310, 650, "Закрыть")
    fon = pygame.transform.scale(load_image('game_over.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 7)

    font = pygame.font.Font(None, 50)
    text = font.render("Счёт: " + str(tank.score), False, (143, 20, 2))
    text_x = width // 2 - text.get_width() // 2
    text_y = 500
    screen.blit(text, (text_x, text_y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MYEVENTTYPE and button_start.is_checked():
                pygame.quit()
                sys.exit()
            button_start.update(event)
        button_start.render()
        pygame.display.flip()
        clock.tick(FPS)


def update_records():
    finish_time = dt.datetime.now()
    delta = finish_time - start_time
    records_read = open("records.txt", "r", encoding="UTF-8").readlines()
    record_point = max(tank.score, int(records_read[0].split()[3]))
    delta = round(delta.seconds + delta.microseconds * 10**-6, 2)
    record_time = min(delta, float(records_read[1].split()[3]))

    records_write = open("records.txt", "w", encoding="UTF-8")
    records_write.write("Текущий рекорд очков: " + str(record_point) + "\n" + "Текущий рекорд времени: " + str(record_time) + " сек.")



def the_win():
    pygame.display.set_caption('PyTanks – Победа')
    button_start = Button(screen, 310, 650, "Закрыть")
    fon = pygame.transform.scale(load_image('start_screen.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 7)

    font = pygame.font.Font(None, 50)
    update_records()
    text = font.render("Счёт: " + str(tank.score), False, (143, 20, 2))
    text_x = width // 2 - text.get_width() // 2
    text_y = 400
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 50)
    text = font.render("Вы выиграли!", False, (143, 20, 2))
    records_read = open("records.txt", "r", encoding="UTF-8").readlines()
    records1 = font.render(records_read[0].strip(), False, (143, 20, 2))
    records2 = font.render(records_read[1].strip(), False, (143, 20, 2))
    text_x = width // 2 - text.get_width() // 2
    text_y = 350
    screen.blit(text, (text_x, text_y))
    screen.blit(records1, (50, 500))
    screen.blit(records2, (50, 550))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MYEVENTTYPE and button_start.is_checked():
                pygame.quit()
                sys.exit()
            button_start.update(event)
        button_start.render()
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)

    start_screen()

    pygame.display.set_caption('PyTanks – Игра')

    all_sprites = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    tanks = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    running = True

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 10)

    start = time.time()

    board = Board(14, 14, all_sprites, tile_width, tile_height, tile_images, screen, pattern=str(lvl) + ".txt")
    board.render()

    tank = None
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if board.board[i][j] == list(tile_images.keys()).index("Точка спавна") + 1:
                tank = Tank(i * tile_width, j * tile_height, board, all_sprites, tanks)
                board.board[i][j] = 0
                board.render()

    tank = Tank((width - load_image("tankkk.png").get_width()) / 2,
                (height - load_image("tankkk.png").get_height()) / 2, board, all_sprites, tanks) \
        if not tank else tank
    tanks.add(tank)

    while len(tanks) <= enemies:
        first_filter = random.randint(0, len(board.board) - 1)
        if not len(list(filter(lambda x: x != 0, board.board[first_filter]))) == board.board[first_filter]:
            second_filter = random.randint(0, len(board.board[first_filter]) - 1)
            if board.board[first_filter][second_filter] == 0:
                bot_tank = EnemyTank(first_filter * tile_width, second_filter * tile_height, board, all_sprites, tanks, tank, shots)
                tanks.add(bot_tank)

    while running:
        all_sprites.remove(tank)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        tanks.draw(screen)
        explosions.draw(screen)
        shots.draw(screen)
        for event in pygame.event.get():
            for i in tanks:
                threading.Thread(target=i.update).start()
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False

            if keys[pygame.K_LEFT] and not tank.is_collide_left and not (
                    keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                tank.pos = "left"
                tank.rect.x -= 1
                tank.image = pygame.transform.rotate(load_image("tankkk.png"), 90)

            if keys[pygame.K_RIGHT] and not tank.is_collide_right and not (
                    keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                tank.pos = "right"
                tank.rect.x += 1
                tank.image = pygame.transform.rotate(load_image("tankkk.png"), -90)

            if keys[pygame.K_UP] and not tank.is_collide_up and not (
                    keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN]):
                tank.pos = "up"
                tank.rect.y -= 1
                tank.image = pygame.transform.rotate(load_image("tankkk.png"), 0)

            if keys[pygame.K_DOWN] and not tank.is_collide_down and not (
                    keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_LEFT]):
                tank.pos = "down"
                tank.rect.y += 1
                tank.image = pygame.transform.rotate(load_image("tankkk.png"), 180)

            if time.time() - start > 1 and keys[pygame.K_SPACE]:
                threading.Thread(target=shoot, args=(shots, tank.pos, tank)).start()
                start = time.time()

            if event.type == MYEVENTTYPE:
                for x in shots:
                    x.update(all_sprites, board, explosions, tanks)

            if pygame.sprite.spritecollide(tank, pygame.sprite.Group(list(filter(lambda x: x.host != tank, shots))), False):
                running = False
                the_end()

            if len(tanks) == 1:
                running = False
                the_win()

            tank.update()
            for i in explosions:
                threading.Thread(target=i.update).start()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
