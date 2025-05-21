import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Create the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Galactic Invaders")

# Icon and Title
icon = pygame.image.load('assets/sprites/lod.png') if pygame.image.get_extended() else pygame.Surface((32,32))
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Player
player_img = pygame.Surface((50, 40))
player_img.fill((0, 128, 255))
player_x = SCREEN_WIDTH // 2 - 25
player_y = SCREEN_HEIGHT - 60
player_x_change = 0
PLAYER_SPEED = 5

# Enemy
enemy_img = pygame.Surface((40, 40))
enemy_img.fill((255, 0, 0))
enemy_speed = 3
enemy_x_change = enemy_speed
enemy_y_change = 40
num_of_enemies = 6
enemies = []

for i in range(num_of_enemies):
    x = random.randint(0, SCREEN_WIDTH - 40)
    y = random.randint(50, 150)
    enemies.append([x, y, enemy_x_change])

# Bullet
bullet_img = pygame.Surface((5, 20))
bullet_img.fill((255, 255, 0))
bullet_x = 0
bullet_y = player_y
bullet_y_change = 10
bullet_state = "ready"  # "ready" - ready to fire, "fire" - bullet is moving

# Score
score_value = 0
font = pygame.font.SysFont('Arial', 32)
text_x = 10
text_y = 10

# Game Over
game_over_font = pygame.font.SysFont('Arial', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, WHITE)
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, WHITE)
    screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, SCREEN_HEIGHT // 2 - over_text.get_height() // 2))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 22, y))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    return distance < 27


# Main loop
running = True
game_over = False

clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                player_x_change = PLAYER_SPEED
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    if not game_over:
        # Player movement boundaries
        player_x += player_x_change
        if player_x <= 0:
            player_x = 0
        elif player_x >= SCREEN_WIDTH - 50:
            player_x = SCREEN_WIDTH - 50

        # Enemy movement
        for i in range(num_of_enemies):
            enemy_x, enemy_y, enemy_x_dir = enemies[i]

            # Game Over condition
            if enemy_y > player_y - 40:
                game_over = True
                break

            enemy_x += enemy_x_dir

            if enemy_x <= 0:
                enemy_x_dir = enemy_speed
                enemy_y += enemy_y_change
            elif enemy_x >= SCREEN_WIDTH - 40:
                enemy_x_dir = -enemy_speed
                enemy_y += enemy_y_change

            # Collision detection
            if bullet_state == "fire":
                if is_collision(enemy_x, enemy_y, bullet_x + 2, bullet_y):
                    bullet_y = player_y
                    bullet_state = "ready"
                    score_value += 1
                    enemy_x = random.randint(0, SCREEN_WIDTH - 40)
                    enemy_y = random.randint(50, 150)
                    enemy_x_dir = enemy_x_change

            enemies[i] = [enemy_x, enemy_y, enemy_x_dir]
            enemy(enemy_x, enemy_y)

        # Bullet movement
        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change
            if bullet_y <= 0:
                bullet_y = player_y
                bullet_state = "ready"

        player(player_x, player_y)
        show_score(text_x, text_y)

    else:
        game_over_text()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
