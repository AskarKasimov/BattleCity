import pygame
import sys
import os
from board import Board
from create_level import tile_width, tile_height, tile_images


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Tank(pygame.sprite.Sprite):
    image = load_image("tank.png")

    def __init__(self, x, y):
        super().__init__(tanks)
        self.image = Tank.image
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global is_collide_up, is_collide_down, is_collide_left, is_collide_right
        for i in all_sprites:
            if pygame.rect.Rect(self.rect.x + 1, self.rect.y, self.rect.width, self.rect.height).colliderect(i.rect) and \
                    board.board[i.rect[0] // tile_width][i.rect[1] // tile_height] != list(tile_images.keys()).index("Трава") + 1:
                is_collide_right = True
                break
        else:
            is_collide_right = False
        for i in all_sprites:
            if pygame.rect.Rect(self.rect.x, self.rect.y + 1, self.rect.width, self.rect.height).colliderect(i.rect) and \
                    board.board[i.rect[0] // tile_width][i.rect[1] // tile_height] != list(tile_images.keys()).index("Трава") + 1:
                is_collide_down = True
                break
        else:
            is_collide_down = False
        for i in all_sprites:
            if pygame.rect.Rect(self.rect.x - 1, self.rect.y, self.rect.width, self.rect.height).colliderect(i.rect) and \
                    board.board[i.rect[0] // tile_width][i.rect[1] // tile_height] != list(tile_images.keys()).index("Трава") + 1:
                is_collide_left = True
                break
        else:
            is_collide_left = False

        for i in all_sprites:
            if pygame.rect.Rect(self.rect.x, self.rect.y - 1, self.rect.width, self.rect.height).colliderect(i.rect) and \
                    board.board[i.rect[0] // tile_width][i.rect[1] // tile_height] != list(tile_images.keys()).index("Трава") + 1:
                is_collide_up = True
                break
        else:
            is_collide_up = False


class Shot(pygame.sprite.Sprite):
    image = load_image("shot.png")

    def __init__(self, pos):
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

    def update(self):
        for i in all_sprites:
            if self.rect.colliderect(i.rect):
                if board.board[i.rect[0] // tile_width][i.rect[1] // tile_height] == list(tile_images.keys()).index("Разрушаемая коробка") + 1:
                    i.kill()
                self.kill()
        if self.pos == "up":
            self.rect.y -= 2
        if self.pos == "down":
            self.rect.y += 2
        if self.pos == "left":
            self.rect.x -= 2
        if self.pos == "right":
            self.rect.x += 2
        if self.rect.x < -25 or self.rect.x > width + 25 or self.rect.y < -25 or self.rect.y > height + 25:
            self.kill()


if __name__ == '__main__':
    is_collide_up, is_collide_down, is_collide_left, is_collide_right = False, False, False, False
    pygame.init()
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    tanks = pygame.sprite.Group()
    running = True

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 10)

    board = Board(14, 14, all_sprites, tile_width, tile_height, tile_images, screen, pattern="2.txt")
    board.render()
    tank = None
    for i in range(len(board.board)):
        for j in range(len(board.board[i])):
            if board.board[i][j] == list(tile_images.keys()).index("Точка спавна") + 1:
                tank = Tank(i * tile_width, j * tile_height)
                board.board[i][j] = 0
                board.render()
    tank = Tank((width - load_image("tank.png").get_width()) / 2, (height - load_image("tank.png").get_height()) / 2) if not tank else tank
    tanks.add(tank)
    pos = "up"
    while running:
        all_sprites.remove(tank)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        tanks.draw(screen)
        shots.draw(screen)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            # TODO: нормальное перемещение
            if keys[pygame.K_LEFT] and not is_collide_left and not(keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                pos = "left"
                tank.rect.x -= 1
                tank.image = pygame.transform.rotate(load_image("tank.png"), 90)
            if keys[pygame.K_RIGHT] and not is_collide_right and not(keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                pos = "right"
                tank.rect.x += 1
                tank.image = pygame.transform.rotate(load_image("tank.png"), -90)
            if keys[pygame.K_UP] and not is_collide_up and not(keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN]):
                pos = "up"
                tank.rect.y -= 1
                tank.image = pygame.transform.rotate(load_image("tank.png"), 0)
            if keys[pygame.K_DOWN] and not is_collide_down and not(keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_LEFT]):
                pos = "down"
                tank.rect.y += 1
                tank.image = pygame.transform.rotate(load_image("tank.png"), 180)
            if keys[pygame.K_SPACE]:
                if len(shots) == 0:
                    shot = Shot(pos)
                    shots.add(shot)
            if event.type == MYEVENTTYPE:
                for x in shots:
                    x.update()
            tank.update()
        pygame.display.flip()
    pygame.quit()
