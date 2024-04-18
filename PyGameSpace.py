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
PROJECTILE_SPEED = 3  # Geschwindigkeit des Schusses
SHOOT_DELAY = 2  # Schussverzögerung in Sekunden
FAUST_SIZE = 35  # Größe des Faust-Bildes
MEISTERSCHALE_SIZE = 63  # Größe der Meisterschale
MEISTERSCHALE_INTERVAL = 5  # Intervall, in dem eine Meisterschale erscheint

# Spielbildschirm initialisieren
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Spielbildschirm erstellen
pygame.display.set_caption("Weiche den Feinden aus")  # Titel des Fensters festlegen
clock = pygame.time.Clock()  # Pygame-Uhr für die Framerate

# Bilder laden und skalieren
background_image = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Neckarstadion.png")  # Hintergrundbild laden
player_image = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/VfB_Wappen.png")  # Spielerbild laden
# Bild für das Schussobjekt laden und skalieren
faust_image = pygame.transform.scale(pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Faust.png").convert_alpha(), (FAUST_SIZE, FAUST_SIZE))
# Meisterschale laden und skalieren
meisterschale_image = pygame.transform.scale(pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Meisterschale.png").convert_alpha(), (MEISTERSCHALE_SIZE, MEISTERSCHALE_SIZE))
# Stern laden und skalieren
stern_image = pygame.transform.scale(pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Stern.png").convert_alpha(), (15, 15))
# Liste der Feindbilder mit transparentem Hintergrund
enemy_images = [
    pygame.transform.scale(pygame.image.load(f"C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/{team}_Wappen.png").convert_alpha(), (ENEMY_SIZE, ENEMY_SIZE)) for team in ["FCB", "BVB", "KSC", "SVK", "Hertha", "Köln"]
]

# Skalieren der Spielergrafik auf die richtige Größe
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Hauptspiel
def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT // 4 * 3 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)  # Spieler-Rechteck erstellen
    enemies = []  # Liste für die Gegner initialisieren
    projectiles = []  # Liste für die Projektile initialisieren

    last_shot_time = time.time()  # Zeitpunkt des letzten Schusses initialisieren
    last_meisterschale_time = time.time()  # Zeitpunkt des letzten Erscheinens der Meisterschale initialisieren
    meisterschaften = 0  # Anzahl der Meisterschaften initialisieren

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
            # Spielerbewegung mit Maussteuerung
            player.centerx, player.centery = max(PLAYER_WIDTH // 2, min(pygame.mouse.get_pos()[0], WIDTH - PLAYER_WIDTH // 2)), max(HEIGHT // 4, min(pygame.mouse.get_pos()[1], HEIGHT - PLAYER_HEIGHT // 2))  # Spielerposition aktualisieren

            # Bewege die Gegner und füge neue hinzu
            for enemy in enemies:  # Für jeden Gegner
                enemy['rect'].y += ENEMY_SPEED  # Gegner nach unten bewegen
            if random.randint(0, ENEMY_INTERVAL) == 0:  # Zufällig neuen Gegner hinzufügen
                x = random.randint(0, WIDTH - ENEMY_SIZE)  # Zufällige X-Position für den Gegner
                enemies.append({'rect': pygame.Rect(x, 0 - ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE), 'image': random.choice(enemy_images)})  # Neuen Gegner hinzufügen

            # Bewege die Projektile
            for projectile in projectiles:  # Für jedes Projektil
                projectile.y -= PROJECTILE_SPEED  # Projektil nach oben bewegen

            # Schuss des Spielers
            current_time = time.time()
            if current_time - last_shot_time >= SHOOT_DELAY:  # Wenn genug Zeit seit dem letzten Schuss vergangen ist
                if pygame.key.get_pressed()[pygame.K_SPACE]:  # Wenn die Leertaste gedrückt wird
                    projectiles.append(pygame.Rect(player.centerx - FAUST_SIZE // 2, player.top - FAUST_SIZE, FAUST_SIZE, FAUST_SIZE))  # Neues Projektil hinzufügen
                    last_shot_time = current_time  # Zeitpunkt des aktuellen Schusses aktualisieren

            # Kollisionserkennung mit dem Spieler für Meisterschaften
            for enemy in enemies[:]:  # Für jeden Gegner
                if player.colliderect(enemy['rect']) and enemy['image'] == meisterschale_image:  # Wenn Spieler die Meisterschale berührt
                    meisterschaften += 1  # Anzahl der Meisterschaften erhöhen
                    enemies.remove(enemy)  # Meisterschale entfernen

            # Kollisionserkennung mit dem Spieler für Feinde
            for enemy in enemies[:]:  # Für jeden Gegner
                if player.colliderect(enemy['rect']) and enemy['image'] != meisterschale_image:  # Wenn Spieler einen Feind (nicht Meisterschale) berührt
                    game_over = True  # Spiel als beendet markieren

            # Kollisionserkennung mit der Faust für Feinde
            for projectile in projectiles[:]:  # Für jedes Projektil
                for enemy in enemies[:]:  # Für jeden Gegner
                    if enemy['rect'].colliderect(projectile):  # Wenn Kollision zwischen Feind und Projektil
                        enemies.remove(enemy)  # Feind entfernen
                        projectiles.remove(projectile)  # Projektil entfernen

            # Meisterschale erscheinen lassen
            if current_time - last_meisterschale_time >= MEISTERSCHALE_INTERVAL:  # Wenn Zeit für eine neue Meisterschale
                x = random.randint(0, WIDTH - MEISTERSCHALE_SIZE)  # Zufällige X-Position für die Meisterschale
                enemies.append({'rect': pygame.Rect(x, 0 - MEISTERSCHALE_SIZE, MEISTERSCHALE_SIZE, MEISTERSCHALE_SIZE), 'image': meisterschale_image})  # Meisterschale hinzufügen
                last_meisterschale_time = current_time  # Zeitpunkt des aktuellen Erscheinens der Meisterschale aktualisieren

            # Anzeige der Anzahl der Meisterschaften oben rechts
            font = pygame.font.Font(None, 36)  # Schriftart für die Anzeige der Meisterschaften festlegen
            text = font.render(f"Meisterschaften: {meisterschaften}", True, RED)  # Meisterschaften-Text rendern
            text_rect = text.get_rect(topright=(WIDTH - 10, 10))  # Position des Texts festlegen
            screen.blit(text, text_rect)  # Text auf den Bildschirm zeichnen

            # Anzeige der Sterne basierend auf der Anzahl der Meisterschaften
            if meisterschaften >= 20:
                screen.blit(stern_image, (player.centerx - 35, player.top - 20))
            if meisterschaften >= 5:
                 screen.blit(stern_image, (player.centerx - 20, player.top - 20))
            if meisterschaften >= 3:
                 screen.blit(stern_image, (player.centerx -5 , player.top - 20))
            if meisterschaften >= 10:
                 screen.blit(stern_image, (player.centerx + 10, player.top - 20))
            if meisterschaften >= 30:
                screen.blit(stern_image, (player.centerx + 25, player.top - 20))

            # Zeichne Spieler und Gegner
            screen.blit(player_image, player)  # Spieler zeichnen
            [screen.blit(enemy['image'], enemy['rect'].topleft) for enemy in enemies]  # Gegner zeichnen
            [screen.blit(faust_image, projectile.topleft) for projectile in projectiles]  # Projektile zeichnen

        if game_over:  # Wenn das Spiel vorbei ist
            font = pygame.font.Font(None, 72)  # Schriftart für die Anzeige des Spielendes festlegen
            text = font.render("Game Over!", True, RED)  # "Game Over!"-Text rendern
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Position des Texts festlegen
            screen.blit(text, text_rect)  # Text auf den Bildschirm zeichnen
            if game_over_time is None:
                game_over_time = time.time()  # Zeitstempel für das Spielende setzen
            if time.time() - game_over_time > 3:  # Wenn 3 Sekunden vergangen sind seit dem Spielende
                running = False  # Spiel beenden

        pygame.display.flip()  # Bildschirm aktualisieren
        clock.tick(60)  # Framerate auf 60 FPS begrenzen

    pygame.quit()  # Pygame beenden

if __name__ == "__main__":  # Wenn das Skript direkt ausgeführt wird
    main()  # Hauptspiel starten
