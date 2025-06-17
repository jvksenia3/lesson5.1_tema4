import pygame
import sys

# --- Константы ---
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 7
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# --- Классы ---
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 0

    def move(self):
        self.rect.y += self.speed
        # Защита от выхода за границы экрана
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от верхней и нижней границы
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def draw(self, surface):
        pygame.draw.ellipse(surface, WHITE, self.rect)

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x *= -1

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Пин-Понг на Python (pygame)')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 36)

        self.left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.score_left = 0
        self.score_right = 0

    def draw(self):
        self.screen.fill(BLACK)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        # Рисуем счет
        score_text = self.font.render(f"{self.score_left} : {self.score_right}", True, WHITE)
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        pygame.display.flip()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Левая ракетка (W/S)
        if keys[pygame.K_w]:
            self.left_paddle.speed = -PADDLE_SPEED
        elif keys[pygame.K_s]:
            self.left_paddle.speed = PADDLE_SPEED
        else:
            self.left_paddle.speed = 0
        # Правая ракетка (Up/Down)
        if keys[pygame.K_UP]:
            self.right_paddle.speed = -PADDLE_SPEED

        elif keys[pygame.K_DOWN]:
            self.right_paddle.speed = PADDLE_SPEED
        else:
            self.right_paddle.speed = 0

    def update(self):
        self.left_paddle.move()
        self.right_paddle.move()
        self.ball.move()

        # Проверка столкновения с ракетками
        if self.ball.rect.colliderect(self.left_paddle.rect) and self.ball.speed_x < 0:
            self.ball.speed_x *= -1
        if self.ball.rect.colliderect(self.right_paddle.rect) and self.ball.speed_x > 0:
            self.ball.speed_x *= -1

        # Проверка гола
        if self.ball.rect.left <= 0:
            self.score_right += 1
            self.ball.reset()
        if self.ball.rect.right >= WIDTH:
            self.score_left += 1
            self.ball.reset()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

if __name__ == '__main__':
    game = Game()
    game.run()
