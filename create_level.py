import pygame
import os
import sys
import checkbox
import button


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('wall.png'),
    'box': load_image("box.png")
}
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Board:
    colors = ["black", "white"]

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

    def render(self, screen, object=None):
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
                if self.board[i1][j1] == 1:
                    check = False
                    for x in all_sprites:
                        if x.rect == (tile_width * i / self.cell_size, tile_height * j / self.cell_size, 50, 50):
                            check = True
                    if not check:
                        if object:
                            all_sprites.add(Tile(object, i / self.cell_size, j / self.cell_size))

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

    def on_click(self, cell_coords, object):
        if cell_coords:
            x, y = cell_coords
            self.board[y][x] = (self.board[y][x] + 1) % 2
            self.render(screen, object)

    def get_click(self, mouse_pos, object):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, object)


if __name__ == '__main__':
    pygame.init()
    all_sprites = pygame.sprite.Group()
    screen = pygame.display.set_mode((1100, 700))
    board = Board(14, 14)
    running = True
    board.render(screen)

    checkbox_stena = checkbox.Checkbox(screen, 750, 100, "wall", activated=True)
    checkbox_korobka = checkbox.Checkbox(screen, 750, 150, "box")
    checkbox_list = list()
    checkbox_list.append(checkbox_korobka)
    checkbox_list.append(checkbox_stena)
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

        font = pygame.font.Font(None, 30)
        text = font.render("Кирпичная стена", False, (143, 20, 2))
        text_x = 770
        text_y = 96
        screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 30)
        text = font.render("Разрушаемая коробка", False, (143, 20, 2))
        text_x = 770
        text_y = 148
        screen.blit(text, (text_x, text_y))

        # button_clear = button.Button(screen)
        #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in checkbox_list:
                    if btn.checked:
                        board.get_click(event.pos, btn.name)
            checkbox_stena.update(event, checkbox_list)
            checkbox_korobka.update(event, checkbox_list)
            print(board.board)

        all_sprites.draw(screen)
        checkbox_stena.render_checkbox()
        checkbox_korobka.render_checkbox()
        pygame.display.flip()