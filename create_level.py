#
# создатель уровней
#

import pygame
import os
import sys
from checkbox import Checkbox
from button import Button
from board import Board


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'Кирпичная стена': load_image('wall.png'),
    'Разрушаемая коробка': load_image("box.png"),
    'Трава': load_image('grass.png'),
    'Вода': load_image('newwoter.png'),
    "Точка спавна": load_image('spawn.png')
}

tile_width = tile_height = 50

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('PyTanks – Редактор уровней')
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((1100, 700))
    board = Board(14, 14, all_sprites, tile_width, tile_height, tile_images, screen)
    running = True
    board.render()

    checkbox_list = list()
    x = 100
    for i in range(len(tile_images)):
        checkbox_list.append(Checkbox(screen, 750, x, 12, 12, list(tile_images.keys())[i]))
        x += 50
    checkbox_list[0].checked = True
    clock = pygame.time.Clock()

    button_clear = Button(screen, 790, 100 + 50 * len(tile_images), "Сбросить")
    button_save = Button(screen, 915, 100 + 50 * len(tile_images), "Сохранить")

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 7)

    # отрисовка кнопок и текста
    font = pygame.font.Font(None, 50)
    text = font.render("Создание уровня", False, (143, 20, 2))
    text_x = 745
    text_y = 25
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (143, 20, 2), (text_x - 10, text_y - 10,
                                            text_w + 20, text_h + 20), 3)
    x = 96
    for i in tile_images.keys():
        font = pygame.font.Font(None, 30)
        text = font.render(i, False, (143, 20, 2))
        text_x = 770
        text_y = x
        screen.blit(text, (text_x, text_y))
        x += 50
    #

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if pygame.mouse.get_pressed()[0]:
                for btn in checkbox_list:
                    if btn.checked:
                        try:
                            board.get_click(event.pos, btn.name)
                        except AttributeError:
                            pass
            if pygame.mouse.get_pressed()[2]:
                for btn in checkbox_list:
                    if btn.checked:
                        try:
                            board.get_click(event.pos)
                        except AttributeError:
                            pass

            if event.type == MYEVENTTYPE and button_save.is_checked():
                with open("levels/" + str(len(os.listdir(path="levels")) + 1) + ".txt", "w") as file:
                    for i in range(len(board.board)):
                        for j in range(len(board.board[i])):
                            file.write(str(board.board[i][j]))
                        file.write("\n")
                button_save.checked = False

            if event.type == MYEVENTTYPE and button_clear.is_checked():
                for i in range(len(board.board)):
                    for j in range(len(board.board[i])):
                        board.board[j][i] = 0
                all_sprites.clear(screen, screen)
                board.render()
                button_clear.checked = False

            [x.update(event, checkbox_list) for x in checkbox_list]
            button_save.update(event)
            button_clear.update(event)
        all_sprites.draw(screen)
        [x.render() for x in checkbox_list]
        button_clear.render()
        button_save.render()
        pygame.display.flip()
        clock.tick(60)
