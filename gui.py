import sys

import pygame
from config import WIDTH, HEIGHT, WHITE, BLACK, RED, GREEN, start_x, amount_points, goal_x, start_y, amount_teams, step_size


class GUI:
    def __init__(self):
        # Bildschirmgröße
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pferderennen")

        self.background_image = pygame.image.load("background_image.png")
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        self.won = False

        # Eingabefeld
        self.font = pygame.font.Font(None, 36)
        self.input_box = pygame.Rect(10, HEIGHT - 75, 400, 32)
        self.input_text = ''
        self.active = False

        # Buttons
        self.button_font = pygame.font.Font(None, 48)
        self.start_button = pygame.Rect(1660, HEIGHT - 75, 20, 32)
        self.restart_button = pygame.Rect(1695, HEIGHT - 75, 20, 32)
        self.quit_button = pygame.Rect(1730, HEIGHT - 75, 20, 32)
        self.top3_button = pygame.Rect(1765, HEIGHT - 75, 20, 32)
        self.winner_button = pygame.Rect(1850, HEIGHT - 75, 100, 32)

        # Spielzustände
        self.game_started = False

        # Bilder laden
        self.bat_image = pygame.image.load('bat.png')
        self.bat_image = pygame.transform.scale(self.bat_image, (162, 100))

    def handle_events(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

                if self.start_button.collidepoint(event.pos):
                    self.game_started = True
                    game.save_horses_to_json(game.horses, "horses.json")

                if self.quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

                if self.restart_button.collidepoint(event.pos):
                    game.reset_horses()

                if self.top3_button.collidepoint(event.pos):
                    game.top3()

                if self.winner_button.collidepoint(event.pos):
                    self.won = True

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    if self.game_started:
                        horse_name, amount = self.input_text.split(",")

                        horse_name = horse_name.strip()  # Entfernt Leerzeichen
                        if not horse_name:
                            print("Der Pferdename darf nicht leer sein.")
                            return True
                        if not game.checkHorse(horse_name):
                            print("Der Pferdename muss gültig sein")
                            return True

                        # Überprüfen, ob amount ein gültiger Integer ist
                        try:
                            amount = int(amount)  # Entfernt Leerzeichen und konvertiert zu int
                        except ValueError:
                            print("Der Betrag muss eine gültige Ganzzahl sein.")
                            return True

                        game.move_horse(horse_name, amount)
                    else:
                        game.add_horse(self.input_text)
                    self.input_text = ''  # Leere das Eingabefeld nach dem Hinzufügen
                    game.save_horses_to_json(game.horses, "horses.json")
                    game.sort_horses()

                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

        return True

    def update_screen(self, game):

        if self.won:
            self.screen.blit(self.background_image, (0, 0))

            # Erstelle eine größere Schriftart für den Gewinner-Text
            winner_font = pygame.font.Font(None, 120)  # Schriftgröße 100
            winner_text = winner_font.render(game.horses[0]["name"] + " hat gewonnen!", True, WHITE)

            # Berechne die Mitte des Bildschirms
            text_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

            # Blitte den Text in die Mitte des Bildschirms
            self.screen.blit(winner_text, text_rect)

            pygame.display.flip()  # Aktualisiert den Bildschirm
            return  # Beendet die Methode

        self.screen.blit(self.background_image, (0, 0))
        # Pferde zeichnen
        for index, horse in enumerate(game.horses):
            self.screen.blit(self.bat_image, (horse["x_pos"], start_y + start_y + index * (HEIGHT / amount_teams)))
            horse_name_text = self.font.render(horse["name"] + "," + str(horse["points"]), True, WHITE)
            text_rect = horse_name_text.get_rect(center=(horse["x_pos"] + 77, start_y + start_y + index * (HEIGHT / amount_teams) + 110))
            self.screen.blit(horse_name_text, text_rect)

        # Eingabefeld zeichnen
        txt_surface = self.font.render(self.input_text, True, WHITE)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Start-Button zeichnen
        if not self.game_started:
            start_text = self.button_font.render("S", True, WHITE)
            self.screen.blit(start_text, (self.start_button.x , self.start_button.y ))

            restart_text = self.button_font.render("R", True, WHITE)
            self.screen.blit(restart_text, (self.restart_button.x, self.restart_button.y))

        quit_text = self.button_font.render("Q", True, WHITE)
        self.screen.blit(quit_text, (self.quit_button.x, self.quit_button.y))

        top3_text = self.button_font.render("3", True, WHITE)
        self.screen.blit(top3_text, (self.top3_button.x, self.top3_button.y))

        winner_text = self.button_font.render("Winner", True, WHITE)

        self.screen.blit(winner_text, (self.winner_button.x-50, self.winner_button.y))

        pygame.display.flip()


