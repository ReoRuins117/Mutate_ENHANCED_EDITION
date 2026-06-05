# creatures/brain/nn_core.py

import numpy as np
import random

class NeuralNetwork:
    def __init__(self, shape, initial_weights=None):
        """
        shape = (input_size, hidden1, hidden2, ..., output_size)
        """
        self.shape = shape
        self.layers = len(shape) - 1

        # Initialize weights
        self.weights = []
        self.biases = []

        for i in range(self.layers):
            inp = shape[i]
            out = shape[i + 1]

            if initial_weights and (i in initial_weights):
                W, b = initial_weights[i]
            else:
                # Xavier initialization
                limit = np.sqrt(6 / (inp + out))
                W = np.random.uniform(-limit, limit, (out, inp))
                b = np.zeros(out)

            self.weights.append(W)
            self.biases.append(b)

    def forward(self, x):
        """
        x: input vector (list or np array)
        returns: output vector
        """
        a = np.array(x, dtype=float)

        for i in range(self.layers):
            W = self.weights[i]
            b = self.biases[i]

            z = W @ a + b

            # Hidden layers use tanh
            if i < self.layers - 1:
                a = np.tanh(z)

            # Output layer uses linear activation
            else:
                a = z

        return a

    def mutate(self, rate=0.05, strength=0.1):
        """
        Mutates weights and biases slightly.
        rate = chance each weight mutates
        strength = how much it mutates
        """
        for i in range(self.layers):
            W = self.weights[i]
            b = self.biases[i]

            # Mutate weights
            mask = np.random.rand(*W.shape) < rate
            W += mask * np.random.normal(0, strength, W.shape)

            # Mutate biases
            mask_b = np.random.rand(*b.shape) < rate
            b += mask_b * np.random.normal(0, strength, b.shape)

        # No return — modifies in place
