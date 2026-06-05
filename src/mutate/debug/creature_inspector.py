# debug/creature_inspector.py

def print_creature(creature):
    g = creature.genome

    print(f"\n=== Creature {creature.id} ({creature.species.name}) ===")
    print(f"Position: {creature.position}")
    print(f"Health: {creature.health:.2f}/{g.basic.max_health}")
    print(f"Energy: {creature.energy:.2f}/{g.basic.energy_capacity}")
    print(f"Age: {creature.age:.2f}/{g.basic.lifespan}")
    print(f"Diseases: {[d.definition.id for d in creature.diseases]}")
    print(f"Flags: {creature.flags}")

    print("\n-- Basic Stats --")
    for k, v in vars(g.basic).items():
        print(f"{k}: {v}")

    print("\n-- Sensory Stats --")
    for k, v in vars(g.sensory).items():
        print(f"{k}: {v}")

    print("\n-- Brain Params --")
    for k, v in vars(g.brain).items():
        if k == "initial_weights":
            print("initial_weights: <weights omitted>")
        else:
            print(f"{k}: {v}")

    print("\n-- Immune Stats --")
    for k, v in vars(g.immune).items():
        print(f"{k}: {v}")

    print("\n-- Digestive Params --")
    for k, v in vars(g.digestive).items():
        print(f"{k}: {v}")

    print("\n-- Damage Params --")
    for k, v in vars(g.damage).items():
        print(f"{k}: {v}")

    print("\n-- Color Profile --")
    print(g.color.rgb)

    print("\n-- Sound Profile --")
    for k, v in vars(g.sound).items():
        print(f"{k}: {v}")

    print("====================================\n")
