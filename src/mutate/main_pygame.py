# main_pygame.py
import pygame
import time
import random

from mutate.config import (
    FRAME_RATE, BRAIN_INTERVAL,
    WORLD_WIDTH, WORLD_HEIGHT,
    INITIAL_CREATURES, INITIAL_PLANTS,
    TERRAIN_DEFAULT, WINDOW_WIDTH, WINDOW_HEIGHT
)

from mutate.core.world import World
from mutate.core.environment import Environment
from mutate.core.logging_system import Logger
from mutate.core.simulation import Simulation
from mutate.core.terrain import TerrainTile
from mutate.plants.plant_instance import Plant
from mutate.plants.plant_types import PlantType
from mutate.creatures.species_template import SpeciesTemplate
from mutate.creatures.genome import (
    Genome, BasicStats, SensoryStats, BrainParams,
    ImmuneStats, DigestiveParams, DamageParams,
    ColorProfile, SoundProfile
)

from mutate.ui.render import Renderer


def build_test_species():
    basic = BasicStats(
        speed=0.5,
        turn_rate=0.1,
        size=1.0,
        max_health=20,
        starting_health=20,
        lifespan=5000,
        metabolism=0.01,
        energy_capacity=20
    )

    sensory = SensoryStats(
        sight_fov=120,
        sight_range=10,
        sight_rays=5,
        sight_day_mod=1.0,
        sight_night_mod=0.5,
        hearing_range=8,
        hearing_bands=3,
        internal_state_inputs=["health", "energy", "age"],
        time_of_day_sensitivity=0.2
    )

    memory_capacity = 10

    input_size = (
        sensory.sight_rays +
        sensory.hearing_bands +
        len(sensory.internal_state_inputs) +
        memory_capacity
    )

    brain = BrainParams(
        master_shape=(input_size, 10, 3),
        subsystem_shapes=[
            (input_size, 10, 3),
            (input_size, 10, 3),
            (input_size, 10, 3)
        ],
        initial_weights={},
        learning_rate=0.01,
        plasticity=0.1,
        memory_capacity=memory_capacity,
        memory_decay=0.01,
        imprinting_strength=0.2
    )

    immune = ImmuneStats(
        resistances={},
        healing_rate=0.01,
        wound_penalty=0.0
    )

    digestive = DigestiveParams(
        edible_types=["plant"],
        food_tags=["meat"],
        digestion_time=30,
        energy_from_food=5,
        hp_from_food=1
    )

    damage = DamageParams(
        attacks=[],
        resistances={}
    )

    color = ColorProfile((100, 200, 100))
    sound = SoundProfile(5.0, 0.2, [1.0, 0.5, 0.2])

    genome = Genome(
        basic, sensory, brain, immune,
        digestive, damage, color, sound
    )

    return SpeciesTemplate("TestSpecies", genome)

def build_terrain(width, height):
    grid = []
    for x in range(width):
        col = []
        for y in range(height):
            col.append(TerrainTile(
                type=TERRAIN_DEFAULT,
                movement_cost=1.0,
                blocks_sight=False,
                blocks_sound=False
            ))
        grid.append(col)
    return grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Ecosystem Simulator (Backend + Pygame)")
    clock = pygame.time.Clock()

    terrain = build_terrain(WORLD_WIDTH, WORLD_HEIGHT)
    world = World(WORLD_WIDTH, WORLD_HEIGHT, terrain)
    env = Environment()
    logger = Logger()

    species = build_test_species()

    for _ in range(INITIAL_CREATURES):
        x = random.randint(0, WORLD_WIDTH - 1)
        y = random.randint(0, WORLD_HEIGHT - 1)
        world.add_creature(species, (x, y))

    plant_type = PlantType("Grass", growth_rate=0.01, max_size=3.0, terrain_preferences=["grass"])
    for _ in range(INITIAL_PLANTS):
        x = random.randint(0, WORLD_WIDTH - 1)
        y = random.randint(0, WORLD_HEIGHT - 1)
        world.add_plant(Plant(plant_type, (x, y)))

    sim = Simulation(world, env, logger, brain_interval=BRAIN_INTERVAL)
    renderer = Renderer(screen, world)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sim.tick()
        renderer.draw()

        clock.tick(FRAME_RATE)

    logger.export_text("sim_log.txt")
    pygame.quit()


if __name__ == "__main__":
    main()
