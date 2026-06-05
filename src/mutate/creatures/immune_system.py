# creatures/immune_system.py

class ImmuneSystem:
    def __init__(self, immune_stats):
        # Store the immune genome block
        self.stats = immune_stats

        # Track active diseases
        self.active_diseases = []

    def tick(self, creature):
        # Heal a little each tick
        creature.health = min(
            creature.genome.basic.max_health,
            creature.health + self.stats.healing_rate
        )

        # Apply resistances to diseases
        for disease in list(self.active_diseases):
            disease.tick(creature)

            # If disease is resolved, remove it
            if disease.is_resolved():
                self.active_diseases.remove(disease)

    def infect(self, disease):
        # Apply resistance modifiers
        if disease.type in self.stats.resistances:
            disease.strength *= (1.0 - self.stats.resistances[disease.type])

        self.active_diseases.append(disease)
