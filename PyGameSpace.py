import pygame  # Pygame-Bibliothek importieren
import random  # Zufallszahlen generieren
import time  # Zeitfunktionen

# Initialisierung von Pygame
pygame.init()

# Bildschirmabmessungen definieren
WIDTH, HEIGHT = 999, 562

# Farben definieren
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Spieler- und Gegner-Eigenschaften festlegen
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 47
ENEMY_SIZE = 55
ENEMY_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

# Spielbildschirm initialisieren
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Spielbildschirm erstellen
pygame.display.set_caption("Weiche den Feinden aus")  # Titel des Fensters festlegen
clock = pygame.time.Clock()  # Pygame-Uhr für die Framerate

# Bilder laden und skalieren
background_image = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Neckarstadion.png")  # Hintergrundbild laden
player_image = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/VfB_Wappen.png")  # Spielerbild laden
# Liste der Feindbilder mit transparentem Hintergrund
enemy_images = [
    pygame.transform.scale(pygame.image.load(f"C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/{team}_Wappen.png").convert_alpha(), (ENEMY_SIZE, ENEMY_SIZE)) for team in ["FCB", "BVB", "KSC", "SVK", "Hertha", "Köln"]
]

# Hauptspiel
def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT // 4 * 3 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)  # Spieler-Rechteck erstellen
    enemies = []  # Liste für die Gegner initialisieren

    running = True  # Flag für das Spiel initialisieren
    game_over = False  # Flag für Spielende initialisieren
    game_over_time = None  # Zeitstempel für das Spielende initialisieren
    while running:  # Hauptschleife des Spiels
        screen.fill(WHITE)  # Bildschirm mit Weiß füllen
        screen.blit(background_image, (0, 0))  # Hintergrundbild zeichnen

        for event in pygame.event.get():  # Ereignisschleife
            if event.type == pygame.QUIT:  # Wenn das Spiel beendet werden soll
                running = False  # Spiel beenden

        if not game_over:  # Wenn das Spiel nicht vorbei ist
            player.centerx, player.centery = max(PLAYER_WIDTH // 2, min(pygame.mouse.get_pos()[0], WIDTH - PLAYER_WIDTH // 2)), max(HEIGHT // 4, min(pygame.mouse.get_pos()[1], HEIGHT - PLAYER_HEIGHT // 2))  # Spielerposition aktualisieren

            for enemy in enemies:  # Für jeden Gegner
                enemy['rect'].y += ENEMY_SPEED  # Gegner nach unten bewegen
            if random.randint(0, ENEMY_INTERVAL) == 0:  # Zufällig neuen Gegner hinzufügen
                x = random.randint(0, WIDTH - ENEMY_SIZE)  # Zufällige X-Position für den Gegner
                enemies.append({'rect': pygame.Rect(x, 0 - ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE), 'image': random.choice(enemy_images)})  # Neuen Gegner hinzufügen

            if any(player.colliderect(enemy['rect']) for enemy in enemies):  # Kollisionserkennung
                game_over, game_over_time = True, time.time()  # Spiel als beendet markieren und Zeitstempel setzen

            screen.blit(player_image, player)  # Spieler zeichnen
            [screen.blit(enemy['image'], enemy['rect'].topleft) for enemy in enemies]  # Gegner zeichnen

        if game_over:  # Wenn das Spiel vorbei ist
            font = pygame.font.Font(None, 72)  # Schriftart für die Anzeige des Spielendes festlegen
            text = font.render("Game Over!", True, RED)  # "Game Over!"-Text rendern
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Position des Texts festlegen
            screen.blit(text, text_rect)  # Text auf den Bildschirm zeichnen
            if time.time() - game_over_time > 3:  # Wenn 3 Sekunden vergangen sind seit dem Spielende
                running = False  # Spiel beenden

        pygame.display.flip()  # Bildschirm aktualisieren
        clock.tick(60)  # Framerate auf 60 FPS begrenzen

    pygame.quit()  # Pygame beenden

if __name__ == "__main__":  # Wenn das Skript direkt ausgeführt wird