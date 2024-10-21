import json
from horse import Horse

class Game:
    def __init__(self):
        # Pferdeliste wird initial leer gehalten
        self.horses = []

    def add_horse(self, name):
        # Füge ein neues Pferd mit einem Namen hinzu
        horse = Horse.create_horse(name, len(self.horses))
        self.horses.append(horse)

    def move_horse(self, horse_name):
        # Bewege ein Pferd, basierend auf seinem Namen
        for horse in self.horses:
            if horse["name"] == horse_name:
                horse["x_pos"] += Horse.get_step_distance()

    def save_horses_to_json(self, horses, file):
        # Speichere die Pferde in eine JSON-Datei
        with open(file, "w") as f:
            json.dump({"horses": horses}, f)

    def load_horses_from_json(self, file):
        # Lade Pferde aus einer JSON-Datei
        with open(file, "r") as f:
            data = json.load(f)
            return data["horses"]

    def reset_horses(self):
        tmp_horses = self.load_horses_from_json("blank.json")
        self.save_horses_to_json(tmp_horses, "horses.json")
        self.load_horses_from_json("horses.json")

    def check_winner(self, goal_x):
        # Überprüfen, ob ein Pferd das Ziel erreicht hat
        for horse in self.horses:
            if horse["x_pos"] >= goal_x:
                return horse["name"]
        return None
