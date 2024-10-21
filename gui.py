import pygame
from horse import Horse

class GUI:
    def __init__(self):
        # Bildschirmgröße
        self.WIDTH, self.HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pferderennen")

        # Farben
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # Eingabefeld
        self.font = pygame.font.Font(None, 36)
        self.input_box = pygame.Rect(self.WIDTH // 2 - 200, self.HEIGHT - 100, 400, 32)
        self.input_text = ''
        self.active = False

        # Buttons
        self.button_font = pygame.font.Font(None, 48)
        self.start_button = pygame.Rect(self.WIDTH // 2 - 100, self.HEIGHT - 200, 200, 50)
        self.quit_button = pygame.Rect(self.WIDTH - 300, self.HEIGHT - 100, 200, 50)

        # Spielzustände
        self.game_started = False

        # Bilder laden
        self.bat_image = pygame.image.load('bat.png')
        self.bat_image = pygame.transform.scale(self.bat_image, (50, 30))

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
                    game.save_horses_to_json()

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    if self.game_started:
                        game.move_horse(self.input_text)
                    else:
                        game.add_horse(self.input_text)
                    self.input_text = ''  # Leere das Eingabefeld nach dem Hinzufügen
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

        return True

    def update_screen(self, game):
        self.screen.fill(self.WHITE)

        # Pferde zeichnen
        for horse in game.horses:
            self.screen.blit(self.bat_image, (horse["x_pos"], horse["y_pos"]))
            horse_name_text = self.font.render(horse["name"], True, self.BLACK)
            text_rect = horse_name_text.get_rect(center=(horse["x_pos"] + 25, horse["y_pos"] + 45))
            self.screen.blit(horse_name_text, text_rect)

        # Eingabefeld zeichnen
        txt_surface = self.font.render(self.input_text, True, self.BLACK)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.RED, self.input_box, 2)

        # Start-Button zeichnen
        if not self.game_started:
            pygame.draw.rect(self.screen, self.GREEN, self.start_button)
            start_text = self.button_font.render("Start", True, self.BLACK)
            self.screen.blit(start_text, (self.start_button.x + 50, self.start_button.y + 10))

        pygame.display.flip()
