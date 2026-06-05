# creatures/creature.py
import random

from .senses import Senses
from .brain.master_brain import MasterBrain
from .brain.subsystem_brain import SubsystemBrain
from .brain.memory import Memory
from .digestion import DigestionSystem
from .immune_system import ImmuneSystem
from creatures.damage import DamageSystem

class Creature:
    """
    Core creature instance:
    - Holds genome and dynamic state
    - Wraps senses, digestion, immune, damage, brain, memory
    """

    _next_id = 1

    def __init__(self, species, genome, position):
        
        self.species = species
        self.genome = genome
        self.position = position

        from creatures.brain.nn_core import NeuralNetwork

        self.brain = NeuralNetwork(
            self.genome.brain.master_shape,
            self.genome.brain.initial_weights
        )

        self.id = Creature._next_id
        Creature._next_id += 1

        # --- Core state ---
        self.health = genome.basic.starting_health
        self.energy = genome.basic.energy_capacity * 0.5
        self.age = 0.0
        self.alive = True

        self.flags = {}
        self.diseases = []

        # --- Subsystems ---
        self.senses = Senses(genome.sensory)
        self.digestion = DigestionSystem(genome.digestive)
        self.immune = ImmuneSystem(genome.immune)
        self.damage_system = DamageSystem(genome.damage)

        # --- Memory ---
        self.memory = Memory(
            capacity=genome.brain.memory_capacity,
            decay=genome.brain.memory_decay
        )

        # --- Brain IO caches ---
        self._sight = []
        self._hearing = []
        self._internal = []

        # --- Brain selection output (movement etc.) ---
        self._action = [0.0, 0.0, 0.0]  # e.g. [move_x, move_y, extra]

        # Build brains AFTER everything else so we can compute input size
        self._build_brains()

    # ------------------------------------------------------------
    # Brain construction (auto-resizing)
    # ------------------------------------------------------------

    def _compute_brain_input_size(self):
        """
        Input vector is:
        - sight rays
        - hearing bands
        - internal state inputs
        - memory vector
        """
        sensory = self.genome.sensory
        brain = self.genome.brain

        return (
            sensory.sight_rays +
            sensory.hearing_bands +
            len(sensory.internal_state_inputs) +
            brain.memory_capacity
        )

    def _build_brains(self):
        """
        Build master and subsystem brains using the actual input size.
        This makes the system robust to changes in sensory counts or memory capacity.
        """
        input_size = self._compute_brain_input_size()
        brain_params = self.genome.brain

        # Master brain
        master_shape = (input_size, brain_params.master_shape[1], brain_params.master_shape[2])

        # Subsystem shapes (we keep same hidden/output sizes, but fix input)
        subsystem_shapes = []
        for shape in brain_params.subsystem_shapes:
            subsystem_shapes.append((input_size, shape[1], shape[2]))

        # Create a shallow copy of brain_params with corrected shapes
        from creatures.genome import BrainParams
        fixed_brain_params = BrainParams(
            master_shape=master_shape,
            subsystem_shapes=subsystem_shapes,
            initial_weights=None,  # force fresh weights to match new shapes
            learning_rate=brain_params.learning_rate,
            plasticity=brain_params.plasticity,
            memory_capacity=brain_params.memory_capacity,
            memory_decay=brain_params.memory_decay,
            imprinting_strength=brain_params.imprinting_strength
        )

        self.master_brain = MasterBrain(fixed_brain_params)
        self.sub_brains = [
            SubsystemBrain(shape) for shape in subsystem_shapes
        ]

    # ------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------

    def is_alive(self):
        return self.alive and self.health > 0 and self.age < self.genome.basic.lifespan

    # ------------------------------------------------------------
    # Ticks
    # ------------------------------------------------------------

    def tick_senses(self, world):
        """
        Update sensory inputs.
        """
        self._sight = self.senses.compute_sight(self, world)
        self._hearing = self.senses.compute_hearing(self, world)
        self._internal = self._compute_internal_state()

    def tick_brain(self, world):
        """
        Run master brain + chosen subsystem, produce action vector.
        """
        if not self.is_alive():
            self._action = [0.0, 0.0, 0.0]
            return

        # Build input vector
        mem_vec = self.memory.get_vector()
        inputs = self.collect_inputs(world)
        output = self.brain.forward(inputs)
        self._action = output

        # Safety: if sizes drift for any reason, rebuild brains
        expected_size = self._compute_brain_input_size()
        if len(inputs) != expected_size:
            # Rebuild brains to match new configuration
            self._build_brains()

        # Master brain chooses subsystem
        subsystem_index = self.master_brain.choose_subsystem(inputs)
        subsystem_index = max(0, min(subsystem_index, len(self.sub_brains) - 1))

        # Subsystem produces action
        action = self.sub_brains[subsystem_index].compute_action(inputs)
        self._action = action

        # Optionally update memory from inputs or action
        self.memory.update(inputs)

        self.apply_action(world)

    def tick_digestion(self):
        self.digestion.tick(self)

    def tick_diseases(self):
        for d in list(self.diseases):
            d.tick(self)
            if d.is_resolved():
                self.diseases.remove(d)

    def tick_energy(self):
        # Basic metabolism
        self.energy -= self.genome.basic.metabolism
        if self.energy < 0:
            self.energy = 0
            self.health -= 0.1  # starvation penalty

    def tick_aging(self):
        self.age += 1.0
        if self.age >= self.genome.basic.lifespan:
            self.alive = False

    # ------------------------------------------------------------
    # Internal state vector
    # ------------------------------------------------------------

    def _compute_internal_state(self):
        """
        Build internal state vector based on genome.sensory.internal_state_inputs.
        Example keys: "health", "energy", "age"
        """
        out = []
        for key in self.genome.sensory.internal_state_inputs:
            if key == "health":
                out.append(self.health / max(1.0, self.genome.basic.max_health))
            elif key == "energy":
                out.append(self.energy / max(1.0, self.genome.basic.energy_capacity))
            elif key == "age":
                out.append(self.age / max(1.0, self.genome.basic.lifespan))
            else:
                out.append(0.0)
        return out

    # ------------------------------------------------------------
    # Damage / healing
    # ------------------------------------------------------------

    def apply_damage(self, amount, damage_type=None):
        self.damage_system.apply_damage(self, amount, damage_type)

    def heal(self, amount):
        self.health = min(self.genome.basic.max_health, self.health + amount)

    def apply_action(self):
        mx, my, eat = self._action

        # Movement
        self.position = (
            self.position[0] + mx * 0.5,
            self.position[1] + my * 0.5
        )

        # Eating
        if eat > 0.5:
            plant = self.world.get_plant_at(self.position)
            if plant:
                self.digestion.eat(plant)
                self.world.remove_plant(plant)

    def try_reproduce(self, world):
        if self.energy > self.genome.basic.energy_capacity * 0.8:
            child_genome = self.genome.mutate()
            world.spawn_creature(self.species, child_genome, self.position)
            self.energy *= 0.5

    def apply_action(self, world):
        mx, my, eat = self._action

        # Smooth movement
        speed = self.genome.basic.speed
        self.position = (
            self.position[0] + mx * speed,
            self.position[1] + my * speed
        )

        # Eating
        if eat > 0.5:
            plant = world.get_plant_at(self.position)
            if plant:
                self.digestion.eat(plant)
                world.remove_plant(plant)

    def collect_inputs(self, world):
        inputs = []

        # 1. Internal state
        inputs.append(self.health / self.genome.basic.max_health)
        inputs.append(self.energy / self.genome.basic.energy_capacity)

        # 2. Memory
        if hasattr(self, "memory"):
            inputs.extend(self.memory.get_vector())
        else:
            inputs.extend([0.0] * self.genome.brain.memory_capacity)

        # 3. Sight rays (placeholder for now)
        sight_count = self.genome.sensory.sight_rays
        inputs.extend([0.0] * sight_count)

        # 4. Hearing (placeholder)
        hearing_count = self.genome.sensory.hearing_bands
        inputs.extend([0.0] * hearing_count)

        # 5. Tiny noise to break symmetry
        inputs.append(random.uniform(-0.05, 0.05))

        return inputs


