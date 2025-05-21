import pygame
import sys
from SaveLoadManager import SaveLoadSystem
from button import Button
import random
import math

pygame.init()

saveloadmanager = SaveLoadSystem(".save", "save_data")

# screen
SCREEN = pygame.display.set_mode((1008, 720))
pygame.display.set_caption("Space Invaders")
# backgrounds
BG = pygame.image.load('assets/Background.png')
bg_game = pygame.image.load('assets/backstar2.jpg')
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# font


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


# Player
player_img = pygame.Surface((50, 40))
player_img.fill((0, 128, 255))
player_x = 1008 // 2 - 25
player_y = 720 - 60
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
    x = random.randint(0, 1008 - 40)
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
text_x = 1000
text_y = 10


# sprites
heart = pygame.image.load('assets/sprites/heart.png').convert_alpha()
damage1 = pygame.image.load('assets/sprites/damage1.png').convert_alpha()
damage2 = pygame.image.load('assets/sprites/damage2.png').convert_alpha()
hard1 = pygame.image.load('assets/sprites/hard1.png').convert_alpha()
hard2 = pygame.image.load('assets/sprites/hard2.png').convert_alpha()
hard1 = pygame.transform.scale2x(hard1)
hard2 = pygame.transform.scale2x(hard2)
hard1 = pygame.transform.scale2x(hard1)
hard2 = pygame.transform.scale2x(hard2)
med1 = pygame.image.load('assets/sprites/med1.png').convert_alpha()
med2 = pygame.image.load('assets/sprites/med2.png').convert_alpha()
med1 = pygame.transform.scale2x(med1)
med2 = pygame.transform.scale2x(med2)
med1 = pygame.transform.scale2x(med1)
med2 = pygame.transform.scale2x(med2)
easy1 = pygame.image.load('assets/sprites/easy1.png').convert_alpha()
easy2 = pygame.image.load('assets/sprites/easy2.png').convert_alpha()
easy1 = pygame.transform.scale2x(easy1)
easy2 = pygame.transform.scale2x(easy2)
easy1 = pygame.transform.scale2x(easy1)
easy2 = pygame.transform.scale2x(easy2)

clock = pygame.time.Clock()
delta_time = 0.1


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, WHITE)
    SCREEN.blit(score, (x, y))


def player(x, y):
    SCREEN.blit(player_img, (x, y))


def enemy(x, y):
    SCREEN.blit(enemy_img, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    SCREEN.blit(bullet_img, (x + 32, y))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    return distance < 27


def play():
    global bullet_state, player_x, bullet_y, player_x_change, bullet_x, score_value
    p = 0
    p2 = 0
    z = 0
    lives = 3
    game_over = False

    while True:
        p = p + 1
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(bg_game, (0, 0))

        # hearts
        if lives >= 1:
            SCREEN.blit(heart, (0, 0))
        if lives > 1:
            SCREEN.blit(heart, (50, 0))
        if lives > 2:
            SCREEN.blit(heart, (100, 0))

        # enemies
        # if p < 51:
        #     SCREEN.blit(hard2, (z, 30))
        #     SCREEN.blit(med2, (z, 90))
        #     SCREEN.blit(easy2, (z, 150))
        # if p > 50:
        #     SCREEN.blit(hard1, (z, 30))
        #     SCREEN.blit(med1, (z, 90))
        #     SCREEN.blit(easy1, (z, 150))
        #     if p == 100:
        #         p = 0

        z = z + 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # saveloadmanager.save_data()
                    pause()
                if event.key == pygame.K_j:
                    if lives > 1:
                        print("oof")
                        # damage animation
                        for i in range(100):
                            if lives == 1:
                                if p2 < 51:
                                    SCREEN.blit(damage1, (0, 0))
                                elif p2 > 50:
                                    SCREEN.blit(damage2, (0, 0))
                            if lives == 2:
                                if p2 < 51:
                                    SCREEN.blit(damage1, (50, 0))
                                elif p2 > 50:
                                    SCREEN.blit(damage2, (50, 0))
                            if lives == 3:
                                if p2 < 51:
                                    SCREEN.blit(damage1, (100, 0))
                                elif p2 > 50:
                                    SCREEN.blit(damage2, (100, 0))
                        lives = lives - 1
                    else:
                        print(":(")
                        main_menu()
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
            elif player_x >= 1008 - 50:
                player_x = 1008 - 50

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
                    elif enemy_x >= 1008 - 40:
                        enemy_x_dir = -enemy_speed
                        enemy_y += enemy_y_change

                    # Collision detection
                    if bullet_state == "fire":
                        if is_collision(enemy_x, enemy_y, bullet_x + 2, bullet_y):
                            bullet_y = player_y
                            bullet_state = "ready"
                            score_value = score_value + 1
                            enemy_x = random.randint(0, 1008 - 40)
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

        player(player_x, player_y)
        pygame.display.update()


def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(35).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(504, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(504, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changecolor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkforinput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(504, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(504, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(504, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(504, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changecolor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkforinput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkforinput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkforinput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def pause():
    loop = 1
    MENU_TEXT = get_font(150).render("PAUSED", True, "#b68f40")
    MENU_RECT = MENU_TEXT.get_rect(center=(504, 600))
    QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(504, 450),
                         text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    while loop:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [QUIT_BUTTON]:
            button.changecolor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = 0
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkforinput(MENU_MOUSE_POS):
                    # saveloadmanager.save_data()
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


main_menu()
