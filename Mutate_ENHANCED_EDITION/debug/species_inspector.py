# debug/species_inspector.py

def print_species_template(species):
    print(f"\n=== Species Template: {species.name} ===")
    g = species.genome

    print("-- Basic Stats --")
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
