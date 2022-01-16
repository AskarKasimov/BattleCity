import pygame
import sys
import os
from board import Board


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
        super().__init__(all_sprites)
        self.image = Tank.image
        self.rect = pygame.Rect(x, y, self.image.get_width() + x, self.image.get_height() + y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global is_collide_up, is_collide_down, is_collide_left, is_collide_right
        for i in all_sprites:
            if pygame.sprite.collide_mask(self, i):
                is_collide_up = True
                break
        else:
            is_collide_up = False
        for i in all_sprites:
            if pygame.sprite.collide_mask(self, i):
                is_collide_down = True
                break
        else:
            is_collide_down = False
        for i in all_sprites:
            if pygame.sprite.collide_mask(self, i):
                is_collide_left = True
                break
        else:
            is_collide_left = False
        for i in all_sprites:
            if pygame.sprite.collide_mask(self, i):
                is_collide_right = True
                break
        else:
            is_collide_right = False


class Wall(pygame.sprite.Sprite):
    image = load_image("Wall.jpg")

    def __init__(self, x, y, check=True):
        super().__init__(all_sprites)
        if not check:  # вертикальная стенка
            self.image = pygame.transform.rotate(load_image("Wall.jpg"), 90)
        else:  # горизонтальная стенка
            self.image = Wall.image
        self.rect = pygame.Rect(x, y, x + self.image.get_width(), y + self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)


class Shot(pygame.sprite.Sprite):
    image = load_image("shot.jpg")

    def __init__(self):
        super().__init__(all_sprites)
        global pos
        self.image = Shot.image
        self.vx = 0
        self.vy = 0
        if pos == "up":
            self.rect = pygame.Rect(tank.rect.x + 10, tank.rect.y - 10, self.image.get_width() + tank.rect.x, self.image.get_height() + tank.rect.y)
            Shot.image = pygame.transform.rotate(load_image("shot.jpg"), 90)
            self.vy = -3
        if pos == "down":
            self.rect = pygame.Rect(tank.rect.x + 10, tank.rect.y + 30, self.image.get_width() + tank.rect.x, self.image.get_height() + tank.rect.y)
            Shot.image = pygame.transform.rotate(load_image("shot.jpg"), -90)
            self.vy = 3
        if pos == "left":
            self.rect = pygame.Rect(tank.rect.x - 10, tank.rect.y + 10, self.image.get_width() + tank.rect.x, self.image.get_height() + tank.rect.y)
            Shot.image = pygame.transform.rotate(load_image("shot.jpg"), 180)
            self.vx = -3
        if pos == "right":
            self.rect = pygame.Rect(tank.rect.x + 30, tank.rect.y + 10, self.image.get_width() + tank.rect.x, self.image.get_height() + tank.rect.y)
            Shot.image = pygame.transform.rotate(load_image("shot.jpg"), 0)
            self.vx = 3
        self.mask = pygame.mask.from_surface(self.image)

    # def update(self):
    #     self.rect = self.rect.move(self.vx, self.vy)
    #     if pygame.sprite.spritecollideany(self, borders_up) or pygame.sprite.spritecollideany(self, borders_down)\
    #             or pygame.sprite.spritecollideany(self, borders_left) or pygame.sprite.spritecollideany(self, borders_right):
    #         """if pygame.sprite.spritecollideany(self, borders_up):
    #             print(pygame.sprite.spritecollideany(self, borders_up).rect)
    #         if pygame.sprite.spritecollideany(self, borders_down):
    #             print(pygame.sprite.spritecollideany(self, borders_down).rect)
    #         if pygame.sprite.spritecollideany(self, borders_right):
    #             print(pygame.sprite.spritecollideany(self, borders_right).rect)
    #         if pygame.sprite.spritecollideany(self, borders_left):
    #             print(pygame.sprite.spritecollideany(self, borders_left).rect)"""
    #         self.kill()


if __name__ == '__main__':
    tile_images = {
        'Кирпичная стена': load_image('wall.png'),
        'Разрушаемая коробка': load_image("box.png"),
        'Трава': load_image('grass.png'),
        'Вода': load_image('newwoter.png')
    }
    tile_width = tile_height = 50
    is_collide_up, is_collide_down, is_collide_left, is_collide_right = False, False, False, False
    pygame.init()
    size = width, height = 700, 700
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    # borders_up = pygame.sprite.Group()
    # borders_down = pygame.sprite.Group()
    # borders_left = pygame.sprite.Group()
    # borders_right = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    tanks = pygame.sprite.Group()
    # borders_up.add(Wall(0, 0, True), Wall(150, 0, True), Wall(300, 0, True), Wall(450, 0, True))
    # borders_down.add(Wall(0, 570, True), Wall(150, 570, True), Wall(300, 570, True), Wall(450, 570, True))
    # borders_left.add(Wall(0, 0, False), Wall(0, 150, False), Wall(0, 300, False), Wall(0, 450, False))
    # borders_right.add(Wall(570, 0, False), Wall(570, 150, False), Wall(570, 300, False), Wall(570, 450, False))
    running = True
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 10)
    tank = Tank((width - load_image("tank.png").get_width()) / 2, (height - load_image("tank.png").get_height()) / 2)
    tanks.add(tank)
    pos = "up"
    board = Board(14, 14, all_sprites, tile_width, tile_height, tile_images, screen, pattern="3.txt")
    board.render()
    # for i in all_sprites:
    #     # print(pygame.sprite.collide_rect(tank, i))
    #     # print(i.rect.x)
    #     # print(i.rect.y)
    #     print(tank.rect.colliderect(i.rect))
    #     if tank.rect.colliderect(i.rect):
    #         all_sprites.remove(i)
    while running:
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        tanks.draw(screen)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            pressed = pygame.mouse.get_pressed()
            if event.type == pygame.QUIT:
                running = False
            if keys[pygame.K_LEFT] and not pygame.sprite.spritecollide(tank, all_sprites, False) and not(keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                pos = "left"
                tank.rect.x -= 1
                tank.image = pygame.transform.rotate(load_image("tank.png"), 90)
            if keys[pygame.K_RIGHT] and not pygame.sprite.spritecollide(tank, all_sprites, False) and not(keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]):
                pos = "right"
                tank.rect.x += 1
                tank.image = pygame.transform.rotate(load_image("tank.png"), -90)
            if keys[pygame.K_UP] and not pygame.sprite.spritecollide(tank, all_sprites, False) and not(keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_DOWN]):
                pos = "up"
                tank.rect.y -= 1
                tank.image = pygame.transform.rotate(load_image("tank.png"), 0)
            if keys[pygame.K_DOWN] and not pygame.sprite.spritecollide(tank, all_sprites, False) and not(keys[pygame.K_RIGHT] or keys[pygame.K_UP] or keys[pygame.K_LEFT]):
                pos = "down"
                tank.rect.y += 1
                tank.image = pygame.transform.rotate(load_image("tank.png"), 180)
            if keys[pygame.K_SPACE]:
                if len(shots) == 0:
                    shot = Shot()
                    all_sprites.add(shot)
                    shots.add(shot)
            if event.type == MYEVENTTYPE:
                for x in shots:
                    x.update()
            tank.update()
        pygame.display.flip()
    pygame.quit()