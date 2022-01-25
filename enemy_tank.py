import os
import sys
import threading
import time

import pygame
from tank import Tank


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# танк-бот (сам катается)
class EnemyTank(Tank):
    def __init__(self, x, y, board, all_sprites_group, all_tanks_group, player, shots):
        super().__init__(x, y, board, all_sprites_group, all_tanks_group)
        self.image = load_image("enemy_tankk.png")
        self.target = player
        self.shots = shots
        self.start = time.time()

    def update(self):
        super(EnemyTank, self).update()
        target_x = self.target.rect.centerx
        target_y = self.target.rect.centery
        self_x = self.rect.centerx
        self_y = self.rect.centery
        if time.time() - self.start > 1 and self_x == target_x and self_y > target_y:
            self.pos = "up"
            self.image = pygame.transform.rotate(load_image("enemy_tankk.png"), 0)
            threading.Thread(target=self.shoot, args=(self.shots,)).start()
            self.start = time.time()
        elif time.time() - self.start > 1 and self_x == target_x and self_y < target_y:
            self.pos = "down"
            self.image = pygame.transform.rotate(load_image("enemy_tankk.png"), 180)
            threading.Thread(target=self.shoot, args=(self.shots,)).start()
            self.start = time.time()
        elif time.time() - self.start > 1 and self_x > target_x and self_y == target_y:
            self.pos = "left"
            self.image = pygame.transform.rotate(load_image("enemy_tankk.png"), 90)
            threading.Thread(target=self.shoot, args=(self.shots,)).start()
            self.start = time.time()
        elif time.time() - self.start > 1 and self_x < target_x and self_y == target_y:
            self.pos = "right"
            self.image = pygame.transform.rotate(load_image("enemy_tankk.png"), -90)
            threading.Thread(target=self.shoot, args=(self.shots,)).start()
            self.start = time.time()

        if self_x > target_x and not self.is_collide_left:
            self.pos = "left"
            self.image = pygame.transform.rotate(load_image("enemy_tankk.png"), 90)
            self.rect.x -= 1
        elif self_x < target_x and not self.is_collide_right:
            self.pos = "right"
            self.image = pygame.transform.rotate(load_image("enemy_tankk.png"), -90)
            self.rect.x += 1
        elif self_y > target_y and not self.is_collide_up:
            self.pos = "up"
            self.image = pygame.transform.rotate(load_image("enemy_tankk.png"), 0)
            self.rect.y -= 1
        elif self_y < target_y and not self.is_collide_down:
            self.pos = "down"
            self.image = pygame.transform.rotate(load_image("enemy_tankk.png"), 180)
            self.rect.y += 1
