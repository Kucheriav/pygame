from board import Board
import pygame
import copy


class Life(Board):
    def __init__(self, width, height, surface):
        super().__init__(width, height, surface, 0)
        self.simulation = False

    def next_move(self):
        next_board = copy.deepcopy(self.board)
        for y, row in enumerate(next_board):
            for x, cell in enumerate(row):
                s = 0
                for j in range(y - 1, y + 2):
                    s += sum(self.board[j % len(self.board)][i % len(self.board[y])] for i in range(x - 1, x + 2))
                s = s - 1 if cell else s
                if not cell and s == 3:
                    next_board[y][x] = 1
                elif cell and (s == 2 or s == 3):
                    next_board[y][x] = 1
                else:
                    next_board[y][x] = 0
        self.board = copy.deepcopy(next_board)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Игра Жизнь')
    n = int(input('Укажите размер поля\n'))
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    game = Life(n, n, screen)
    fps = 15
    speed_add_on_wheel = 5
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game.simulation:
                if event.button == 1:
                    game.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.simulation = False if game.simulation else True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    game.simulation = False if game.simulation else True
            if event.type == pygame.MOUSEWHEEL:
                fps += speed_add_on_wheel * event.y
                fps = 1 if fps < 1 else fps
        screen.fill((0, 0, 0))
        if game.simulation:
            game.next_move()
        game.render()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()