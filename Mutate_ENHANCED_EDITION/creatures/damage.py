# creatures/damage.py

class DamageSystem:
    def __init__(self, damage_stats):
        # Store the damage genome block
        self.stats = damage_stats

    def apply_damage(self, creature, amount, damage_type=None):
        # Apply resistance if applicable
        if damage_type in self.stats.resistances:
            amount *= (1.0 - self.stats.resistances[damage_type])

        # Apply damage
        creature.health -= amount

        # Clamp health
        if creature.health <= 0:
            creature.health = 0
            creature.alive = False
