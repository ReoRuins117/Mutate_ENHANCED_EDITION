# creatures/species_template.py

class SpeciesTemplate:
    def __init__(self, name: str, genome, special_behaviors=None):
        self.name = name
        self.genome = genome
        self.special_behaviors = special_behaviors or []
