import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("First Game")


def play():
    x = 50
    y = 50
    width = 40
    height = 60
    vel = 5
    while True:
        pygame.display.set_mode((500, 500))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            x -= vel

        if keys[pygame.K_RIGHT]:
            x += vel

        if keys[pygame.K_UP]:
            y -= vel

        if keys[pygame.K_DOWN]:
            y += vel

        pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
        pygame.display.update()


play()
pygame.quit()
