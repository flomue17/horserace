import sys

import pygame

class GUI:
    def __init__(self, screen, width, height):
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 48)

        # Eingabefeld und Buttons
        self.input_box_width = 400
        self.input_box_height = 32
        self.input_box = pygame.Rect(width // 2 - self.input_box_width // 2, height - 100, self.input_box_width, self.input_box_height)
        self.input_text = ''
        self.active = False

        self.start_button = pygame.Rect(width // 2 - 100, height - 200, 200, 50)
        self.quit_button = pygame.Rect(width - 300, height - 100, 200, 50)
        self.game_started = False

    def draw(self, screen):
        # Eingabefeld zeichnen
        txt_surface = self.font.render(self.input_text, True, (0, 0, 0))
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(screen, (255, 0, 0), self.input_box, 2)

        # Start-Button zeichnen, wenn das Spiel noch nicht gestartet ist
        if not self.game_started:
            pygame.draw.rect(screen, (0, 255, 0), self.start_button)
            start_text = self.button_font.render("Start", True, (0, 0, 0))
            screen.blit(start_text, (self.start_button.x + 50, self.start_button.y + 10))

        # Quit-Button zeichnen
        pygame.draw.rect(screen, (0, 255, 0), self.quit_button)
        quit_text = self.button_font.render("Quit", True, (0, 0, 0))
        screen.blit(quit_text, (self.quit_button.x + 50, self.quit_button.y + 10))

    def handle_event(self, event, game):
        # Überprüfe das Eingabefeld und die Buttons
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

            # Start-Button gedrückt
            if self.start_button.collidepoint(event.pos) and not self.game_started:
                game.start()  # Startet das Spiel
                self.game_started = True  # Aktualisiere den Status des Spiels

            # Quit-Button gedrückt
            if self.quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                # Nur im SETUP-Modus Pferde hinzufügen
                if not self.game_started and self.input_text.strip():
                    game.add_horse(self.input_text)
                    self.input_text = ''  # Textfeld nach Hinzufügen leeren

                # Im RUNNING-Modus Pferd bewegen
                elif self.game_started and self.input_text.strip():
                    horse_moved = game.move_horse(self.input_text)
                    if horse_moved:  # Nur Textfeld leeren, wenn das Pferd bewegt wurde
                        self.input_text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                self.input_text += event.unicode