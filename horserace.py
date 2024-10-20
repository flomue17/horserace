import pygame
import sys
import json
from enum import Enum

# Initialisieren von Pygame
pygame.init()

# Bildschirmgröße definieren
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pferderennen")

# Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Spielzustände
class GameState(Enum):
    SETUP = 0
    RUNNING = 1


# Startpositionen
start_x = 50
goal_x = WIDTH - 100
goal_size = 8

# JSON-Datei initial laden und leere Pferdeliste erstellen
with open("horses.json", "r") as f:
    data = json.load(f)

horses = data["horses"]

# Fledermaus-Bild laden und auf passende Größe skalieren
bat_image = pygame.image.load('bat.png')  # Hier ist der Pfad zur Fledermausbilddatei
bat_image = pygame.transform.scale(bat_image, (50, 30))  # Größe anpassen

# Eingabefeld-Setup
font = pygame.font.Font(None, 36)
input_box_width = 400
input_box_height = 32
input_box = pygame.Rect(WIDTH // 2 - input_box_width // 2, HEIGHT - 300, input_box_width, input_box_height)

input_text = ''
active = False

# Button-Setup
button_font = pygame.font.Font(None, 48)
start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 300, 200, 50)
quit_button = pygame.Rect(WIDTH - 300, HEIGHT - 300, 200, 50)

# Initialer Spielzustand
game_state = GameState.SETUP

clock = pygame.time.Clock()


def draw_horses():
    for horse in horses:
        # Zeichne das Fledermaus-Bild statt eines Rechtecks
        screen.blit(bat_image, (horse["x_pos"], horse["y_pos"]))

        # Teamnamen unter dem Bild anzeigen
        horse_name_text = font.render(horse["name"], True, BLACK)
        text_rect = horse_name_text.get_rect(center=(horse["x_pos"] + 25, horse["y_pos"] + 45))
        screen.blit(horse_name_text, text_rect)


def move_horse(horse_name):
    step_distance = (goal_x - start_x) / goal_size
    for horse in horses:
        if horse["name"] == horse_name:
            horse["x_pos"] += step_distance


def add_horse(name):
    y_pos = 50 + len(horses) * 100  # Neue Y-Position für das neue Pferd
    horse = {
        "name": name,
        "color": [200, 0, 0],  # Farbe des Pferdes (wird jetzt nicht mehr verwendet)
        "y_pos": y_pos,
        "x_pos": start_x
    }
    horses.append(horse)


def save_horses_to_json():
    # Speichern der Pferdedaten in einer JSON-Datei
    with open("horses.json", "w") as f:
        json.dump({"horses": horses}, f)


# Hauptschleife
running = True
while running:
    screen.fill(WHITE)

    # Zeichnen der Pferde
    if horses:
        draw_horses()

    # Quit-Button zeichnen
    pygame.draw.rect(screen, GREEN, quit_button)
    quit_text = button_font.render("Quit", True, BLACK)
    screen.blit(quit_text, (quit_button.x + 50, quit_button.y + 10))

    # Eingabefeld zeichnen
    txt_surface = font.render(input_text, True, BLACK)
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, RED, input_box, 2)

    # Start-Button zeichnen, wenn im Setup-Modus
    if game_state == GameState.SETUP:
        pygame.draw.rect(screen, GREEN, start_button)
        start_text = button_font.render("Start", True, BLACK)
        screen.blit(start_text, (start_button.x + 50, start_button.y + 10))

    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False

            # Start-Button gedrückt
            if start_button.collidepoint(event.pos) and game_state == GameState.SETUP:
                game_state = GameState.RUNNING
                save_horses_to_json()

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    # Pferd bewegen im RUNNING-Modus
                    if game_state == GameState.RUNNING and input_text.strip() != "":
                        move_horse(input_text)
                    # Neues Pferd hinzufügen im SETUP-Modus
                    elif game_state == GameState.SETUP and input_text.strip() != "":
                        add_horse(input_text)
                    input_text = ''  # Textfeld nach dem Hinzufügen oder Bewegen leeren
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # Überprüfen, ob ein Pferd das Ziel erreicht hat
    if game_state == GameState.RUNNING:
        for horse in horses:
            if horse["x_pos"] >= goal_x:
                print(f"{horse['name']} hat das Rennen gewonnen!")
                

    pygame.display.flip()
    clock.tick(30)
