from config import start_x,start_y, HEIGHT, amount_teams
class Horse:
    @staticmethod
    def create_horse(name, index):
        """
        Erstellt ein neues Pferd mit einem Namen und einer Y-Position basierend auf dem Index.
        """
        return {
            "name": name,
            "color": [200, 0, 0],  # Farbe des Pferdes
            "y_pos": start_y + index * (HEIGHT / amount_teams) ,  # Y-Position basierend auf der Anzahl der Pferde
            "x_pos": start_x,  # Startposition
            "points": 0
        }

    @staticmethod
    def from_dict(data):
        """
        Erstellt ein Horse-Objekt aus einem Dictionary (z.B. nach dem Laden aus JSON).
        """
        return {
            "name": data["name"],
            "color": data["color"],
            "y_pos": data["y_pos"],
            "x_pos": data["x_pos"],
            "points": data["points"]
        }
