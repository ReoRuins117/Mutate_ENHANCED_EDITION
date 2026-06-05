# creatures/senses.py

class Senses:
    def __init__(self, sensory_stats):
        self.stats = sensory_stats
    def compute_sight(self, creature, world):
        """
        Returns a placeholder list of sight ray results.
        Real raycasting is implemented in Step 4 (world/grid).
        """
        return [0.0] * int(creature.genome.sensory.sight_rays)

    def compute_hearing(self, creature, world):
        """
        Returns placeholder hearing data.
        Real sound propagation comes in Step 4.
        """
        return [0.0] * creature.genome.sensory.hearing_bands

    def compute_internal_state(self, creature):
        """
        Converts creature internal state into a vector for the brain.
        """
        state = []
        for key in creature.genome.sensory.internal_state_inputs:
            if key == "health":
                state.append(creature.health / creature.genome.basic.max_health)
            elif key == "energy":
                state.append(creature.energy / creature.genome.basic.energy_capacity)
            elif key == "age":
                state.append(creature.age / creature.genome.basic.lifespan)
            else:
                state.append(0.0)
        return state
