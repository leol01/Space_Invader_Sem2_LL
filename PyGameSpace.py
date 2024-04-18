import pygame
import random

# Initialisierung von Pygame
pygame.init()

# Bildschirmabmessungen
WIDTH, HEIGHT = 600, 400

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Spieler Eigenschaften
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 20
PLAYER_SPEED = 5

# Gegner Eigenschaften
ENEMY_WIDTH, ENEMY_HEIGHT = 30, 30
ENEMY_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

# Initialisierung des Bildschirms
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weiche den Feinden aus")
clock = pygame.time.Clock()

# Hintergrundbild laden
background = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Neckarstadion.png")

# Funktion zum Erzeugen eines neuen Gegners
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = 0 - ENEMY_HEIGHT
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

# Funktion zum Bewegen der Gegner
def move_enemies(enemies):
    for enemy in enemies:
        enemy.y += ENEMY_SPEED

# Funktion zum Zeichnen des Spielers
def draw_player(player):
    pygame.draw.rect(screen, RED, player)

# Funktion zum Zeichnen der Gegner
def draw_enemies(enemies):
    for enemy in enemies:
        pygame.draw.rect(screen, BLACK, enemy)

# Hauptspiel
def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = []

    running = True
    while running:
        # Hintergrund zeichnen
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED

        # Begrenze den Spieler auf den Bildschirm
        player.x = max(0, min(player.x, WIDTH - PLAYER_WIDTH))

        # Bewege die Gegner und füge neue hinzu
        move_enemies(enemies)
        if random.randint(0, ENEMY_INTERVAL) == 0:
            enemies.append(create_enemy())

        # Kollisionserkennung
        for enemy in enemies:
            if player.colliderect(enemy):
                running = False

        # Zeichne Spieler und Gegner
        draw_player(player)
        draw_enemies(enemies)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
