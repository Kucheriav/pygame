from board import Board
import pygame
import random

class Minesweeper(Board):
    def __init__(self, width, height, surface, mines):
        super().__init__(width + 2, height + 2, surface, -1)
        self.simulation = False
        self.mines = mines
        self.plant_mines()

    def plant_mines(self):
        for i in range(mines):
            while True:
                x = random.randint(1, self.width - 2)
                y = random.randint(1, self.height - 2)
                if self.board[y][x] == -1:
                    self.board[y][x] = 10
                    break

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_cell(self, pos):
        column = (pos[0] - self.left) // self.cell_size
        row = (pos[1] - self.top) // self.cell_size
        if 1 <= row < len(self.board) - 1 and 1 <= column < len(self.board[0]) - 1:
            return column, row
        return None

    def on_click(self, cell_x_y):
        if self.board[cell_x_y[1]][cell_x_y[0]] == -1:
            self.open_cell(cell_x_y)

    def open_cell(self, cell):
        x = cell[0]
        y = cell[1]
        s = 0
        for j in range(y - 1, y + 2):
            for i in range(x - 1, x + 2):
                if self.board[j][i] == 10 and (x, y) != (i, j):
                    s += 1
        self.board[y][x] = s
        if self.board[y][x] == 0:
            for j in range(y - 1, y + 2):
                for i in range(x - 1, x + 2):
                    if 1 <= j < len(self.board) - 1 and 1 <= i < len(self.board[0]) - 1:
                        self.on_click((i, j))



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Дедушка Сапера')
    n = int(input('Укажите размер поля\n'))
    mines = int(input('Укажите количество мин\n'))
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    game = Minesweeper(n, n, screen, mines)
    fps = 30
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.get_click(event.pos)
        screen.fill((0, 0, 0))
        game.render()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()