import pygame
import random
from main import load_image

# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()


class Game:
    # создание поля
    def __init__(self):
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

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
    image = load_image("block.xcf")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Blocks.image
        self.rect = self.image.get_rect()
        self.rect.x = x * 50 + 5
        self.rect.y = y * 50 + 5


class Money(pygame.sprite.Sprite):
    image = load_image("money.xcf")

    def __init__(self, *group):
        super().__init__(*group)
        self.rect = Money.image.get_rect()
        self.rect.x = random.randint(0, 16) * 50 + 5
        self.rect.y = random.randrange(0, 6, 2) * 50 + 5


class Ladder(pygame.sprite.Sprite):
    image = load_image("ladder.xcf")

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.rect = Ladder.image.get_rect()
        self.rect.x = x * 50 + 5
        self.rect.y = y * 50 + 5
