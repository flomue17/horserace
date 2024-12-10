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

        # Farben

        # Eingabefeld
        self.font = pygame.font.Font(None, 36)
        self.input_box = pygame.Rect(10, HEIGHT - 75, 400, 32)
        self.input_text = ''
        self.active = False

        # Buttons
        self.button_font = pygame.font.Font(None, 48)
        self.start_button = pygame.Rect(250, HEIGHT - 75, 20, 32)
        self.restart_button = pygame.Rect(285, HEIGHT - 75, 20, 32)
        self.quit_button = pygame.Rect(320, HEIGHT - 75, 20, 32)

        # Spielzustände
        self.game_started = False

        # Bilder laden
        self.bat_image = pygame.image.load('bat.png')
        self.bat_image = pygame.transform.scale(self.bat_image, (130, 80))

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

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    if self.game_started:
                        horse_name, amount = self.input_text.split(",")

                        horse_name = horse_name.strip()  # Entfernt Leerzeichen
                        if not horse_name:
                            print("Der Pferdename darf nicht leer sein.")
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
        self.screen.blit(self.background_image, (0, 0))

        # Pferde zeichnen
        for index, horse in enumerate(game.horses):
            self.screen.blit(self.bat_image, (horse["x_pos"], start_y + start_y + index * (HEIGHT / amount_teams)))
            horse_name_text = self.font.render(horse["name"] + "," + str(horse["points"]), True, WHITE)
            text_rect = horse_name_text.get_rect(center=(horse["x_pos"] + 45, start_y + start_y + index * (HEIGHT / amount_teams) + 70))
            self.screen.blit(horse_name_text, text_rect)

        # Eingabefeld zeichnen
        txt_surface = self.font.render(self.input_text, True, BLACK)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, RED, self.input_box, 2)

        # Start-Button zeichnen
        if not self.game_started:
            pygame.draw.rect(self.screen, WHITE, self.start_button)
            start_text = self.button_font.render("S", True, BLACK)
            self.screen.blit(start_text, (self.start_button.x , self.start_button.y ))

            restart_text = self.button_font.render("R", True, BLACK)
            pygame.draw.rect(self.screen, WHITE, self.restart_button)
            self.screen.blit(restart_text, (self.restart_button.x, self.restart_button.y))

        quit_text = self.button_font.render("Q", True, BLACK)
        pygame.draw.rect(self.screen, WHITE, self.quit_button)
        self.screen.blit(quit_text, (self.quit_button.x, self.quit_button.y))
        pygame.display.flip()