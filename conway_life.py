import sys
import random
import math
import pygame as pg
from collections import Counter

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Cell(pg.sprite.Sprite):
    """Cell object"""

    def __init__(self, screen, background, size, index, pos, alive):
        super().__init__()
        self.screen = screen
        self.background = background
        self.width, self.height = size
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.color = WHITE
        self.column, self.row = index
        self.x, self.y = pos
        self.alive = alive
        self.cells = {}

    def update(self):
        self.alive = self.verify_neighbours()
        if self.alive:
            self.color = WHITE
        else:
            self.color = BLACK
        pg.draw.rect(self.background, self.color, (self.x, self.y, self.width, self.height), 0)

    def verify_neighbours(self):
        # list of neighbours
        neighbours = [self.cells.get((self.column, self.row - 1), None),  # upper
                      self.cells.get((self.column - 1, self.row - 1), None),  # upper left
                      self.cells.get((self.column + 1, self.row - 1), None),  # upper right
                      self.cells.get((self.column + 1, self.row), None),  # right
                      self.cells.get((self.column - 1, self.row), None),  # left
                      self.cells.get((self.column, self.row + 1), None),  # bottom
                      self.cells.get((self.column - 1, self.row + 1), None),  # bottom left
                      self.cells.get((self.column + 1, self.row + 1), None)]  # bottom right
        neighbours_status = [x.alive for x in neighbours if x is not None]
        neighbours_count = Counter(neighbours_status)
        if self.alive and (2 > neighbours_count[True] or neighbours_count[True] > 3):
            return False
        elif not self.alive and neighbours_count[True] == 3:
            return True
        else:
            return False


def main():
    pg.init()  # initialize pygame
    screen = pg.display.set_mode((800, 645))
    pg.display.set_caption("Conway's Game of Life")
    background = pg.Surface(screen.get_size())

    clock = pg.time.Clock()
    fps = 25

    # instantiate cells
    cells = pg.sprite.Group()
    width, height = screen.get_size()
    gcd = math.gcd(width, height)
    columns = width // gcd
    rows = height // gcd
    cell_width = width / columns
    cell_height = height / rows
    cells_dict = {}
    half_column = columns // 2
    half_row = rows // 2
    initial_live_cells = [(half_column - 1, half_row), (half_column - 1, half_row + 1), (half_column, half_row - 1),
                          (half_column, half_row), (half_column + 1, half_row)]
    x = 0
    for i in range(columns):
        y = 0
        for j in range(rows):
            if (i, j) in initial_live_cells:
                cell = Cell(screen, background, (cell_width, cell_height), (i, j), (x, y), True)
            else:
                cell = Cell(screen, background, (cell_width, cell_height), (i, j), (x, y), False)
            cells.add(cell)
            cells_dict[(i, j)] = cell
            y += cell_height
        x += cell_width

    for cell in cells.sprites():
        cell.cells = cells_dict

    while True:
        clock.tick(fps)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        screen.blit(background, (0, 0))

        cells.update()
        cells.draw(screen)

        pg.display.flip()


if __name__ == '__main__':
    main()
