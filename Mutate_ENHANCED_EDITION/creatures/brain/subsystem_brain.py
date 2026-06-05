# creatures/brain/subsystem_brain.py

class SubsystemBrain:
    def __init__(self, shape):
        from .nn_core import NeuralNetwork
        self.nn = NeuralNetwork(shape)

    def compute_action(self, inputs):
        return self.nn.forward(inputs)
