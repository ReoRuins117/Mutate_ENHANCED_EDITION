# core/simulation.py

import random
import math

class Simulation:
    """
    Runs the backend simulation:
    - Environment tick
    - Creature senses
    - Brain (every N frames)
    - Movement
    - Digestion
    - Diseases
    - Aging
    - Reproduction
    - Mutation
    - Plant growth
    """

    def __init__(self, world, environment, logger, brain_interval=3):
        self.world = world
        self.environment = environment
        self.logger = logger
        self.frame = 0
        self.brain_interval = brain_interval

    def tick(self):
        self.world.tick()
        self.logger.set_sim_time(self.frame)
        self.frame += 1
        self.environment.tick()

        dead = []
        newborns = []

        # --- Creature Loop ---
        for creature in list(self.world.creatures.values()):
            # 1. Senses
            creature.tick_senses(self.world)

            # 2. Brain (every N frames)
            if self.frame % self.brain_interval == 0:
                creature.tick_brain(self.world)

            # 3. Movement
            self._apply_movement(creature)

            # 4. Digestion
            creature.tick_digestion()

            # 5. Diseases
            creature.tick_diseases()

            # 6. Energy & aging
            creature.tick_energy()
            creature.tick_aging()

            # 7. Reproduction
            baby = self._try_reproduce(creature)
            if baby:
                newborns.append(baby)

            # 8. Death check
            if not creature.is_alive():
                dead.append(creature)

        # Remove dead creatures
        for d in dead:
            self.world.remove_creature(d)
            self.logger.log("CREATURE_LIFE", "death", d)

        # Add newborns
        for b in newborns:
            self.logger.log("CREATURE_LIFE", "birth", b)

        # --- Plant Loop ---
        for plant in self.world.plants:
            self._tick_plant(plant)


    # ------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------

    def _apply_movement(self, creature):
        """
        Uses the creature's last brain action vector to move it.
        """
        if not hasattr(creature, "_action"):
            return

        ax, ay = creature._action[:2] if len(creature._action) >= 2 else (0, 0)

        # Apply speed
        speed = creature.genome.basic.speed
        vx = ax * speed
        vy = ay * speed

        # Apply wind penalty
        wx, wy = self.environment.wind
        vx -= wx * 0.1
        vy -= wy * 0.1

        # New position
        x, y = creature.position
        nx = x + vx
        ny = y + vy

        # Clamp to world
        nx = max(0, min(self.world.width - 1, nx))
        ny = max(0, min(self.world.height - 1, ny))

        # Terrain movement cost
        tile = self.world.terrain[int(nx)][int(ny)]
        if tile.movement_cost > 1.0:
            # Slow movement
            nx = x + vx / tile.movement_cost
            ny = y + vy / tile.movement_cost

        # Update world grid
        self.world.move_creature(creature, (int(nx), int(ny)))

    # ------------------------------------------------------------
    # Reproduction & Mutation
    # ------------------------------------------------------------

    def _try_reproduce(self, creature):
        """
        Simple reproduction rule:
        - If energy is high enough, spawn a child
        - Apply mutation to genome
        """
        if creature.energy < creature.genome.basic.energy_capacity * 0.8:
            return None

        # Energy cost
        creature.energy *= 0.5

        # Create mutated genome
        mutated_genome = self._mutate_genome(creature.genome)

        # Create new species template (same species name)
        from creatures.species_template import SpeciesTemplate
        baby_species = SpeciesTemplate(creature.species.name, mutated_genome)

        # Spawn near parent
        x, y = creature.position
        bx = max(0, min(self.world.width - 1, x + random.randint(-1, 1)))
        by = max(0, min(self.world.height - 1, y + random.randint(-1, 1)))

        baby = self.world.add_creature(baby_species, (bx, by))
        return baby

    def _mutate_genome(self, genome):
        import copy
        new = copy.deepcopy(genome)

        # Helper: mutate floats
        def mutate_float(v, scale=0.05):
            return v + random.gauss(0, abs(v) * scale)

        # Helper: mutate ints safely
        def mutate_int(v, scale=0.05, minimum=1):
            mutated = int(round(v + random.gauss(0, abs(v) * scale)))
            return max(minimum, mutated)

        # ------------------------------------------------------------
        # Basic Stats (all floats)
        # ------------------------------------------------------------
        for attr in vars(new.basic):
            val = getattr(new.basic, attr)
            if isinstance(val, (int, float)):
                setattr(new.basic, attr, mutate_float(val))

        # ------------------------------------------------------------
        # Sensory Stats
        # ------------------------------------------------------------
        # Floats
        float_fields = [
            "sight_fov", "sight_range",
            "sight_day_mod", "sight_night_mod",
            "hearing_range", "time_of_day_sensitivity"
        ]
        for attr in float_fields:
            val = getattr(new.sensory, attr)
            setattr(new.sensory, attr, mutate_float(val))

        # Int fields (must stay >= 1)
        int_fields = ["sight_rays", "hearing_bands"]
        for attr in int_fields:
            val = getattr(new.sensory, attr)
            setattr(new.sensory, attr, mutate_int(val, minimum=1))

        # ------------------------------------------------------------
        # Brain Params
        # ------------------------------------------------------------
        # Mutate learning rate, plasticity, imprinting
        new.brain.learning_rate = mutate_float(new.brain.learning_rate)
        new.brain.plasticity = mutate_float(new.brain.plasticity)
        new.brain.imprinting_strength = mutate_float(new.brain.imprinting_strength)

        # Memory capacity must stay integer >= 1
        new.brain.memory_capacity = mutate_int(new.brain.memory_capacity, minimum=1)

        # Mutate neural network weights
        for key, weight_list in new.brain.initial_weights.items():
            for w in weight_list:
                w += random.gauss(0, 0.1)

        # ------------------------------------------------------------
        # Immune Stats
        # ------------------------------------------------------------
        new.immune.healing_rate = mutate_float(new.immune.healing_rate)
        new.immune.wound_penalty = mutate_float(new.immune.wound_penalty)

        # Resistances (floats between 0 and 1)
        for k, v in new.immune.resistances.items():
            mutated = mutate_float(v)
            new.immune.resistances[k] = max(0.0, min(1.0, mutated))

        # ------------------------------------------------------------
        # Digestive Params
        # ------------------------------------------------------------
        new.digestive.digestion_time = mutate_int(new.digestive.digestion_time, minimum=1)
        new.digestive.energy_from_food = mutate_float(new.digestive.energy_from_food)
        new.digestive.hp_from_food = mutate_float(new.digestive.hp_from_food)

        # ------------------------------------------------------------
        # Damage Params
        # ------------------------------------------------------------
        for k, v in new.damage.resistances.items():
            mutated = mutate_float(v)
            new.damage.resistances[k] = max(0.0, min(1.0, mutated))

        # Attacks are left unchanged for now (can mutate later)

        return new


    # ------------------------------------------------------------
    # Plant Growth
    # ------------------------------------------------------------

    def _tick_plant(self, plant):
        """
        Plants grow slowly and may spread.
        """
        plant.size += plant.type.growth_rate
        if plant.size > plant.type.max_size:
            plant.size = plant.type.max_size

        # Spread chance
        if random.random() < 0.001:
            x, y = plant.position
            nx = max(0, min(self.world.width - 1, x + random.randint(-1, 1)))
            ny = max(0, min(self.world.height - 1, y + random.randint(-1, 1)))

            from plants.plant_instance import Plant
            new_plant = Plant(plant.type, (nx, ny))
            self.world.add_plant(new_plant)
