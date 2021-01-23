import pygame
import random


class Board:
    def __init__(self, width, height, surface):
        self.width = width
        self.height = height
        self.board = [[0 for i in range(width)] for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.border = 1
        self.surface = surface

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                pygame.draw.rect(self.surface, pygame.Color('white'),
                                 [self.left + self.cell_size * j, self.top + self.cell_size * i,
                                  self.cell_size, self.cell_size], self.border)
                if cell == 1:
                    pygame.draw.rect(self.surface, pygame.Color('green'),
                                     [self.left + self.cell_size * j + self.border, self.top + self.cell_size * i + self.border,
                                      self.cell_size - self.border, self.cell_size - self.border])

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

    def on_click(self, cell_x_y):
        self.board[cell_x_y[1]][cell_x_y[0]] = (self.board[cell_x_y[1]][cell_x_y[0]] + 1) % 2


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра Жизнь')
    n = int(input('Укажите размер поля\n'))
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    board = Board(n, n, screen)
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