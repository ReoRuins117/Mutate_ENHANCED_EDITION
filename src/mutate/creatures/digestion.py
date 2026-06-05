# creatures/digestion.py

class DigestionSystem:
    def __init__(self, digestive_stats):
        # Store the digestive genome block
        self.stats = digestive_stats

        # Digestion timer
        self.timer = 0

        # Food currently being digested (None or a food object)
        self.current_food = None

    def eat(self, food):
        # Start digestion
        self.current_food = food
        self.timer = self.stats.digestion_time

    def tick(self, creature):
        # No food being digested
        if self.current_food is None:
            return

        # Count down digestion
        self.timer -= 1

        # Finished digesting
        if self.timer <= 0:
            creature.energy = min(
                creature.genome.basic.energy_capacity,
                creature.energy + self.stats.energy_from_food
            )

            creature.health = min(
                creature.genome.basic.max_health,
                creature.health + self.stats.hp_from_food
            )

            # Clear stomach
            self.current_food = None
