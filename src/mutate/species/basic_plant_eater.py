from creatures.genome import (
    BasicStats, SensoryStats, DigestiveStats,
    ImmuneStats, DamageStats, BrainParams, SpeciesGenome
)

def make_basic_plant_eater():
    return SpeciesGenome(
        basic=BasicStats(
            starting_health=50,
            max_health=50,
            energy_capacity=100,
            metabolism=0.05,
            lifespan=5000
        ),

        sensory=SensoryStats(
            sight_rays=5,
            hearing_bands=0,
            internal_state_inputs=["health", "energy"],
        ),

        digestive=DigestiveStats(
            digestion_time=20,
            energy_from_food=30,
            hp_from_food=5
        ),

        immune=ImmuneStats(
            healing_rate=0.01,
            resistances={}
        ),

        damage=DamageStats(
            resistances={}
        ),

        brain=BrainParams(
            master_shape=(7, 8, 3),      # 7 inputs → 8 hidden → 3 outputs
            subsystem_shapes=[(7, 6, 3)],
            learning_rate=0.01,
            plasticity=0.1,
            memory_capacity=2,
            memory_decay=0.1,
            imprinting_strength=0.0,
            initial_weights=None
        )
    )
