# creatures/brain/master_brain.py

class MasterBrain:
    def __init__(self, params):
        from .nn_core import NeuralNetwork
        self.nn = NeuralNetwork(params.master_shape)

    def choose_subsystem(self, inputs):
        out = self.nn.forward(inputs)
        return int(out.argmax())


