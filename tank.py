import os
import sys
import pygame
from create_level import tile_width, tile_height, tile_images


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Tank(pygame.sprite.Sprite):
    image = load_image("tankkk.png")

    def __init__(self, x, y, board, all_sprites_group, all_tanks_group):
        super().__init__(all_tanks_group)
        self.image = Tank.image
        self.pos = "up"
        self.all_sprites = all_sprites_group
        self.board = board
        self.is_collide_up = False
        self.is_collide_down = False
        self.is_collide_left = False
        self.is_collide_right = False
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        for i in self.all_sprites:
            if pygame.rect.Rect(self.rect.x + 1, self.rect.y, self.rect.width, self.rect.height).colliderect(i.rect) and \
                    self.board.board[i.rect[0] // tile_width][i.rect[1] // tile_height] != list(tile_images.keys()).index("Трава") + 1:
                self.is_collide_right = True
                break
        else:
            self.is_collide_right = False
        for i in self.all_sprites:
            if pygame.rect.Rect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height).colliderect(i.rect) and \
                    self.board.board[i.rect[0] // tile_width][i.rect[1] // tile_height] != list(tile_images.keys()).index("Трава") + 1:
                self.is_collide_down = True
                break
        else:
            self.is_collide_down = False
        for i in self.all_sprites:
            if pygame.rect.Rect(self.rect.x - 1, self.rect.y, self.rect.width, self.rect.height).colliderect(i.rect) and \
                    self.board.board[i.rect[0] // tile_width][i.rect[1] // tile_height] != list(tile_images.keys()).index("Трава") + 1:
                self.is_collide_left = True
                break
        else:
            self.is_collide_left = False

        for i in self.all_sprites:
            if pygame.rect.Rect(self.rect.x, self.rect.y - 1, self.rect.width, self.rect.height).colliderect(i.rect) and \
                    self.board.board[i.rect[0] // tile_width][i.rect[1] // tile_height] != list(tile_images.keys()).index("Трава") + 1:
                self.is_collide_up = True
                break
        else:
            self.is_collide_up = False