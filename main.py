import timeit
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
player_cords = [5, 304]
dist = 50
# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()

# создадим список мест, где уже есть блоки
filled = {}

blocks, ladders, moneys = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()


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
                    print('Нажмите корректную кнопку')
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


def final_screen(time):
    line = f'Вы прошли уровень за {round(time, 2)} секунд!'

    fon = pygame.transform.scale(generate.load_image('fon.jpg'), (810, 410))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    string_rendered = font.render(line, 1, pygame.Color('white'))
    intro_rect = string_rendered.get_rect()
    intro_rect.top = 100
    intro_rect.x = 10
    screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.flip()


def main():
    start_screen()

    # Если нажата кнопка 1, то генерируем уровень
    if clicked_button == 1:
        # создадим лестницы,
        for i in range(1, 6, 2):
            for j in range(2):
                x = random.randint(1, 15)
                if (x, i) not in filled.keys() and (x + 1, i) not in filled.keys():
                    ladders.add(generate.Ladder(x, i, all_sprites), ladders)
                    ladders.add(generate.Ladder(x, i + 1, all_sprites), ladders)
                    filled[(x, i)] = 'ladder'
                    filled[(x, i + 1)] = 'ladder'

        # монетки,
        for i in range(3):
            x = random.randint(1, 15)
            y = random.randrange(0, 6, 2)
            if (x, y) not in filled.keys():
                moneys.add(generate.Money(x, y, all_sprites), moneys)
                filled[(x, y)] = 'money'

        # и блоки
        for i in range(1, 8, 2):
            for j in range(16):
                if (j, i) not in filled.keys():
                    blocks.add(generate.Blocks(j, i, all_sprites), blocks)
                    filled[(j, i)] = 'block'

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
                        if level[y][x] == '1':
                            blocks.add(generate.Blocks(x, y, all_sprites), blocks)
                            filled[(x, y)] = 'block'
                        elif level[y][x] == '2':
                            ladders.add(generate.Ladder(x, y, all_sprites), ladders)
                            filled[(x, y)] = 'ladder'
                        elif level[y][x] == '3':
                            moneys.add(generate.Money(x, y, all_sprites), moneys)
                            filled[(x, y)] = 'money'
                running = False
            except IndexError:
                print('Нажмите корректную клавишу')

    # под конец создадим игрока
    player = generate.Player(all_sprites)

    # и заполним остаточные значения в filled значениями air
    for i in range(1, 16):
        for j in range(1, 7):
            try:
                filled[(i, j)]
            except KeyError:
                filled[(i, j)] = 'air'
    start_time = timeit.default_timer()
    running = True
    while running:
        for event in pygame.event.get():
            # Проверка на нажатие клавиш движения
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and filled[player_cords[0] // 50 + 1, player_cords[1] // 50] != 'block':
                    player.rect.left += dist
                    player_cords[0] += dist
                elif event.key == pygame.K_LEFT and filled[player_cords[0] // 50 - 1, player_cords[1] // 50] != 'block':
                    player.rect.left -= dist
                    player_cords[0] -= dist
                elif (event.key == pygame.K_DOWN and
                      filled[player_cords[0] // 50, player_cords[1] // 50 + 1] == 'ladder'):
                    player.rect.top += dist
                    player_cords[1] += dist
                elif event.key == pygame.K_UP and pygame.sprite.spritecollideany(player, ladders):
                    player.rect.top -= dist
                    player_cords[1] -= dist
            # Проверка на выход из игры
            elif event.type == pygame.QUIT:
                running = False

        if pygame.sprite.spritecollideany(player, moneys):
            money = pygame.sprite.spritecollide(player, moneys, True)[0]
        if not moneys:
            final_screen(timeit.default_timer() - start_time)

        screen.fill((0, 0, 0), (5, 5, screen.get_size()[0] - 10, screen.get_size()[1] - 10))
        board.render(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
