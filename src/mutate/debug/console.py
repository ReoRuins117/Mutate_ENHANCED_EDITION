# debug/console.py

from debug.creature_inspector import print_creature
from debug.world_inspector import print_world_summary, print_creatures_near
from debug.species_inspector import print_species_template

class DebugConsole:
    """
    A simple backend REPL for interacting with the simulation.
    Commands:
      help
      list
      inspect <id>
      near <x> <y> <r>
      species
      tick <n>
      spawn <x> <y>
      quit
    """

    def __init__(self, sim, world, species):
        self.sim = sim
        self.world = world
        self.species = species

    def run(self):
        print("\n=== Debug Console ===")
        print("Type 'help' for commands.\n")

        while True:
            cmd = input("> ").strip().split()

            if not cmd:
                continue

            if cmd[0] == "help":
                print("Commands:")
                print("  list                - list all creatures")
                print("  inspect <id>        - inspect creature")
                print("  near <x> <y> <r>    - list creatures near point")
                print("  species             - print species template")
                print("  tick <n>            - advance simulation n ticks")
                print("  spawn <x> <y>       - spawn a new creature")
                print("  quit                - exit console")

            elif cmd[0] == "list":
                print_world_summary(self.world)
                for c in self.world.creatures.values():
                    print(f"ID {c.id} ({c.species.name}) at {c.position}")

            elif cmd[0] == "inspect" and len(cmd) == 2:
                cid = int(cmd[1])
                if cid in self.world.creatures:
                    print_creature(self.world.creatures[cid])
                else:
                    print("Creature not found.")

            elif cmd[0] == "near" and len(cmd) == 4:
                x, y, r = map(int, cmd[1:])
                print_creatures_near(self.world, (x, y), r)

            elif cmd[0] == "species":
                print_species_template(self.species)

            elif cmd[0] == "tick" and len(cmd) == 2:
                n = int(cmd[1])
                for _ in range(n):
                    self.sim.tick()
                print(f"Advanced {n} ticks.")

            elif cmd[0] == "spawn" and len(cmd) == 3:
                x, y = map(int, cmd[1:])
                baby = self.world.add_creature(self.species, (x, y))
                print(f"Spawned creature {baby.id} at {(x, y)}")

            elif cmd[0] == "quit":
                print("Exiting debug console.")
                break

            else:
                print("Unknown command. Type 'help'.")
