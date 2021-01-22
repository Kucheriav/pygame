import pygame
import math

class Fan:
    def __init__(self):
        self.center_coor = (size[0] // 2, size[1] // 2)
        self.r = 10
        self.color = pygame.Color('white')
        self.surface = pygame.Surface(screen.get_size())
        pygame.draw.circle(self.surface, self.color, self.center_coor, self.r)
        self.wings = []
        self.rotation_index = 0
        for i in range(3):
            self.wings.append(Wing(self.center_coor))

    def update(self):
        pygame.draw.circle(self.surface, self.color, self.center_coor, self.r)
        for i, wing in enumerate(self.wings):
            wing.adjust_to_angle(i * 120 + v)
            pygame.draw.polygon(self.surface, self.color, wing.shape)
        screen.blit(self.surface, (0, 0))

    def rotate(self):
        angle = self.rotation_index * 3.14 / 180
        for i, wing in enumerate(self.wings):
            wing.adjust_to_angle(angle)
        self.rotation_index += 3



class Wing:
    def __init__(self, center, hypotenuza=70, inner_angle=60):
        self.c_x, self.c_y = center[0], center[1]
        self.a_x = self.c_x - hypotenuza * math.cos(math.radians(inner_angle))
        self.a_y = self.c_y - hypotenuza * math.sin(math.radians(inner_angle))
        self.b_x = self.c_x + hypotenuza * math.cos(math.radians(inner_angle))
        self.b_y = self.c_y - hypotenuza * math.sin(math.radians(inner_angle))
        self.shape = [(self.c_x, self.c_y), (self.a_x, self.a_y), (self.b_x, self.b_y)]

    def adjust_to_angle(self, angle):
        for i in range(1, 3):
            x = self.c_x + (self.shape[i][0] - self.c_x) * math.cos(math.radians(angle)) + (self.c_y - self.shape[i][1]) * math.sin(math.radians(angle))
            y = self.c_y + (self.shape[i][0] - self.c_x) * math.sin(math.radians(angle)) + (self.shape[i][1] - self.c_y) * math.cos(math.radians(angle))
            self.shape[i] = (x, y)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Вентилятор')
    size = width, height = 201, 201
    screen = pygame.display.set_mode(size)
    running = True
    clock = pygame.time.Clock()
    fps = 60
    v = 0
    fan = Fan()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    v += 3
                if event.button == 3:
                    v -= 3
        fan.update()
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()