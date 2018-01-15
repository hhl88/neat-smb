#! /usr/bin/env python


from NEAT import neural_network as NeuralNetwork
import numpy as np
from NEAT import config
from gamelib.menu import Menu as Mario


INPUTS = 10
OUTPUTS = 1


class Environment(object):
    def __init__(self):
        # Create parent generation
        self.generations = []
        initial_topology = [INPUTS, OUTPUTS]
        self.generations.append([NeuralNetwork(initial_topology) for _ in range(config.POPULATION)])

    def start(self):

        # Create
        for generation_index in range(config.GENERATIONS):
            current_generation = self.generations[generation_index]

            """ FITNESS """
            self.fitness(current_generation)

            """ SELECTION """
            self.selection(current_generation)

            """ REPLICATION """
            self.replication(current_generation)

    def fitness(self, current_generation):

        # Play game and get results
        mario = Mario(current_generation)
        mario.play()
        results = flappy_Bio.crash_info
        # Calculate fitness
        self.fitness_values = []
        self.network_index_dict = {}
        for index, result in enumerate(results):
            network = result['network']
            self.network_index_dict[index] = network

            distance = result['distance']
            energy = result['energy']

            fitness = distance - energy* 0.5
            fitness = -1 if fitness == 0 else fitness

            self.fitness_values.append((index, fitness))

    def selection(self, current_generation):
        dtype = [('network_index', int), ('fitness', int)]
        self.fitnesses = np.array(self.fitness_values, dtype=dtype)

        sorted_fitness_indices = np.sort(self.fitnesses, order='fitness')[::-1]

        self.top_networks = []
        for top_fitness_indices in sorted_fitness_indices[:int(len(sorted_fitness_indices) / 2)]:
            self.top_networks.append(self.network_index_dict[top_fitness_indices[0]])

    def replication(self, current_generation):
        new_generation = []
        for top_network in self.top_networks:
            progeny = []
            for _ in range(2):
                topology, genes = top_network.copy_genes()
                new_network = NeuralNetwork(topology, genes)
                progeny.append(new_network)

            new_generation += progeny

        self.generations.append(new_generation)


if __name__ == "__main__":
    world = Environment()
    world.start()
