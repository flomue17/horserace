import json
import sys

import pygame
from horse import Horse

class Game:
    def __init__(self, width, height):
        self.start_x = 50
        self.goal_x = width - 100
        self.goal_size = 8
        self.horses = []
        self.font = pygame.font.Font(None, 36)

        # Fledermaus-Bild laden
        self.bat_image = pygame.image.load('bat.png')
        self.bat_image = pygame.transform.scale(self.bat_image, (50, 30))

        self.game_running = False  # Status, ob das Spiel läuft

    def start(self):
        print("Das Rennen hat begonnen!")
        self.save_horses_to_json()
        self.game_running = True  # Setze das Spiel auf laufend

    def add_horse(self, name):
        if not self.game_running:  # Nur Pferde hinzufügen, wenn das Spiel nicht läuft
            y_pos = 50 + len(self.horses) * 100  # Bestimme die Position des Pferds
            horse = Horse(name, y_pos, self.start_x, self.bat_image)
            self.horses.append(horse)

    def draw(self, screen):
        # Zeichne jedes Pferd
        for horse in self.horses:
            horse.draw(screen, self.font)

    def move_horse(self, name):
        step_distance = (self.goal_x - self.start_x) / self.goal_size
        horse_moved = False
        for horse in self.horses:
            if horse.name == name:
                horse.move(step_distance)
                horse_moved = True  # Pferd wurde bewegt
                break
        return horse_moved  # Gibt zurück, ob das Pferd bewegt wurde

    def save_horses_to_json(self):
        # Speichern der Pferdedaten in einer JSON-Datei
        horse_data = [{"name": horse.name, "x_pos": horse.x_pos, "y_pos": horse.y_pos} for horse in self.horses]
        with open("horses.json", "w") as f:
            json.dump({"horses": horse_data}, f)

    def handle_event(self, event, gui):
        if self.game_running:
            # Überprüfe, ob ein Pferd das Ziel erreicht hat
            for horse in self.horses:
                if horse.x_pos >= self.goal_x:
                    print(f"{horse.name} hat das Rennen gewonnen!")
                    pygame.quit()
                    sys.exit()
