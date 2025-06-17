import pygame
import random
import sys

# Константы
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
FPS = 10

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (CELL_SIZE, 0)  # Начальное движение вправо
        self.grow_snake = False

    def move(self):
        head_x, head_y = self.body[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)
        self.body.insert(0, new_head)
        if not self.grow_snake:
            self.body.pop()
        else:
            self.grow_snake = False

    def change_direction(self, new_dir):
        # Запретить движение в обратную сторону
        opp_dir = (-self.direction[0], -self.direction[1])
        if new_dir != opp_dir:
            self.direction = new_dir

    def grow(self):
        self.grow_snake = True

    def collides_with_self(self):
        return self.body[0] in self.body[1:]

    def collides_with_wall(self):
        head_x, head_y = self.body[0]
        return (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT)

class Food:
    def __init__(self, snake):
        self.position = self.random_position(snake)

    def random_position(self, snake):
        while True:
            x = random.randrange(0, WIDTH, CELL_SIZE)
            y = random.randrange(0, HEIGHT, CELL_SIZE)
            if (x, y) not in snake.body:
                return (x, y)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Змейка на Python (pygame)')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 25)
        self.snake = Snake()
        self.food = Food(self.snake)
        self.score = 0
        self.running = True

    def draw_grid(self):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, (40, 40, 40), (0, y), (WIDTH, y))

    def draw_snake(self):
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction((CELL_SIZE, 0))

    def update(self):
        self.snake.move()
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food = Food(self.snake)
            self.score += 1

        if self.snake.collides_with_self() or self.snake.collides_with_wall():
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.food.draw(self.screen)
        self.draw_snake()
        score_text = self.font.render(f"Счет: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def show_game_over(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render(f"Игра окончена! Счет: {self.score}", True, RED)
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(3000)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        self.show_game_over()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
