# utils/grid.py

class Grid:
    """
    A simple 2D grid wrapper for terrain, creatures, and plants.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Each cell holds lists of creature IDs and plant references
        self.creatures = [[[] for _ in range(height)] for _ in range(width)]
        self.plants = [[[] for _ in range(height)] for _ in range(width)]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def add_creature(self, creature, x, y):
        if self.in_bounds(x, y):
            self.creatures[x][y].append(creature.id)

    def remove_creature(self, creature, x, y):
        if self.in_bounds(x, y):
            if creature.id in self.creatures[x][y]:
                self.creatures[x][y].remove(creature.id)

    def move_creature(self, creature, old_pos, new_pos):
        ox, oy = old_pos
        nx, ny = new_pos
        self.remove_creature(creature, ox, oy)
        self.add_creature(creature, nx, ny)

    def add_plant(self, plant, x, y):
        if self.in_bounds(x, y):
            self.plants[x][y].append(plant)
