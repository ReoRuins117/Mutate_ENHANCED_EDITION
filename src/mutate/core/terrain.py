# core/terrain.py

class TerrainTile:
    def __init__(self, type, movement_cost, blocks_sight, blocks_sound):
        self.type = type
        self.movement_cost = movement_cost
        self.blocks_sight = blocks_sight
        self.blocks_sound = blocks_sound
