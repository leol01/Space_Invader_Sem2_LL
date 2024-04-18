import pygame
import random
import time

# Initialisierung von Pygame
pygame.init()

# Bildschirmabmessungen
WIDTH, HEIGHT = 999, 562

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Spieler Eigenschaften
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 47
PLAYER_SPEED = 5

# Gegner Eigenschaften
ENEMY_SIZE = 55
ENEMY_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

# Spielbildschirm initialisieren
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weiche den Feinden aus")
clock = pygame.time.Clock()

# Bilder laden
background_image = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Neckarstadion.png")
player_image = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/VfB_Wappen.png")

# Liste der Feindbilder mit transparentem Hintergrund
enemy_images = [
    pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/FCB_Wappen.png").convert_alpha(),
    pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/BVB_Wappen.png").convert_alpha(),
    pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/KSC_Wappen.png").convert_alpha(),
    pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/SVK_Wappen.png").convert_alpha(),
    pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Hertha_Wappen.png").convert_alpha(),
    pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Köln_Wappen.png").convert_alpha()
]

# Skalieren der Feindbilder auf 55x55
enemy_images = [pygame.transform.scale(image, (ENEMY_SIZE, ENEMY_SIZE)) for image in enemy_images]

# Funktion zum Erzeugen eines neuen Gegners
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_SIZE)
    y = 0 - ENEMY_SIZE
    image = random.choice(enemy_images)  # Zufälliges Bild auswählen
    return {'rect': pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE), 'image': image}

# Funktion zum Bewegen der Gegner
def move_enemies(enemies):
    for enemy in enemies:
        enemy['rect'].y += ENEMY_SPEED

# Funktion zum Zeichnen des Spielers
def draw_player(player):
    screen.blit(player_image, player)

# Funktion zum Zeichnen der Gegner
def draw_enemies(enemies):
    for enemy in enemies:
        screen.blit(enemy['image'], enemy['rect'].topleft)

# Hauptspiel
def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT // 4 * 3 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = []

    running = True
    game_over = False
    game_over_time = None
    while running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Spielerbewegung mit Maussteuerung
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player.centerx = max(PLAYER_WIDTH // 2, min(mouse_x, WIDTH - PLAYER_WIDTH // 2))  # Begrenze nach rechts und links
            player.centery = max(HEIGHT // 4, min(mouse_y, HEIGHT- ((PLAYER_HEIGHT/2))))  # Begrenze nach unten, aber nicht nach oben

            # Bewege die Gegner und füge neue hinzu
            move_enemies(enemies)
            if random.randint(0, ENEMY_INTERVAL) == 0:
                enemies.append(create_enemy())

            # Kollisionserkennung
            for enemy in enemies[:]:
                if player.colliderect(enemy['rect']):
                    game_over = True
                    game_over_time = time.time()
                    break

            # Zeichne Spieler und Gegner
            draw_player(player)
            draw_enemies(enemies)

        if game_over:
            font = pygame.font.Font(None, 72)
            text = font.render("Game Over!", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            if time.time() - game_over_time > 3:  # Überprüfe, ob 3 Sekunden seit Game Over vergangen sind
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()