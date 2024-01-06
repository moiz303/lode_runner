import pygame
from generate import Game


class Bot(Game):
    def __init__(self):
        super().__init__()
        self.selected_cell = None
        self.ticks = 0
        self.path = []

    def get_distances(self, start):
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
                    if self.board[x + dx][y + dy] != 'block':
                        dn = d.get((x + dx, y + dy), -1)
                        if dn == -1:
                            d[(x + dx, y + dy)] = d[(x, y)] + 1
                            v.append((x + dx, y + dy))
        return d

    def get_path(self, x1, y1, x2, y2):
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

    def updata(self):
        if self.ticks == 10:
            if len(self.path) > 0:
                x, y = self.path.pop(0)
                self.board[x][y] = 1
                self.board[self.selected_cell[0]][self.selected_cell[1]] = 0
                self.selected_cell = x, y
                if len(self.path) == 0:
                    self.selected_cell = None
            self.ticks = 0
        self.ticks += 1

    def has_path(self, x1, y1, x2, y2):
        d = self.get_distances((x1, y1))
        dist = d.get((x2, y2), -1)
        return dist >= 0


def go():
    pygame.init()
    clock = pygame.time.Clock()

    board = Bot()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        board.get_click()

        board.updata()
        pygame.display.flip()
        clock.tick(50)
    pygame.quit()


if __name__ == '__main__':
    go()
