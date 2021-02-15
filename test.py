import pygame as pg
from pygame.math import Vector2
import os
import sys
import math

BALL_RADIUS = 20
FIRST_BALL_X = 600
FIRST_BALL_Y = 250
COLLIDE_LOSS = 0.2
FRICTION_COEF = 0.1
FPS = 30
pg.init()
size = width, height = 900, 500
screen = pg.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Hole(pg.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__(all_sprites)
        self.add(holes)
        self.image = pg.Surface([30, 30])
        self.image.fill(pg.Color('black'))
        self.rect = self.image.get_rect(topleft=(x1, y1))


class Stick(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = load_image('stick.png')
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.angle = 0
        self.pos = Vector2((pos[0] - self.rect.w // 2, pos[1]))
        self.offset = Vector2(0, 0)
        self.sweep = 0

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.angle = (self.angle - 3) % 360
        elif keys[pg.K_d]:
            self.angle = (self.angle + 3) % 360
        elif keys[pg.K_w]:
            self.sweep += 1
        elif keys[pg.K_s]:
            self.sweep -= 1

        #print(self.angle)
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        self.sweep = max(min(10, self.sweep), 0)
        self.offset = Vector2(-10 * self.sweep, 0).rotate(self.angle)
        self.pos = Vector2((pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]))
        x, y, w, h = self.image.get_rect(center=self.pos + self.offset)
        #print(x, y, w, h)
        self.rect = pg.Rect(x, y, w, h)
        pg.draw.rect(screen, pg.Color('yellow'), (x, y, w, h), 1)
        #
        # if self.angle < 90:
        #     pg.draw.rect(screen, pg.Color('yellow'), (x, y, w + abs(self.offset[0]), h + abs(self.offset[1])), 1)
        #     self.rect = pg.Rect(x, y, w + abs(self.offset[0]), h + abs(self.offset[1]))
        # elif self.angle < 180:
        #     pg.draw.rect(screen, pg.Color('yellow'), (x - abs(self.offset[0]), y, w , h + abs(self.offset[1])), 1)
        #     self.rect = pg.Rect(x - abs(self.offset[0]), y, w, h + abs(self.offset[1]))




class Ball(pg.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.add(balls)
        self.radius = radius
        self.image = pg.Surface((2 * radius, 2 * radius), pg.SRCALPHA, 32)
        pg.draw.circle(self.image, pg.Color("white"), (radius, radius), radius)
        pg.draw.circle(self.image, pg.Color("black"), (radius, radius), radius, 1)
        self.rect = pg.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = self.vy = 0


    def update(self):
        if pg.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pg.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        if len(col_list:=pg.sprite.spritecollide(self, balls, False)) > 1:
            print(1)
            temp_vx = temp_vy = 0
            for el in col_list:
                if el is not self:
                # el.vy = -max(abs(el.vy), abs(self.vy))
                # el.vx = -max(abs(el.vx), abs(self.vx))
                    temp_vy += el.vy
                    temp_vx += el.vx
                    el.vx = self.vx + el.vx - COLLIDE_LOSS
                    el.vy = self.vy + el.vy - COLLIDE_LOSS
            self.vy += temp_vy - COLLIDE_LOSS
            self.vx += temp_vx - COLLIDE_LOSS
        if pg.sprite.spritecollideany(self, holes):
            print(self.rect.topleft)
            self.kill()
        if abs(self.vx) <= FRICTION_COEF:
            self.vx = 0
        else:
            self.vx = self.vx - FRICTION_COEF if self.vx > 0 else self.vx - FRICTION_COEF
        if abs(self.vy) <= FRICTION_COEF:
            self.vy = 0
        else:
            self.vy = self.vy - FRICTION_COEF if self.vy > 0 else self.vy - FRICTION_COEF

        self.rect = self.rect.move(self.vx, self.vy)

class Border(pg.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pg.Surface([1, y2 - y1])
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pg.Surface([x2 - x1, 1])
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)



class Game:
    def __init__(self, players):
        self.round = 0
        self.players = players
        self.score = [0] * 5

    def create(self):
        Border(5, 5, width - 5, 5)
        Border(5, height - 5, width - 5, height - 5)
        Border(5, 5, 5, height - 5)
        Border(width - 5, 5, width - 5, height - 5)
        koef_y = 0
        for row in range(5):
            koef_y = -BALL_RADIUS * row - BALL_RADIUS // 2
            for j in range(row + 1):
                Ball(BALL_RADIUS, FIRST_BALL_X + (BALL_RADIUS * 2 * row), FIRST_BALL_Y + koef_y)
                koef_y += BALL_RADIUS * 2 + 2
        Ball(BALL_RADIUS, FIRST_BALL_X - 350, FIRST_BALL_Y - BALL_RADIUS // 2)
        Hole(0, 0)
        Hole(width - 30, 0)
        Hole(0, height - 30)
        Hole(width - 30, height - 30)

    def show_start_screen(self):
        pass

    def hit(self):
        print('sweep', stick.sweep)

        temp = stick.sweep
        stick.sweep = 0
        stick.update()
        if col_list := pg.sprite.spritecollide(stick, balls, False):
            print(col_list)

            col_list[0].vx = math.cos(math.radians(stick.angle)) * temp
            col_list[0].vy = math.sin(math.radians(stick.angle)) * temp
            print(temp)
            print(math.cos(math.radians(stick.angle)), math.sin(math.radians(stick.angle)))
            print(col_list[0].vx, col_list[0].vy)
            print()






if __name__ == '__main__':
    pg.display.set_caption('Бильярд')
    game = Game(players=2)
    game.show_start_screen()

    all_sprites = pg.sprite.Group()
    horizontal_borders = pg.sprite.Group()
    vertical_borders = pg.sprite.Group()
    holes = pg.sprite.Group()
    balls = pg.sprite.Group()
    stick = Stick(pg.mouse.get_pos())
    player = pg.sprite.Group(stick)

    game.create()
    running = True
    clock = pg.time.Clock()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    game.hit()
        screen.fill((0, 128, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        player.draw(screen)
        player.update()
        pg.display.flip()
        clock.tick(FPS)
    pg.quit()