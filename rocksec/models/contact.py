# rocksec/models/contact.py

class Contact:
    def __init__(self, name="Unnamed Contact"):
        self.name = name
        self.points = []  # List of (distance, elevation)

    def add_point(self, distance, elevation):
        self.points.append((distance, elevation))

    def sorted_points(self):
        return sorted(self.points, key=lambda p: p[0])

    def __str__(self):
        return f"Contact {self.name} with {len(self.points)} points"
