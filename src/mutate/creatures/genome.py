# creatures/genome.py

class BasicStats:
    def __init__(
        self,
        speed: float,
        turn_rate: float,
        size: float,
        max_health: float,
        starting_health: float,
        lifespan: float,
        metabolism: float,
        energy_capacity: float,
    ):
        self.speed = speed
        self.turn_rate = turn_rate
        self.size = size
        self.max_health = max_health
        self.starting_health = starting_health
        self.lifespan = lifespan
        self.metabolism = metabolism
        self.energy_capacity = energy_capacity


class SensoryStats:
    def __init__(
        self,
        sight_fov: float,
        sight_range: float,
        sight_rays: int,
        sight_day_mod: float,
        sight_night_mod: float,
        hearing_range: float,
        hearing_bands: int,
        internal_state_inputs: list,
        time_of_day_sensitivity: float,
    ):
        self.sight_fov = sight_fov
        self.sight_range = sight_range
        self.sight_rays = sight_rays
        self.sight_day_mod = sight_day_mod
        self.sight_night_mod = sight_night_mod
        self.hearing_range = hearing_range
        self.hearing_bands = hearing_bands
        self.internal_state_inputs = internal_state_inputs
        self.time_of_day_sensitivity = time_of_day_sensitivity


class BrainParams:
    def __init__(
        self,
        master_shape: tuple,
        subsystem_shapes: list,
        initial_weights: dict,
        learning_rate: float,
        plasticity: float,
        memory_capacity: int,
        memory_decay: float,
        imprinting_strength: float,
    ):
        self.master_shape = master_shape
        self.subsystem_shapes = subsystem_shapes
        self.initial_weights = initial_weights
        self.learning_rate = learning_rate
        self.plasticity = plasticity
        self.memory_capacity = memory_capacity
        self.memory_decay = memory_decay
        self.imprinting_strength = imprinting_strength


class ImmuneStats:
    def __init__(
        self,
        resistances: dict,
        healing_rate: float,
        wound_penalty: float,
    ):
        self.resistances = resistances
        self.healing_rate = healing_rate
        self.wound_penalty = wound_penalty


class DigestiveParams:
    def __init__(
        self,
        edible_types: list,
        food_tags: list,
        digestion_time: float,
        energy_from_food: float,
        hp_from_food: float,
    ):
        self.edible_types = edible_types
        self.food_tags = food_tags
        self.digestion_time = digestion_time
        self.energy_from_food = energy_from_food
        self.hp_from_food = hp_from_food


class DamageParams:
    def __init__(
        self,
        attacks: list,
        resistances: dict,
    ):
        self.attacks = attacks
        self.resistances = resistances


class ColorProfile:
    def __init__(self, rgb: tuple):
        self.rgb = rgb


class SoundProfile:
    def __init__(
        self,
        emission_range: float,
        movement_sound_level: float,
        hearing_profile: list,
    ):
        self.emission_range = emission_range
        self.movement_sound_level = movement_sound_level
        self.hearing_profile = hearing_profile


class Genome:
    def __init__(
        self,
        basic_stats: BasicStats,
        sensory_stats: SensoryStats,
        brain_params: BrainParams,
        immune_stats: ImmuneStats,
        digestive_params: DigestiveParams,
        damage_params: DamageParams,
        color_profile: ColorProfile,
        sound_profile: SoundProfile,
    ):
        self.basic = basic_stats
        self.sensory = sensory_stats
        self.brain = brain_params
        self.immune = immune_stats
        self.digestive = digestive_params
        self.damage = damage_params
        self.color = color_profile
        self.sound = sound_profile

    def mutate(self):
        import copy, random
        child = copy.deepcopy(self)

        # Example mutations
        child.basic.metabolism *= random.uniform(0.95, 1.05)
        child.sensory.sight_rays = max(1, int(child.sensory.sight_rays + random.choice([-1, 0, 1])))

        # You can mutate brain weights inside the NN class later

        return child

