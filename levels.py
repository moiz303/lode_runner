import pygame
import os
import generate
import main


screen = pygame.display.set_mode((810, 410))


def load_level(filename) -> list:
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('0')
    return list(map(lambda i: i.ljust(max_width, '0'), level_map))


def take_level() -> int:
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
                main.terminate()
            elif event.type == pygame.KEYDOWN:
                return pygame.key.get_pressed().index(True)
        pygame.display.flip()
