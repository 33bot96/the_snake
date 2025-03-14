from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
directions: list[tuple[int, int]] = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Исползуется как родительский класс для
    игровых объектов:
    """

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Прорисовка объекта."""


class Apple(GameObject):
    """Класс игрового объекта 'яблоко':"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color: tuple[int, int, int] = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """
        Метод случайного поялвения игрового
        объекта 'яблоко' на игровом поле.
        """
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Прорисовка игрового объекта 'яблоко'."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс игрового объекта 'змейка':"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color: tuple[int, int, int] = SNAKE_COLOR
        self.direction = choice(directions)  # Cлучайное направление змейки^_^.
        self.next_direction = None
        self.positions = [self.position]
        self.last = None
        self.lenght = 1

    def get_head_position(self):
        """Возвращает позицию первой клетки 'змейки'."""
        return self.positions[0]

    def move(self):
        """Класс отвечающий за все что касается движения 'змейки':"""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.lenght:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Отвечает за направление движения."""
        if self.next_direction:  # это то что я должен был сделать?
            self.direction, self.next_direction = (
                self.next_direction, None
            )  # 40ка минутная лекция по тернарным операторам коту под хвост(

    def draw(self):
        """Отвечает за прорисовку."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Отвечает за сборс змейки к стандартому состоянию"""
        self.direction = choice(directions)
        self.next_direction = None
        self.positions = [self.position]
        self.last = None
        self.lenght = 1


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основаня функия запуска игры."""
    pygame.init()  # Инстализация 'pygame'.
    apple = Apple()  # Инстализация класса 'Яблоко'.
    snake = Snake()  # Инстализация класса 'Змейка'.

    while True:
        clock.tick(SPEED)  # Ограничение частоты обновления экрана.
        handle_keys(snake)  # Обработка нажатий клавиш.
        snake.update_direction()  # Обновление направления змейки.
        snake.move()  # Движение змейки.

        # Проверка, съела ли змейка яблоко.
        if snake.get_head_position() == apple.position:
            snake.lenght += 1  # Увеличиваем длину змейки.
            apple.randomize_position()  # Перемещаем яблоко на новую позицию.

        # Проверка на столкновение змейки с самой собой.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()  # Сбрасываем змейку в начальное состояние.

        # Отрисовка игрового поля.
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очистка экрана.
        apple.draw()  # Отрисовка яблока.
        snake.draw()  # Отрисовка змейки.

        pygame.display.update()  # Обновление экрана.


if __name__ == '__main__':
    main()
