import generate


def load_level(filename):
    filename = "levels/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('0')
    return list(map(lambda i: i.ljust(max_width, '0'), level_map))


def return_all(symbol, x, y, group):
    if symbol == '1':
        return generate.Blocks(x, y, group)
    elif symbol == '2':
        return generate.Ladder(x, y, group)
    elif symbol == '3':
        return generate.Money(x, y, group)
