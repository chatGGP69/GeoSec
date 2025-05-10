# rocksec/models/topography.py

class Topography:
    def __init__(self):
        self.points = []  # List of (distance, elevation)

    def add_point(self, distance, elevation):
        self.points.append((distance, elevation))

    def get_profile(self):
        distances = [d for d, e in self.points]
        elevations = [e for d, e in self.points]
        return distances, elevations

    def sorted_points(self):
        return sorted(self.points, key=lambda p: p[0])

    def clear(self):
        self.points.clear()

    def __str__(self):
        return f"Topography with {len(self.points)} points"
