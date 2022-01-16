import pygame


class Board:
    # создание поля
    def __init__(self, width, height, sprites, tile_width, tile_height, tile_images, screen, pattern=None):
        self.width = width
        self.height = height
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 50
        self.all_sprites = sprites
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.screen = screen
        self.tile_images = tile_images
        if pattern:
            with open("levels/" + pattern, "r") as file:
                self.board = list()
                line = file.readline()
                while line:
                    line = line.replace("\n", "")
                    self.board.append(list([int(x) for x in line]))
                    line = file.readline()
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    self.board[i][j], self.board[j][i] = self.board[i][j], self.board[j][i]
        else:
            self.board = [[0] * width for _ in range(height)]

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        i1 = 0
        j1 = 0
        for i in range(self.left, self.height * self.cell_size, self.cell_size):
            for j in range(self.top, self.width * self.cell_size, self.cell_size):
                if self.board[i1][j1] == 0:
                    for x in self.all_sprites:
                        if x.rect == (self.tile_width * i / self.cell_size, self.tile_height * j / self.cell_size, 50, 50):
                            x.kill()
                            break
                    pygame.draw.rect(self.screen, (255, 255, 255), (i, j, self.cell_size, self.cell_size), 1)
                    pygame.draw.rect(self.screen, (0, 0, 0), (i + 1, j + 1, self.cell_size - 2, self.cell_size - 2), 0)
                else:
                    check = False
                    for x in self.all_sprites:
                        if x.rect == (self.tile_width * i / self.cell_size, self.tile_height * j / self.cell_size, 50, 50):
                            check = True
                    if not check:
                        self.all_sprites.add(Tile(list(self.tile_images.keys())[self.board[i1][j1] - 1], i / self.cell_size,
                                             j / self.cell_size, self.all_sprites, self.tile_images, self.tile_width, self.tile_height))

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
                self.board[y][x] = list(self.tile_images.keys()).index(object) + 1
            elif not object:
                self.board[y][x] = 0
            self.render()

    def get_click(self, mouse_pos, object=None):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell, object)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, all_sprites, tile_images, tile_width, tile_height):
        super().__init__(all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
