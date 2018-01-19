from config import *
import numpy as np


class Gene(object):
    def __init__(self):
        self.innovation_number = 0
        self.input = 0
        self.output = 0
        self.weight = 0.0
        self.enabled = True

    def copy_gene(self):
        new_gene = Gene()
        new_gene.input = self.input
        new_gene.output = self.output
        new_gene.weight = self.weight
        new_gene.enabled = self.enabled
        new_gene.innovation_number = self.innovation_number
        return new_gene

    def mutate_weight(self):
        # uniform_chance = np.random.uniform()
        if np.random.uniform() < UNIFORM_PERTURBED_WEIGHT_MUTATION_IN_GENE:
            self.weight += 2.0 * np.random.uniform() * CONNECT_STEP - CONNECT_STEP
        else:
            self.weight = np.random.uniform(-1, 1)

    def __eq__(self, other):
        if not isinstance(other, Gene):
            return False
        return self.input == other.input and self.output == other.output

    def __str__(self):
        return '      innovation = %d, input= %s, output = %s, weight= %s, enabled = %s' % (
                    self.innovation_number, self.input, self.output, self.weight, self.enabled)

    def __cmp__(self, other):
        if self.innovation_number > other.innovation_number:
            return 1
        elif self.innovation_number == other.innovation_number:
            return 0
        else:
            return -1

    def __repr__(self):
        return self.__str__()

