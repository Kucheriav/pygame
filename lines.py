from board import Board
import pygame
import copy


class Lines(Board):
    def __init__(self, width, height, surface):
        super().__init__(width, height, surface, default=-1)
        self.start_point = None
        self.finish_point = None
        self.movement_animation = False
        self.iterator = None

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
        if self.board[cell_x_y[1]][cell_x_y[0]] == -1 and not self.start_point:
            self.board[cell_x_y[1]][cell_x_y[0]] = 'blue'
        elif self.board[cell_x_y[1]][cell_x_y[0]] == 'blue' and not self.start_point:
            self.board[cell_x_y[1]][cell_x_y[0]] = 'red'
            self.start_point = cell_x_y[0], cell_x_y[1]
        elif self.board[cell_x_y[1]][cell_x_y[0]] == 'red':
            self.board[cell_x_y[1]][cell_x_y[0]] = 'blue'
            self.start_point = False
        elif self.board[cell_x_y[1]][cell_x_y[0]] == -1 and self.start_point:
            self.finish_point = cell_x_y[0], cell_x_y[1]
            result = self.has_path(*self.start_point, *self.finish_point)
            if result:
                route = self.find_route(result)
                self.iterator = self.animate_step_from_route(route)
                self.movement_animation = True

    def has_path(self, x1, y1, x2, y2):
        T = 0
        new_wave = [(x1, y1)]
        temp_board = copy.deepcopy(self.board)
        while True:
            old_wave = new_wave[:]
            new_wave = list()
            T += 1
            if not old_wave:
                return False
            for point in old_wave:
                x = point[0]
                y = point[1]
                for i, j in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
                    if 0 <= i < len(temp_board[0]) and 0 <= j < len(temp_board):
                        if temp_board[j][i] not in ('blue', 'red'):
                            if temp_board[j][i] == -1:
                                temp_board[j][i] = T
                                new_wave.append((i, j))
                                if (i, j) == (x2, y2):
                                    return temp_board

    def find_route(self, board):
        route_points = [self.finish_point]
        while True:
            x, y = route_points[-1]
            ways = list()
            for i, j in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
                if 0 <= i < len(board[0]) and 0 <= j < len(board):
                    if (i, j) == self.start_point:
                        route_points.append((i, j))
                        return route_points
                    if (i, j) not in route_points and board[j][i] != -1 and board[j][i] not in ('blue', 'red'):
                        ways.append([board[j][i], (i, j)])
            ways.sort(key=lambda x: (x[0], x[1][0]))
            choice = ways[0][1]
            route_points.append(choice)

    def animate_step_from_route(self, route):
        route.reverse()
        for i in range(1, len(route)):
            x = route[i][0]
            y = route[i][1]
            self.board[y][x] = 'red'
            old_x = route[i - 1][0]
            old_y = route[i - 1][1]
            self.board[old_y][old_x] = -1
            yield
        self.movement_animation = False


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Полилинии')
    n = int(input('Укажите размер поля\n'))
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    game = Lines(n, n, screen)
    fps = 5
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
        if game.movement_animation:
            try:
                next(game.iterator)
            except Exception:
                game.movement_animation = False
                game.start_point = game.finish_point
        game.render()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()