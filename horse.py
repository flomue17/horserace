class Horse:
    @staticmethod
    def create_horse(name, index):
        """
        Erstellt ein neues Pferd mit einem Namen und einer Y-Position basierend auf dem Index.
        """
        return {
            "name": name,
            "color": [200, 0, 0],  # Farbe des Pferdes
            "y_pos": 50 + index * 100,  # Y-Position basierend auf der Anzahl der Pferde
            "x_pos": 50  # Startposition
        }

    @staticmethod
    def get_step_distance():
        """
        Berechnet die Schrittweite, die das Pferd bei jedem Zug vorankommt.
        """
        return 10  # Beispielsweise, passe diesen Wert nach Belieben an

    @staticmethod
    def from_dict(data):
        """
        Erstellt ein Horse-Objekt aus einem Dictionary (z.B. nach dem Laden aus JSON).
        """
        return {
            "name": data["name"],
            "color": data["color"],
            "y_pos": data["y_pos"],
            "x_pos": data["x_pos"]
        }
