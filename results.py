def results_func(): 



    # Import
    import pygame
    import csv
    import sys

    # Initialisierung von Pygame
    pygame.init()

    # Definieren der Bildschirmgröße
    WIDTH, HEIGHT = 999, 562

    # Hintergrundbild laden
    background_image = pygame.image.load("Neckarstadion.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Fenster erstellen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Spielergebnisse")



    ###################################################################################################################



    # Funktion zum Lesen von Daten aus der CSV-Datei
    def read_from_csv(filename):
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                # Überspringe die erste Zeile, die die Spaltenüberschriften enthält
                next(reader)
                data = [row for row in reader]  # Lies alle folgenden Zeilen aus der CSV-Datei
            return data
        except Exception as e:
            print("Fehler beim Lesen der CSV-Datei:", e)
            return None

    # Funktion zum Anzeigen der Spielergebnisse im Fenster
    def show_player_results(data):
        if data:
            # Sortiere die Daten nach Meisterschaften
            sorted_data = sorted(data, key=lambda x: int(x[1]), reverse=True)

            # Schleife durch die sortierten Daten und zeige sie an
            for i, row in enumerate(sorted_data):
                # Zeige die Daten an
                font = pygame.font.Font(None, 36)
                text_surface = font.render(f"{i+1}. {row[0]} - {row[1]} Meistertitel", True, (100, 0, 0))
                screen.blit(text_surface, (10, 5 + i * 40))  # Position des Textes auf dem Bildschirm
        else:
            print("Fehler beim Lesen der Spielergebnisse aus der CSV-Datei.")

    # Funktion zum Zurücksetzen der Spielergebnisse
    def reset_scores():
        with open("deine_datei.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Spielername", "Meisterschaften"])  # Überschriften schreiben
        pygame.quit()
        sys.exit()



    #################################################################################################################



    # Lese die Daten aus der CSV-Datei
    player_data = read_from_csv("deine_datei.csv")

    # Schleife für das Hauptprogramm
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Überprüfen, ob die Maus über dem Zurücksetzen-Knopf liegt
                if reset_button_rect.collidepoint(mouse_pos):
                    reset_scores()

        # Hintergrundbild zeichnen
        screen.blit(background_image, (0, 0))

        # Spielergebnisse anzeigen
        show_player_results(player_data)

        # Knopf zum Zurücksetzen der Spielergebnisse zeichnen
        font = pygame.font.Font(None, 30)
        reset_text = font.render("Zurücksetzen der Spielstände", True, (255, 255, 255))
        reset_button_width = reset_text.get_width() + 20  # Breite des Knopfes an die Textlänge anpassen
        reset_button_rect = pygame.draw.rect(screen, (0, 100, 0), (WIDTH - reset_button_width, HEIGHT - 50, reset_button_width, 40))
        screen.blit(reset_text, (WIDTH - reset_button_width + 10, HEIGHT - 40))

        # Bildschirm aktualisieren
        pygame.display.flip()

    # Pygame beenden
    pygame.quit()