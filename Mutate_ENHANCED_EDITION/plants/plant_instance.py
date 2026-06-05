# plants/plant_instance.py

class Plant:
    def __init__(self, plant_type, position):
        self.type = plant_type
        self.position = position
        self.size = 1.0
        self.health = 1.0

    def tick(self, world):
        # Implementation added later
        ...
