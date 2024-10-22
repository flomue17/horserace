import pygame
import sys

from config import goal_x
from game import Game
from gui import GUI

def main():
    pygame.init()

    # Erstelle das GUI und Game-Objekt
    gui = GUI()
    game = Game()
    game.horses = game.load_horses_from_json("horses.json")
    # Starte das Spiel
    running = True
    while running:
        running = gui.handle_events(game)
        gui.update_screen(game)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
