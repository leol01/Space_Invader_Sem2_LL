import pygame
import random
import time

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
SHOOT_DELAY = 0.5  # Schussverzögerung in Sekunden
FAUST_SIZE = 35  # Größe des Faust-Bildes
MEISTERSCHALE_SIZE = 63  # Größe der Meisterschale
MEISTERSCHALE_INTERVAL = 5  # Intervall, in dem eine Meisterschale erscheint

# Geschwindigkeitszunahme der Feinde
enemy_speed_increment = 0.001  

# Intervallverringerung für das Erscheinen neuer Feinde
enemy_interval_decrement = 0.01 

# Spielbildschirm initialisieren
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weiche den Feinden aus")
clock = pygame.time.Clock()

# Bilder laden und skalieren
background_image = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Neckarstadion.png")
player_image = pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/VfB_Wappen.png")
faust_image = pygame.transform.scale(pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Faust.png").convert_alpha(), (FAUST_SIZE, FAUST_SIZE))
meisterschale_image = pygame.transform.scale(pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Meisterschale.png").convert_alpha(), (MEISTERSCHALE_SIZE, MEISTERSCHALE_SIZE))
stern_image = pygame.transform.scale(pygame.image.load("C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/Stern.png").convert_alpha(), (15, 15))
enemy_images = [
    pygame.transform.scale(pygame.image.load(f"C:/Users/leo.leberer/Desktop/Space_Invader_Sem2_LL/{team}_Wappen.png").convert_alpha(), (ENEMY_SIZE, ENEMY_SIZE)) for team in ["FCB", "BVB", "KSC", "SVK", "Hertha", "Köln"]
]
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Einleitung anzeigen
def show_instructions():
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font("C:/Windows/Fonts/arial.ttf", 18)
    
    # Transparenten Hintergrund für die Spielregeln erstellen
    transparent_surface = pygame.Surface((5000, 5000), pygame.SRCALPHA)
    transparent_surface.fill((0, 0, 0, 163))  # 128 für 50% Transparenz
    screen.blit(transparent_surface, (-100, -100))
    
    instructions = [
        "Spielregeln:",
        "1. Bewegen Sie das VfB - Wappem mit der Maus.",
        "2. Klicken Sie die linke Maustaste oder drücken Sie die Leertaste, um andere Vereine zu schlagen.",
        "3. Berühren Sie die Meisterschale, um eine Meisterschaft zu gewinnen.",
        "    Die Anzahl der gewonnenen Meisterschaften wird rechts oben angezeigt, sowie durch die Sterne über dem Wappen.",
        "4. Berühren Sie einen Gegner, so haben sie das Spiel verloren.",
        "5. Können Sie den DFB- oder den CL- Pokal gewinnen, so erhalten sie ein Extraleben."
    ]
    y = 100
    for line in instructions:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(left=WIDTH - 980, centery=y-80)
        screen.blit(text, text_rect)
        y += 30
    
    start_button_rect = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT // 2 + 50, PLAYER_WIDTH, PLAYER_HEIGHT)
    pygame.draw.rect(screen, RED, start_button_rect)
    screen.blit(player_image, start_button_rect)
    font = pygame.font.Font("C:/Windows/Fonts/arial.ttf", 33)
    text = font.render("Hier klicken für START", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
    screen.blit(text, text_rect)

    pygame.display.flip()

    return start_button_rect

# Hauptspiel
def main():
    global ENEMY_SPEED  # Zugriff auf die globale Variable ENEMY_SPEED
    global ENEMY_INTERVAL  # Zugriff auf die globale Variable ENEMY_INTERVAL

    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT // 4 * 3 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = []
    projectiles = []

    last_shot_time = time.time()
    last_meisterschale_time = time.time()
    meisterschaften = 0

    running = True
    game_over = False
    game_over_time = None
    while running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # Schuss mit Leertaste
                projectiles.append(pygame.Rect(player.centerx - FAUST_SIZE // 2, player.top - FAUST_SIZE, FAUST_SIZE, FAUST_SIZE))
                last_shot_time = time.time()

        if not game_over:
            # Spielerbewegung mit Maus
            player.centerx, player.centery = max(PLAYER_WIDTH // 2, min(pygame.mouse.get_pos()[0], WIDTH - PLAYER_WIDTH // 2)), max(HEIGHT // 4, min(pygame.mouse.get_pos()[1], HEIGHT - PLAYER_HEIGHT // 2))

            for enemy in enemies:
                enemy['rect'].y += ENEMY_SPEED
            if random.randint(0, int(ENEMY_INTERVAL)) == 0:
                x = random.randint(0, WIDTH - ENEMY_SIZE)
                # Überprüfen, ob der Abstand zu anderen Feinden groß genug ist
                overlap = True
                while overlap:
                    overlap = False
                    new_enemy_rect = pygame.Rect(x, 0 - ENEMY_SIZE, ENEMY_SIZE, ENEMY_SIZE)
                    for existing_enemy in enemies:
                        if new_enemy_rect.colliderect(existing_enemy['rect']):
                            overlap = True
                            x = random.randint(0, WIDTH - ENEMY_SIZE)
                            break
                enemies.append({'rect': new_enemy_rect, 'image': random.choice(enemy_images)})

            for projectile in projectiles:
                projectile.y -= PROJECTILE_SPEED

            # Schuss des Spielers mit Mausklick
            current_time = time.time()
            if current_time - last_shot_time >= SHOOT_DELAY:
                if pygame.mouse.get_pressed()[0]:  # Wenn die linke Maustaste gedrückt wird
                    projectiles.append(pygame.Rect(player.centerx - FAUST_SIZE // 2, player.top - FAUST_SIZE, FAUST_SIZE, FAUST_SIZE))
                    last_shot_time = current_time

            # Kollisionserkennung mit dem Spieler für Meisterschaften
            for enemy in enemies[:]:
                if player.colliderect(enemy['rect']) and enemy['image'] == meisterschale_image:
                    meisterschaften += 1
                    enemies.remove(enemy)

            # Kollisionserkennung mit dem Spieler für Feinde
            for enemy in enemies[:]:
                if player.colliderect(enemy['rect']) and enemy['image'] != meisterschale_image:
                    game_over = True

            # Kollisionserkennung mit der Faust für Feinde
            for projectile in projectiles[:]:
                for enemy in enemies[:]:
                    if enemy['rect'].colliderect(projectile):
                        enemies.remove(enemy)
                        projectiles.remove(projectile)

            # Meisterschale erscheinen lassen
            if current_time - last_meisterschale_time >= MEISTERSCHALE_INTERVAL:
                x = random.randint(0, WIDTH - MEISTERSCHALE_SIZE)
                enemies.append({'rect': pygame.Rect(x, 0 - MEISTERSCHALE_SIZE, MEISTERSCHALE_SIZE, MEISTERSCHALE_SIZE), 'image': meisterschale_image})
                last_meisterschale_time = current_time

            # Anzeige der Anzahl der Meisterschaften oben rechts
            transparent_surface = pygame.Surface((600, 50), pygame.SRCALPHA)
            transparent_surface.fill((0, 0, 0, 100))  # 128 für 50% Transparenz
            screen.blit(transparent_surface, (763, 0))
            font = pygame.font.Font(None, 36)
            text = font.render(f"Meisterschaften: {meisterschaften}", True, RED)
            text_rect = text.get_rect(topright=(WIDTH - 10, 10))
            screen.blit(text, text_rect)

            # Anzeige der Sterne basierend auf der Anzahl der Meisterschaften

            if meisterschaften >= 20:
                screen.blit(stern_image, (player.centerx - 35, player.top - 20))
            if meisterschaften >= 5:
                screen.blit(stern_image, (player.centerx - 20, player.top - 20))
            if meisterschaften >= 3:
                screen.blit(stern_image, (player.centerx - 5, player.top - 20))
            if meisterschaften >= 10:
                screen.blit(stern_image, (player.centerx + 10, player.top - 20))
            if meisterschaften >= 30:
                screen.blit(stern_image, (player.centerx + 25, player.top - 20))

            screen.blit(player_image, player)
            [screen.blit(enemy['image'], enemy['rect'].topleft) for enemy in enemies]
            [screen.blit(faust_image, projectile.topleft) for projectile in projectiles]

            # Geschwindigkeit der Feinde erhöhen
            ENEMY_SPEED += enemy_speed_increment
            # Intervall zwischen dem Erscheinen neuer Feinde verkürzen
            ENEMY_INTERVAL -= enemy_interval_decrement
            # Begrenzen, damit die Geschwindigkeit nicht ins Unendliche steigt und das Intervall nicht negativ wird
            ENEMY_SPEED = min(10, ENEMY_SPEED)
            ENEMY_INTERVAL = max(10, ENEMY_INTERVAL)

        if game_over:
            # Transparenten Hintergrund 
            transparent_surface = pygame.Surface((5000, 5000), pygame.SRCALPHA)
            transparent_surface.fill((0, 0, 0, 163))  # 128 für 50% Transparenz
            screen.blit(transparent_surface, (-100, -100))
            font = pygame.font.Font(None, 72)
            text = font.render("Game Over!", True, RED)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            if game_over_time is None:
                game_over_time = time.time()
            if time.time() - game_over_time > 3:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    start_button_rect = show_instructions()
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    waiting_for_start = False
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting_for_start = False
    main()
