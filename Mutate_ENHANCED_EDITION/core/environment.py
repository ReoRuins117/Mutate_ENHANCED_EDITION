# core/environment.py

class Environment:
    """
    Handles global simulation conditions:
    - Time of day
    - Wind
    - Fog
    - Weather effects
    """

    def __init__(self):
        self.time_of_day = 0.0  # 0–1
        self.time_speed = 0.001

        self.wind = (0.0, 0.0)
        self.fog_density = 0.0

    def tick(self):
        # Advance time of day
        self.time_of_day += self.time_speed
        if self.time_of_day > 1.0:
            self.time_of_day -= 1.0
