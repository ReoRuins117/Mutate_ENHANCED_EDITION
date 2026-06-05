# plants/plant_types.py

class PlantType:
    def __init__(self, name, growth_rate, max_size, terrain_preferences):
        self.name = name
        self.growth_rate = growth_rate
        self.max_size = max_size
        self.terrain_preferences = terrain_preferences
