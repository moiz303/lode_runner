import pygame
import os
import sys


class Game:
    # создание поля
    def __init__(self):
        self.board = [[0] * 20 for _ in range(7)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def render(self, screen):
        for y in range(7):
            for x in range(20):
                pygame.draw.rect(screen, pygame.Color(255, 255, 255), (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size,
                    self.cell_size), 1)

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 360))
    pygame.display.set_caption('Lode Runner')
    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()

    # создадим спрайты
    player = pygame.sprite.Sprite(all_sprites)

    # определим их вид
    player.image = load_image("player.xcf")
    player.rect = player.image.get_rect()

    # и их расположение
    player.rect.x = 0
    player.rect.y = 235

    board = Game()
    board.set_view(5, 5, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(pygame.Color('orange'), (5, 5, screen.get_size()[0] - 10, screen.get_size()[1] - 10))
        board.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
