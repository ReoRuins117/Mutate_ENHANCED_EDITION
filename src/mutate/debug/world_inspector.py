# debug/world_inspector.py

def print_world_summary(world):
    print("\n=== World Summary ===")
    print(f"Size: {world.width} x {world.height}")
    print(f"Creatures: {len(world.creatures)}")
    print(f"Plants: {len(world.plants)}")
    print("======================\n")


def print_creatures_near(world, pos, radius):
    print(f"\nCreatures near {pos} (r={radius}):")
    for c in world.nearby_creatures(pos, radius):
        print(f" - ID {c.id} ({c.species.name}) at {c.position}")
    print()
