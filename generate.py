import os
import pygame
import sys

# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Game:
    # создание поля
    def __init__(self):
        # значения по умолчанию
        self.left = 5
        self.top = 5
        self.cell_size = 50
        self.width = 16
        self.height = 8
        self.bot_cords = [8, 0]

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


class Blocks(pygame.sprite.Sprite):
    """Генерация блоков"""
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = load_image("block.xcf")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x * 50 + 5
        self.rect.y = y * 50 + 5

    def return_all(self):
        return self.image, self.rect


class Money(pygame.sprite.Sprite):
    """Генерация монеток"""
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = load_image("money.xcf")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x * 50 + 5
        self.rect.y = y * 50 + 5

    def return_all(self):
        return self.image, self.rect


class Ladder(pygame.sprite.Sprite):
    """Генерация лестниц"""
    def __init__(self, x, y, group):
        super().__init__(group)
        self.image = load_image("ladder.xcf")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x * 50 + 5
        self.rect.y = y * 50 + 5

    def return_all(self):
        return self.image, self.rect


class Player(pygame.sprite.Sprite):
    """Создание игрока с анимациями"""
    def __init__(self, group, sheet, x, y):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, 4, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.frames = []
        self.recti = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.recti.w * i, self.recti.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.recti.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Bots(pygame.sprite.Sprite):
    """Создание бота с его анимациями"""
    def __init__(self, group, sheet, x, y):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, 3, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.frames = []
        self.recti = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.recti.w * i, self.recti.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.recti.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
