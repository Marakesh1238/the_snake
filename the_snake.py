# Стандартные библиотеки
import random

# Сторонние библиотеки
import pygame

# Локальные импорты
from pygame.locals import QUIT

# Инициализация PyGame:
pygame.init()

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Это базовый класс,от которого наследуются другие игровые объекты."""

    def __init__(
        self, position: tuple = (0, 0), body_color: tuple = None
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Заготовка метода для отрисовки объекта."""


def get_free_coordinates(
    snake_positions: set[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Получение списка свободных координат."""
    all_coordinates = set(
        (x * GRID_SIZE, y * GRID_SIZE)
        for y in range(GRID_HEIGHT)
        for x in range(GRID_WIDTH)
    )
    snake_positions_set = set(snake_positions)
    free_coordinates = list(all_coordinates - snake_positions_set)
    return free_coordinates


class Apple(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    """

    def __init__(self, free_coordinates: list[tuple[int, int]] = None) -> None:
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(free_coordinates)

    def randomize_position(
        self, free_coordinates: list[tuple[int, int]]
    ) -> None:
        """Обновление позиции яблока по списку свободных координат."""
        if free_coordinates:
            self.position = random.choice(free_coordinates)

    def draw(self) -> None:
        """Метод отрисовки объекта."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self) -> None:
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
        self.next_direction = None

    def move(self) -> None:
        """Метод обновления позиции."""
        self.last = self.positions[-1]
        head_position = self.get_head_position()
        new_head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self) -> None:
        """Метод draw класса Apple."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_position = self.get_head_position()
        head_rect = pygame.Rect(head_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple[int, int]:
        """Определение позиции головы."""
        return self.positions[0]

    def reset(self) -> None:
        """Метод сброса змейки в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object: Snake):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            if event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            if event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            if event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция содержит основной цикл игры,
    объекты яблока и змейки и поддерживает состояние игры.
    """
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    free_coordinates = get_free_coordinates(snake.positions)
    apple = Apple(free_coordinates)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(free_coordinates)

        if len(set(snake.positions)) != len(snake.positions):
            snake.reset()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
