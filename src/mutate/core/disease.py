# core/disease.py

class DiseaseDefinition:
    def __init__(self, id, incubation, damage_per_tick, contagiousness):
        self.id = id
        self.incubation = incubation
        self.damage_per_tick = damage_per_tick
        self.contagiousness = contagiousness


class DiseaseInstance:
    def __init__(self, definition):
        self.definition = definition
        self.timer = 0

    def tick(self, creature):
        self.timer += 1

        if self.timer > self.definition.incubation:
            creature.health -= self.definition.damage_per_tick
