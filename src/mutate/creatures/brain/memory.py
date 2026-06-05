# creatures/brain/memory.py

import numpy as np

class Memory:
    def __init__(self, capacity, decay):
        self.capacity = capacity
        self.decay = decay

        # Initialize memory vector
        self.vector = np.zeros(capacity, dtype=float)

    def update(self, inputs):
        """
        Simple memory mechanism:
        - Blend new inputs into memory
        - Apply decay
        - Keep only the first N values if inputs are longer
        """

        # Convert to numpy
        inputs = np.array(inputs, dtype=float)

        # Resize or crop inputs to match memory capacity
        if len(inputs) >= self.capacity:
            new_info = inputs[:self.capacity]
        else:
            new_info = np.zeros(self.capacity)
            new_info[:len(inputs)] = inputs

        # Update memory with decay
        self.vector = (1 - self.decay) * self.vector + self.decay * new_info

    def get_vector(self):
        return self.vector.tolist()
