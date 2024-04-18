import pygame
import random

# Initialisierung von Pygame
pygame.init()

# Neue Bildschirmabmessungen
WIDTH, HEIGHT = 999, 562  # Neue Abmessungen für das Spielfeld

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Spieler Eigenschaften
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 47  # Spielergröße
PLAYER_SPEED = 5

# Gegner Eigenschaften
ENEMY_WIDTH, ENEMY_HEIGHT = 30, 30
ENEMY_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

# Hintergrundbild laden und anpassen
background = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Neckarstadion.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Spielerbild laden und anpassen
player_image = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/VfB_Wappen.png")
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Initialisierung des Bildschirms
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weiche den Feinden aus")
clock = pygame.time.Clock()

# Funktion zum Erzeugen eines neuen Gegners
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = 0 - ENEMY_HEIGHT
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)

# Funktion zum Bewegen der Gegner
def move_enemies(enemies):
    for enemy in enemies:
        enemy.y += ENEMY_SPEED

# Funktion zum Zeichnen der Spieler
def draw_player(player):
    screen.blit(player_image, (player.x, player.y))

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

        # Spielerbewegung basierend auf der Mausposition aktualisieren
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player.x = mouse_x - PLAYER_WIDTH // 2
        player.y = mouse_y - PLAYER_HEIGHT // 2

        # Begrenze den Spieler auf den Bildschirm
        player.x = max(0, min(player.x, WIDTH - PLAYER_WIDTH))
        player.y = max(0, min(player.y, HEIGHT - PLAYER_HEIGHT))

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
