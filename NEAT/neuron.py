import numpy as np


class Neuron(object):
    def __init__(self):
        self.value = 0.0
        self.inputs = []

    def sigmoid(self, x):
        return 2.0 / (1 + np.exp(-4.9 * float(x))) - 1.0

    def __str__(self):
        return "value = %s   inputs = [%s]" % (self.value, [str(item) for item in self.inputs])

    def __repr__(self):
        return self.__str__()
