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
        self.host = tank
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

    def update(self, all_sprites, board, explosions, tanks):
        if self.host == list(tanks)[0]:
            a = tanks.copy()
            a.remove(self.host)
            if pygame.sprite.spritecollide(self, a, True):
                self.host.increase_score()
                self.kill()
                destruction(explosions, self.rect.x - 15, self.rect.y - 10)

        if pygame.sprite.spritecollide(self, pygame.sprite.Group(list(filter(
                lambda x: board.board[x.rect[0] // tile_width][x.rect[1] // tile_height] == list(
                        tile_images.keys()).index("Разрушаемая коробка") + 1, all_sprites))), True):
            self.kill()
            destruction(explosions, self.rect.x - 15, self.rect.y - 10)
        if pygame.sprite.spritecollide(self, pygame.sprite.Group(list(filter(
                lambda x: board.board[x.rect[0] // tile_width][x.rect[1] // tile_height] == list(
                        tile_images.keys()).index("Кирпичная стена") + 1, all_sprites))), False):
            self.kill()
            destruction(explosions, self.rect.x - 15, self.rect.y - 10)
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
            destruction(explosions, self.rect.x - 15, self.rect.y - 10)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, explosions):
        super().__init__(explosions)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.count = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if not self.count == 10:
            self.count += 1
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        else:
            self.kill()


def destruction(explosions, x, y):
    AnimatedSprite(load_image("boom.png"), 5, 2, x, y, explosions)
