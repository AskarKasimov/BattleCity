import os
import sys
import pygame
from tank import Tank


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class EnemyTank(Tank):
    def __init__(self, x, y, board, all_sprites_group, all_tanks_group):
        super().__init__(x, y, board, all_sprites_group, all_tanks_group)
        self.image = load_image("enemy_tankk.png")