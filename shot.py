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


class Shot(pygame.sprite.Sprite):
    image = load_image("shot.png")

    def __init__(self, pos, shots, tank):
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

    def update(self, all_sprites, board):
        if pygame.sprite.spritecollide(self, pygame.sprite.Group(list(filter(
                lambda x: board.board[x.rect[0] // tile_width][x.rect[1] // tile_height] == list(
                        tile_images.keys()).index("Разрушаемая коробка") + 1, all_sprites))), True):
            self.kill()
        if pygame.sprite.spritecollide(self, pygame.sprite.Group(list(filter(
                lambda x: board.board[x.rect[0] // tile_width][x.rect[1] // tile_height] == list(
                        tile_images.keys()).index("Кирпичная стена") + 1, all_sprites))), False):
            self.kill()
        if self.pos == "up":
            self.rect.y -= 2
        if self.pos == "down":
            self.rect.y += 2
        if self.pos == "left":
            self.rect.x -= 2
        if self.pos == "right":
            self.rect.x += 2
        if self.rect.x < -25 or self.rect.x > len(board.board) * tile_width + 25 or self.rect.y < -25 or self.rect.y > len(board.board[0]) * tile_height + 25:
            self.kill()
