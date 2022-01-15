import pygame
import os
import sys
import checkbox
import button


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
    'Вода': load_image('newwoter.png')
}
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        i1 = 0
        j1 = 0
        for i in range(self.left, self.height * self.cell_size, self.cell_size):
            for j in range(self.top, self.width * self.cell_size, self.cell_size):
                if self.board[i1][j1] == 0:
                    for x in all_sprites:
                        if x.rect == (tile_width * i / self.cell_size, tile_height * j / self.cell_size, 50, 50):
                            x.kill()
                            break
                    pygame.draw.rect(screen, (255, 255, 255), (i, j, self.cell_size, self.cell_size), 1)
                    pygame.draw.rect(screen, (0, 0, 0), (i + 1, j + 1, self.cell_size - 2, self.cell_size - 2), 0)
                else:
                    check = False
                    for x in all_sprites:
                        if x.rect == (tile_width * i / self.cell_size, tile_height * j / self.cell_size, 50, 50):
                            check = True
                    if not check:
                        all_sprites.add(Tile(list(tile_images.keys())[self.board[i1][j1] - 1], i / self.cell_size,
                                             j / self.cell_size))

                j1 += 1
            i1 += 1
            j1 = 0

    def get_cell(self, mouse_pos):
        y = (mouse_pos[0] - self.left) // self.cell_size
        x = (mouse_pos[1] - self.top) // self.cell_size
        if 0 <= x < self.width and 0 <= y < self.height:
            return x, y
        else:
            return None

    def on_click(self, cell_coords, object=None):
        if cell_coords:
            x, y = cell_coords
            if object and self.board[y][x] == 0:
                self.board[y][x] = list(tile_images.keys()).index(object) + 1
            elif not object:
                self.board[y][x] = 0
            self.render(screen)

    def get_click(self, mouse_pos, object=None):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, object)


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((1100, 700))
    board = Board(14, 14)
    running = True
    board.render(screen)

    checkbox_list = list()
    x = 100
    for i in range(len(tile_images)):
        checkbox_list.append(checkbox.Checkbox(screen, 750, x, 12, 12, list(tile_images.keys())[i]))
        x += 50
    checkbox_list[0].checked = True
    clock = pygame.time.Clock()

    button_clear = button.Button(screen, 790, 100 + 50 * len(tile_images), "Сбросить")
    button_save = button.Button(screen, 915, 100 + 50 * len(tile_images), "Сохранить")

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 7)
    while running:
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
                            file.write(str(board.board[j][i]))
                        file.write("\n")
                button_save.checked = False

            if event.type == MYEVENTTYPE and button_clear.is_checked():
                for i in range(len(board.board)):
                    for j in range(len(board.board[i])):
                        board.board[j][i] = 0
                all_sprites.clear(screen, screen)
                board.render(screen)
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
