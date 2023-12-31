import pygame
import os
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
        for y in range(8):
            for x in range(16):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


class Blocks(pygame.sprite.Sprite):
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
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("player.xcf")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 5
        self.rect.y = 304


class Bots(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image("bot.xcf")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = 405
        self.rect.y = 5
