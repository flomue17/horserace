import json
from config import step_size, goal_x, amount_points, start_x

from horse import Horse

class Game:
    def __init__(self):
        # Pferdeliste wird initial leer gehalten
        self.horses = []

    def add_horse(self, name):
        # Füge ein neues Pferd mit einem Namen hinzu
        horse = Horse.create_horse(name, len(self.horses))
        self.horses.append(horse)

    def move_horse(self, horse_name, size):
        # Bewege ein Pferd, basierend auf seinem Namen
        for horse in self.horses:
            if horse["name"] == horse_name:
                horse["x_pos"] += size * step_size

                if horse["x_pos"] > goal_x:
                    horse["x_pos"] = goal_x
                if horse["x_pos"] < start_x:
                    horse["x_pos"] = start_x

                horse["points"] += size

                if horse["points"] > amount_points:
                    horse["points"] = amount_points
                if horse["points"] < 0:
                    horse["points"] = 0

    def save_horses_to_json(self, horses, file):
        # Speichere die Pferde in eine JSON-Datei
        with open(file, "w") as f:
            json.dump({"horses": horses}, f)

    def load_horses_from_json(self, file):
        # Lade Pferde aus einer JSON-Datei
        with open(file, "r") as f:
            data = json.load(f)
            return data["horses"]

    def sort_horses(self):
        self.horses = sorted(self.horses, key=lambda horse: -horse["points"])

    def reset_horses(self):
        self.save_horses_to_json([], "horses.json")
        self.horses = self.load_horses_from_json("horses.json")

    def check_winner(self, goal_x):
        # Überprüfen, ob ein Pferd das Ziel erreicht hat
        for horse in self.horses:
            if horse["x_pos"] >= goal_x:
                return horse["name"]
        return None
