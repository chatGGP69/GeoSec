# rocksec/models/rock_layer.py

class RockLayer:
    def __init__(self, top_contact, bottom_contact, rock_type):
        self.top_contact = top_contact  # Reference to Contact object
        self.bottom_contact = bottom_contact  # Reference to Contact object
        self.rock_type = rock_type

    def __str__(self):
        return f"RockLayer {self.rock_type} between {self.top_contact.name} and {self.bottom_contact.name}"
