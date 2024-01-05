import pygame
import sys
import os
import random
import generate
import levels


pygame.init()
screen = pygame.display.set_mode((810, 410))
pygame.display.set_caption('Lode Runner')
clock = pygame.time.Clock()


FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global board, clicked_button
    intro_text = ["Начнём игру",
                  "Чтобы сгенерировать уровень нажмите 1",
                  "Чтобы выбрать из сохранённых нажмите 2"]

    fon = pygame.transform.scale(generate.load_image('fon.jpg'), (800, 400))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    board = generate.Game()
                    board.set_view(5, 5, 50)
                    clicked_button = 1
                    return  # начинаем игру
                elif event.key == pygame.K_2:
                    board = generate.Game()
                    board.set_view(5, 5, 50)
                    clicked_button = 2
                    return  # начнём игру
                else:
                    print('error')
                    continue  # Неправильный ввод, пробуем ещё
        pygame.display.flip()
        clock.tick(FPS)


def take_level():
    intro_text = [f'Нажмите {os.listdir(os.path.join("levels")).index(i) + 1}, чтобы выбрать уровень ' + i[:-4]
                  for i in os.listdir(os.path.join("levels"))]

    fon = pygame.transform.scale(generate.load_image('fon.jpg'), (800, 400))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return pygame.key.get_pressed().index(True)
        pygame.display.flip()
        clock.tick(FPS)


def main():
    start_screen()

    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()

    # Если нажата кнопка 1, то генерируем уровень
    if clicked_button == 1:
        # создадим блоки,
        for i in range(1, 8, 2):
            for j in range(16):
                generate.Blocks(j, i, all_sprites)

        # лестницы
        for i in range(1, 6, 2):
            for j in range(2):
                x = random.randint(1, 16)
                generate.Ladder(x, i, all_sprites)
                generate.Ladder(x, i + 1, all_sprites)

        # и монетки
        for i in range(3):
            generate.Money(random.randint(1, 16) ,
                           random.randrange(0, 6, 2), all_sprites)

    # Если нажата кнопка 2, то выбираем из сохранённых
    else:
        running = True
        while running:
            # "Защита от дурака" - проверка, что выбранный уровень существует
            try:
                num = take_level() - 30
                level = levels.load_level(os.listdir(os.path.join("levels"))[num])
                # Выстраивание уровня по блокам
                for y in range(len(level)):
                    for x in range(len(level[y])):
                        levels.return_all(level[y][x], x, y, all_sprites)
                running = False
            except IndexError:
                print('Нажмите корректную клавишу')

    # под конец создадим игрока
    player = generate.Player(all_sprites)

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
