# core/world.py

from utils.grid import Grid
from creatures.creature import Creature
from plants.plant_instance import Plant

class World:
    """
    The main backend world:
    - Terrain grid
    - Creature registry
    - Plant registry
    - Spatial queries
    - Raycasting hooks
    - Sound propagation hooks
    """

    def __init__(self, width, height, terrain_grid):
        self.width = width
        self.height = height

        self.terrain = terrain_grid
        self.grid = Grid(width, height)

        self.creatures = {}   # id -> Creature
        self.plants = []      # list of Plant
        self.next_id = 1
        self.next_creature_id = 1

    # --- Creature Management ---

    def add_creature(self, species, position):
        cid = self.next_creature_id
        self.next_creature_id += 1

        # Use the species template genome
        genome = species.genome

        c = Creature(species, genome, position)
        self.creatures[cid] = c
        return c
    
    def spawn_creature(self, species, genome, position):
        cid = self.next_creature_id
        self.next_creature_id += 1

        c = Creature(species, genome, position)
        self.creatures[cid] = c
        return c

    def remove_creature(self, creature):
        x, y = creature.position
        self.grid.remove_creature(creature, x, y)
        del self.creatures[creature.id]

    def move_creature(self, creature, new_pos):
        ox, oy = creature.position
        nx, ny = new_pos
        creature.position = (nx, ny)
        self.grid.move_creature(creature, (ox, oy), (nx, ny))

    # --- Plant Management ---

    def add_plant(self, plant):
        self.plants.append(plant)
        x, y = plant.position
        self.grid.add_plant(plant, x, y)

    # --- Spatial Queries ---

    def nearby_creatures(self, position, radius):
        px, py = position
        results = []
        r2 = radius * radius

        for c in self.creatures.values():
            cx, cy = c.position
            dx = cx - px
            dy = cy - py
            if dx*dx + dy*dy <= r2:
                results.append(c)

        return results

    def nearby_sounds(self, position, radius):
        # Placeholder — sound system added later
        return []

    # --- Raycasting (simple placeholder) ---

    def raycast(self, origin, direction, max_dist):
        """
        Very simple grid stepping raycast.
        Real optimization comes later.
        """
        ox, oy = origin
        dx, dy = direction

        steps = int(max_dist)
        x, y = ox, oy

        for _ in range(steps):
            x += dx
            y += dy

            ix, iy = int(x), int(y)
            if not self.grid.in_bounds(ix, iy):
                return ("out_of_bounds", (ix, iy))

            tile = self.terrain[ix][iy]
            if tile.blocks_sight:
                return ("blocked", (ix, iy))

        return ("clear", (int(x), int(y)))

    
    def tick(self):
        # Tick all creatures
        for c in self.creatures.values():
            c.tick_senses(self)
            c.tick_brain(self)
            c.tick_digestion()
            c.tick_diseases()
            c.tick_energy()
            c.tick_aging()

        # REMOVE DEAD CREATURES
        dead_ids = [cid for cid, c in self.creatures.items() if not c.is_alive()]
        for cid in dead_ids:
            del self.creatures[cid]

    def get_plant_at(self, position):
        for plant in self.plants:
            if plant.position == position:
                return plant
        return None

    def remove_plant(self, plant):
        self.plants.remove(plant)


