import pygame
import random


class Board:
    def __init__(self, width, height, surface, default):
        self.width = width
        self.height = height
        self.board = [[default for i in range(width)] for _ in range(height)]
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
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                pygame.draw.rect(self.surface, pygame.Color('white'),
                                 [self.left + self.cell_size * j, self.top + self.cell_size * i,
                                  self.cell_size, self.cell_size], self.border)
                if self.board[i][j] == 'blue':
                    pygame.draw.circle(self.surface, pygame.Color('blue'),
                                       (self.left + self.cell_size * j + self.cell_size / 2,
                                        self.top + self.cell_size * i + self.cell_size / 2),
                                       self.cell_size / 2 - 2)
                elif self.board[i][j] == 'red':
                    pygame.draw.circle(self.surface, pygame.Color('red'),
                                       (self.left + self.cell_size * j + self.cell_size / 2,
                                        self.top + self.cell_size * i + self.cell_size / 2),
                                       self.cell_size / 2 - 2)
                else:
                    font = pygame.font.Font(None, 40)
                    text = font.render(str(self.board[i][j]), True, (100, 255, 100))
                    text_x = self.left + self.cell_size * j + self.border
                    text_y = self.top + self.cell_size * i + self.border
                    self.surface.blit(text, (text_x, text_y))
