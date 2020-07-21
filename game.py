
import random
import pygame as pg
import copy
import sys
pg.init()
GRID_SIZE = (20, 20)
SCREEN_SIZE = (800, 600)
screen = pg.display.set_mode(SCREEN_SIZE)
pg.display.set_caption('Snake')

clock = pg.time.Clock()


class Fruit(pg.Rect):
    def pick_random_loc(self):
        w, h = pg.display.get_surface().get_size()
        g_w, g_h = GRID_SIZE
        self.x, self.y = random.randint(0,
                                        w // g_w) * (g_w - 1), random.randint(0, h // g_h) * (g_h-1)


class Snake(pg.Rect):
    def __init__(self, pos, size):
        super(Snake, self).__init__(pos, size)
        self.dir = (1, 0)
        self.tail = []

    def change_dir(self, new_dir):
        if self._is_not_opposite_dir(new_dir):
            self.dir = new_dir

    def add_tail(self):
        self.tail.append([self.x, self.y])

    def draw_tail(self, screen):
        for part in self.tail:
            x, y = part
            pg.draw.rect(screen, SNAKE_COLOR, pg.Rect((x, y), GRID_SIZE))

    def update(self):
        for i in range(len(self.tail) - 1):
            self.tail[i] = copy.deepcopy(self.tail[i + 1])
        if len(self.tail):
            self.tail[len(self.tail)-1] = [self.x, self.y]

        dir_x, dir_y = self.dir
        size_x, size_y = self.size
        move_x, move_y = dir_x * size_x, dir_y * size_y

        self.move_ip(int(move_x), int(move_y))

    def _is_not_opposite_dir(self, new_dir):
        dir_x, dir_y = self.dir
        new_dir_x, new_dir_y = new_dir
        if dir_x + new_dir_x == 0 or dir_y + new_dir_y == 0:
            return False
        return True


BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SNAKE_HEAD_COLOR = (0, 0, 255)
FRUIT_COLOR = (255, 0, 0)

snake = Snake((200, 200), GRID_SIZE)
fruit = Fruit((0, 0), GRID_SIZE)
fruit.pick_random_loc()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
            break
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                snake.change_dir((0, -1))
            if event.key == pg.K_s:
                snake.change_dir((0, 1))
            if event.key == pg.K_a:
                snake.change_dir((-1, 0))
            if event.key == pg.K_d:
                snake.change_dir((1, 0))

    screen.fill(BACKGROUND_COLOR)
    if snake.colliderect(fruit):
        fruit.pick_random_loc()
        snake.add_tail()
    snake.update()

    if not snake.colliderect(pg.Rect((0, 0), SCREEN_SIZE)):
        pg.quit()
        sys.exit(0)

    if snake.collidelistall([pg.Rect((part[0], part[1]), GRID_SIZE) for part in snake.tail]):

        pg.quit()
        sys.exit(0)
    pg.draw.rect(screen, SNAKE_HEAD_COLOR, snake)
    snake.draw_tail(screen)
    pg.draw.rect(screen, FRUIT_COLOR, fruit)
    pg.display.flip()
    clock.tick(35)

pg.quit()
sys.exit(0)
