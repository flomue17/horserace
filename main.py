import pygame
import sys
from gui import GUI
from game import Game

def main():
    pygame.init()

    # Bildschirmgröße definieren
    WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pferderennen")

    # Initialisiere GUI und Game
    gui = GUI(screen, WIDTH, HEIGHT)
    game = Game(WIDTH, HEIGHT)

    # Hauptschleife
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill((255, 255, 255))  # Weißer Hintergrund

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Übergabe des Events an die GUI und das Spiel
            gui.handle_event(event, game)
            game.handle_event(event, gui)

        # Zeichnen der Pferde und GUI
        game.draw(screen)
        gui.draw(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
