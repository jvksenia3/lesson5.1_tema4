import pygame
import random
import sys

# --- Константы
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
ENEMY_SIZE = 40
ENEMY_SPAWN_TIME = 1000  # миллисекунд
PLAYER_SPEED = 0.4
PLAYER_FRICTION = 0.92
ENEMY_SPEED = 2

# --- Классы
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.vel = pygame.Vector2(0, 0)

    def update(self, keys):
        # Управление
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel.y += PLAYER_SPEED

        # Трение
        self.vel *= PLAYER_FRICTION

        # Движение
        self.rect.x += int(self.vel.x)
        self.rect.y += int(self.vel.y)

        # Ограничения экрана
        self.rect.x = max(0, min(WIDTH - PLAYER_SIZE, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - PLAYER_SIZE, self.rect.y))

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 120, 255), self.rect)

class Enemy:
    def __init__(self):
        # Враги появляются по краям экрана
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            self.rect = pygame.Rect(random.randint(0, WIDTH-ENEMY_SIZE), 0, ENEMY_SIZE, ENEMY_SIZE)
            angle = random.uniform(0.2, 2.9)
        elif edge == 'bottom':
            self.rect = pygame.Rect(random.randint(0, WIDTH-ENEMY_SIZE), HEIGHT-ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE)
            angle = random.uniform(3.4, 6.0)
        elif edge == 'left':
            self.rect = pygame.Rect(0, random.randint(0, HEIGHT-ENEMY_SIZE), ENEMY_SIZE, ENEMY_SIZE)
            angle = random.uniform(-1.3, 1.3)
        else:
            self.rect = pygame.Rect(WIDTH-ENEMY_SIZE, random.randint(0, HEIGHT-ENEMY_SIZE), ENEMY_SIZE, ENEMY_SIZE)
            angle = random.uniform(1.8, 4.5)
        self.vel = pygame.Vector2(ENEMY_SPEED, 0).rotate_rad(angle)

    def update(self):
        self.rect.x += int(self.vel.x)
        self.rect.y += int(self.vel.y)

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 40, 40), self.rect)

    def off_screen(self):
        return (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT)

# --- Основной игровой цикл
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Игра на выживание")
    clock = pygame.time.Clock()

    player = Player(WIDTH // 2, HEIGHT // 2)
    enemies = []
    pygame.time.set_timer(pygame.USEREVENT, ENEMY_SPAWN_TIME)
    font = pygame.font.SysFont(None, 36)
    start_ticks = pygame.time.get_ticks()

    running = True
    while running:
        dt = clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                enemies.append(Enemy())

        player.update(keys)
        for enemy in enemies:
            enemy.update()

        # Удаляем врагов, ушедших за экран
        enemies = [e for e in enemies if not e.off_screen()]

        # Проверка столкновения
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                running = False

        # Рендер
        screen.fill((30, 30, 30))
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        # Время выживания
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        text = font.render(f"Время: {seconds} сек", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        pygame.display.flip()

    # --- Гейм овер экран
    screen.fill((30, 30, 30))
    text1 = font.render("Вы проиграли! Ваше время: {} сек".format(seconds), True, (255, 0, 0))
    text2 = font.render("Нажмите любую клавишу для выхода.", True, (255, 255, 255))
    screen.blit(text1, (WIDTH//2 - text1.get_width()//2, HEIGHT//2 - 40))
    screen.blit(text2, (WIDTH//2 - text2.get_width()//2, HEIGHT//2 + 10))
    pygame.display.flip()
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                wait = False

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
