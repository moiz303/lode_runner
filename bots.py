from generate import Game, load_image


class Bot(Game):
    def __init__(self, field, bot_cords):
        super().__init__()
        self.selected_cell = bot_cords
        self.ticks = 0
        self.path = []
        self.board = field

    # cell - кортеж (x, y)
    def get_cell(self, cords):
        """Из координат делаем клетку"""
        cell_x = (cords[0] - self.left) // self.cell_size
        cell_y = (cords[1] + 1 - self.top) // self.cell_size
        return cell_x, cell_y

    def get_click(self, cords, spr):
        """Находим клетку по клику"""
        cell = self.get_cell(cords)
        if cell and cell < (self.width, self.height):
            return self.on_click(cell, spr)

    def on_click(self, cell, spr):
        """Собственно, поиск пути и запуск по нему бота"""
        x, y = cell
        x2, y2 = self.selected_cell
        if self.has_path(x2, y2, x, y):
            self.path = self.get_path(x2, y2, x, y)
        self.go_bot(self.path, spr)

    def get_distances(self, start):
        """Ядро поиска пути -
        поиск расстояний между двумя точками"""
        v = [(start[0], start[1])]
        # словарь расстояний
        d = {(start[0], start[1]): 0}
        while len(v) > 0:
            x, y = v.pop(0)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                        continue
                    if self.board[y + dy][x + dx] == 0:
                        dn = d.get((x + dx, y + dy), -1)
                        if dn == -1:
                            d[(x + dx, y + dy)] = d[(x, y)] + 1
                            v.append((x + dx, y + dy))
        return d

    def get_path(self, x1, y1, x2, y2):
        """Получаем расстояния и говорим, можем ли пройти
        и еслида, то как"""
        d = self.get_distances((x1, y1))
        v = x2, y2
        path = [v]
        while v != (x1, y1):
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx * dy != 0 or (dx == 0 and dy == 0):
                        continue
                    x = v[0]
                    y = v[1]
                    if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                        continue
                    if d.get((x + dx, y + dy), -100) == d[v] - 1:
                        v = (x + dx, y + dy)
                        path.append(v)
        path.reverse()
        return path[1:]

    def update(self):
        """Обновляем путь с задержкой"""
        if self.ticks == 15:
            if len(self.path) > 0:
                x, y = self.path.pop(0)
                self.board[y][x] = 1
                self.board[self.selected_cell[1]][self.selected_cell[0]] = 0
                self.selected_cell = x, y
                if len(self.path) == 0:
                    return
            self.ticks = 0
        self.ticks += 1

    def has_path(self, x1, y1, x2, y2):
        """Простая проверка на наличие пути"""
        d = self.get_distances((x2, y2))
        dist = d.get((x1, y1), -1)
        return dist >= 0

    def go_bot(self, path, sprite):
        """Логика передвижения бота"""
        try:
            next_x, next_y = path[0]
            if next_x == sprite.rect.x // 50:
                if next_y < sprite.rect.y // 50:
                    sprite.rect.top -= 50
                else:
                    sprite.rect.top += 50
            else:
                if next_x < sprite.rect.x // 50:
                    sprite.rect.left -= 50
                    sprite.cut_sheet(load_image('bot_left_animations.xcf'), 3, 1)
                    sprite.update()
                else:
                    sprite.rect.left += 50
                    sprite.cut_sheet(load_image('bot_right_animations.xcf'), 3, 1)
                    sprite.update()
        except IndexError:
            return
