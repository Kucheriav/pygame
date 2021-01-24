from board import Board
import pygame


class Lines(Board):
    def __init__(self, wigth, height, surface, default=-1):
        super().__init__(wigth, height, surface, default=-1)
        self.start_point = None
        self.finish_point = None

        self.emulate_find_way = False
        self.emulate_T = 0
        self.emulate_new_wave = list()
        self.emulate_old_wave = list()


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
            #self.find_way()
            self.emulate_find_way = True
            self.emulate_new_wave.append(self.start_point)



    def find_way(self):
        self.emulate_old_wave = self.emulate_new_wave[:]
        self.emulate_new_wave = list()
        self.emulate_T += 1
        if not self.emulate_old_wave:
            print('No way')
            self.emulate_find_way = False
            return
        for point in self.emulate_old_wave:
            x = point[0]
            y = point[1]
            for i, j in [(x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y)]:
                if 0 <= i < len(self.board[0]) and 0 <= j < len(self.board):
                    if self.board[j][i] not in ('blue', 'red'):
                        if self.board[j][i] == -1:
                        #if (i, j) not in self.emulate_old_wave and (i, j) not in self.emulate_new_wave:
                            self.board[j][i] = self.emulate_T
                            self.emulate_new_wave.append((i, j))
                            if (i, j) == self.finish_point:
                                print(self.board[j][i])
                                self.emulate_find_way = False
                                return




if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Линеечки')
    n = int(input('Укажите размер поля\n'))
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    game = Lines(n, n, screen)
    fps = 1
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
        if game.emulate_find_way:
            game.find_way()
        game.render()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()