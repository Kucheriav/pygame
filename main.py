import pygame
import os
import sys


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


MAPS_DIR = 'maps'
DATA_DIR = 'data'
FPS = 10
pygame.init()
pygame.display.set_caption('Перемещение героя')
size = WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode(size)

def load_level(filename):
    filename = f"{MAPS_DIR}/{filename}"
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join(DATA_DIR, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mar.png')
tile_width = tile_height = 50


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        print(target.rect.x, target.rect.w )
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.type = tile_type
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Labyrinth:
    def __init__(self):
        self.level = None
        self.tiles_x = self.tiles_y = None

    def load_level(self, level_filename):
        self.level = list()
        try:
            level = load_level(level_filename)
        except Exception as e:
            print('Ошибка:', e)
            terminate()
        for y in range(len(level)):
            self.level.append([])
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    self.level[y].append(Tile('empty', x, y))
                elif level[y][x] == '#':
                    self.level[y].append(Tile('wall', x, y))
                elif level[y][x] == '@':
                    self.level[y].append(Tile('empty', x, y))
                    new_player = Player(x, y)
        self.tiles_x, self.tiles_y = x + 1, y + 1
        return new_player

    def get_tile_type(self, x, y):
        if 0 <= x < self.tiles_x and 0 <= y < self.tiles_y:
            return self.level[y][x].type
        return False


class Player(pygame.sprite.Sprite):
    def __init__(self, tile_x, tile_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * tile_x + 15, tile_height * tile_y + 5)
        self.tile_x = tile_x
        self.tile_y = tile_y

    def move(self, args):
        next_x, next_y = self.tile_x, self.tile_y
        print('old', self.rect, self.tile_x, self.tile_y)
        if args.key == pygame.K_RIGHT:
            next_x += 1
        if args.key == pygame.K_LEFT:
            next_x -= 1
        if args.key == pygame.K_UP:
            next_y -= 1
        if args.key == pygame.K_DOWN:
            next_y += 1
        if next_tile := labyrinth.get_tile_type(next_x, next_y):
            if next_tile == 'empty':
                self.rect = self.image.get_rect().move(tile_width * next_x + 15, tile_height * next_y + 5)
                self.tile_x, self.tile_y = next_x, next_y
                print('new', self.rect, self.tile_x, self.tile_y)
        print()

if __name__ == '__main__':
    labyrinth = Labyrinth()
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    #file = input('Введите название уровня\n')
    file = 'level3'
    player = labyrinth.load_level(f'{file}.txt')
    running = True
    clock = pygame.time.Clock()
    start_screen()
    camera = Camera()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.move(event)
        screen.fill((0, 0, 0))

        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)




        tiles_group.draw(screen)
        player_group.draw(screen)
        #all_sprites.update()

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
