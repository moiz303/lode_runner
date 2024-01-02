import pygame
import os
import sys
import random
import generate


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
    screen = pygame.display.set_mode((810, 410))
    pygame.display.set_caption('Lode Runner')

    board = generate.Game()
    board.set_view(5, 5, 50)

    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()

    # создадим спрайты
    player = pygame.sprite.Sprite(all_sprites)

    # определим их вид
    player.image = load_image("player.xcf")

    # размеры
    player.rect = player.image.get_rect()

    # и их расположение - игрок
    player.rect.x = 0
    player.rect.y = 285

    # блоки
    for i in range(1, 8, 2):
        for j in range(16):
            generate.Blocks(j, i, all_sprites)

    # лестницы
    for i in range(1, 6, 2):
        for j in range(2):
            x = random.randint(0, 16)
            generate.Ladder(x, i, all_sprites)
            generate.Ladder(x, i + 1, all_sprites)
    # монетки
    for i in range(3):
        generate.Money(all_sprites)

    dist = 50
    running = True
    while running:
        for event in pygame.event.get():
            # Проверка на нажатие клавиш движения
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.rect.left += dist
                elif event.key == pygame.K_LEFT:
                    player.rect.left -= dist
                elif event.key == pygame.K_DOWN:
                    player.rect.top += dist
                elif event.key == pygame.K_UP:
                    player.rect.top -= dist
            # Проверка на выход из игры
            elif event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0), (5, 5, screen.get_size()[0] - 10, screen.get_size()[1] - 10))
        board.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
