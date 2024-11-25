from random import randint

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position, body_color):
        self.position = position
        self.body_color = body_color

    def draw():
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко на игровом поле."""

    body_color = (0, 0, 0)  # Красный цвет
    position = (0, 0)  # Позиция по умолчанию

    def __init__(self):
        """Создает объект яблока с начальным цветом."""
        self.body_color = (255, 0, 0)
        self.position = (0, 0)  # Задаём начальную позицию

    def randomize_position(self, snake_positions):
        """
        Выбирает случайную позицию для яблока, не совпадающую с телом змейки.
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in snake_positions:
                return new_position

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку."""

    length = 2
    body_color = (0, 255, 0)
    direction = RIGHT  # Направление по умолчанию (вправо)

    def __init__(self, positions, direction):
        """Инициализирует змейку с начальным положением и направлением."""
        self.positions = positions
        self.direction = direction
        self.next_direction = direction

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Двигает змейку в текущем направлении.
        """
        # Обновляем направление на новое, если оно задано
        if self.next_direction:
            self.direction = self.next_direction

        # Вычисляем новую позицию головы
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head_x = (head_x + delta_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + delta_y * GRID_SIZE) % SCREEN_HEIGHT

        new_head = (new_head_x, new_head_y)

        # Добавляем новую голову в начало списка
        self.positions.insert(0, new_head)

        # Удаляем последний элемент, если длина змейки не увеличилась
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.
        """
        return self.positions[0]

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # Центр экрана
        self.direction = (1, 0)  # Движение вправо
        self.next_direction = self.direction


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
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
    """Основная функция игры."""
    pygame.init()

    # Создаём экземпляры классов
    apple = Apple()
    snake = Snake(
        positions=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)],
        direction=RIGHT
    )

    # Генерируем первую позицию яблока
    apple.position = apple.randomize_position(snake.positions)

    while True:
        # Устанавливаем частоту обновления
        clock.tick(SPEED)

        # Обработка событий (нажатий клавиш)
        handle_keys(snake)

        # Перемещение змейки
        snake.move()

        # Проверка на столкновение с собой
        head_position = snake.get_head_position()
        if head_position in snake.positions[1:]:
            # Проверяем, находится ли голова в теле змейки

            pygame.quit()
            return

        # Проверка на съедание яблока
        if head_position == apple.position:
            snake.length += 1  # Увеличиваем длину змейки
            apple.position = apple.randomize_position(snake.positions)
            # Перемещаем яблоко

        # Отрисовка игрового поля, яблока и змейки
        screen.fill(BOARD_BACKGROUND_COLOR)  # Заливка фона
        apple.draw()
        snake.draw()

        # Обновление экрана
        pygame.display.flip()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key ==
# pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == (pygame.K_RIGHT and
#                                game_object.direction != LEFT
#                               ):
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
