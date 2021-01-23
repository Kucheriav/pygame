import pygame
import random

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[random.randint(0, 1) for i in range(width)] for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.border = 1
        self.counter = 0

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                pygame.draw.rect(screen, pygame.Color('white'),
                                 [self.left + self.cell_size * j, self.top + self.cell_size * i,
                                  self.cell_size, self.cell_size], self.border)
                if self.board[i][j] == 0:
                    pygame.draw.circle(screen, pygame.Color('blue'), (self.left + self.cell_size * j + self.cell_size / 2,
                                                                     self.top + self.cell_size * i + self.cell_size / 2),
                                                                        self.cell_size / 2 - 2)

                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, pygame.Color('red'), (self.left + self.cell_size * j + self.cell_size / 2,
                                                                     self.top + self.cell_size * i + self.cell_size / 2),
                                                                        self.cell_size / 2 - 2)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def get_cell(self, pos):
        column = (pos[0] - self.left) // self.cell_size
        row = (pos[1] - self.top) // self.cell_size
        if 0 <= row < len(self.board) and 0 <= column < len(self.board[0]):
            return column, row
        return None

    def on_click(self, cell):
        if self.counter == self.board[cell[1]][cell[0]]:
            self.line_invert(cell)
            self.counter = (self.counter + 1) % 2

    def invert_color(self, cell):
        # cell - (x, y) but board - [y][x]
        self.board[cell[1]][cell[0]] = (self.board[cell[1]][cell[0]] + 1) % 2

    def line_invert(self, cell):
        for i in range(self.width):
            self.invert_color((i, cell[1]))
        for j in range(self.height):
            self.invert_color((cell[0], j))
        self.invert_color(cell)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Недореверси')
    n = int(input('Укажите размер поля\n'))
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    board = Board(n, n)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()
    pygame.quit()