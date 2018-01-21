import pickle

import os

from config import *
from NEAT.innovation import  *
from NEAT.species import *
from NEAT.genome import *
import math
import matplotlib.pyplot as plt


class Generation(object):
    def __init__(self):
        self.solved = False
        self.results = {}
        self.solution_genome = []
        self.species = []
        self.current_species = 0
        self.current_genome = 0
        self.population_fitness = 0
        self.generation_number = 1
        self.species_id = 0
        self.current_max_fitness = 0
        self.list_fitness = []
        self.max_fitness = 0
        self.innovation = Innovation()

    def initialize_generation(self):
        for i in xrange(0, POPULATION):
            genome = Genome(self.innovation)
            genome.max_neuron = INPUT_NEURONS
            genome.mutate()
            self.speciate(genome)

    def create_new_generation(self):
        self.take_best_genomes_in_species(False)
        self.rank_globally()
        self.remove_stale_species()
        self.rank_globally()
        for species in self.species:
            species.calculate_average_fitness()
        self.take_half_best_species()

        sum_fitness = self.calculate_total_average_fitness()
        childs = []
        if len(self.solution_genome) > 10:
            self.take_best_genomes_in_solution_genome()
        for species in self.species:
            breed = int(math.floor(species.average_fitness * POPULATION / sum_fitness))
            for i in xrange(0, breed):
                # if not self.solved or np.random.uniform() > 0.6:
                childs.append(species.breed_child())
                # else:
                #     childs.append(species.breed_child(np.random.choice(self.solution_genome)))

        self.take_best_genomes_in_species(True)

        while len(childs) + len(self.species) < POPULATION:
            random_sp = np.random.choice(self.species)
            childs.append(random_sp.breed_child())
        for genome in childs:
            genome.mutate()
            self.speciate(genome)
        average_fitness = sum(self.list_fitness, 0.0) / float(len(self.list_fitness))
        self.results[self.generation_number] = [self.current_max_fitness, average_fitness]
        self.list_fitness = []
        self.current_max_fitness = 0
        self.save_results()
        self.draw_graph()
        self.get_next_generation_number()

    def take_best_genomes_in_solution_genome(self):
        self.solution_genome.sort(cmp=lambda x, y: -1 if x.fitness > y.fitness else
                                                    1 if x.fitness < y.fitness else
                                                    -1 if len(x.genes) > len(y.genes) else
                                                    1 if len(x.genes) > len(y.genes) else 0)
        self.solution_genome = self.solution_genome[: 10]

    def save_results(self):
        save_path = os.getcwd() + "/records/graphs/"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        with open(save_path + 'results.json', 'w') as outfile:
            outfile.write(str(self.results))

        # with open('results.json', 'r') as f:
        #     s = f.read()
        #     loaded_results = ast.literal_eval(s)

    def draw_graph(self):
        save_path = os.getcwd() + "/records/graphs/"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        ax = plt.subplot(111)
        max_fitness = []
        average_fitness = []
        for x in self.results.values():
            max_fitness.append(x[0])
            average_fitness.append(x[1])
        ax.plot(self.results.keys(), max_fitness)
        ax.plot(self.results.keys(), average_fitness)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        ax.legend(['max fitness', 'average fitness'], loc='center left', bbox_to_anchor=(1, 0.5))
        max_length = len(self.results)
        max_interval = 10 ** max(0, (len(str(max_length)) - 2))

        # min_interval = max_length / 2
        max_length = int(math.ceil(max_length / float(max_interval) + 1) * max_interval)
        ax.legend(['max fitness', 'average fitness'], loc='center left', bbox_to_anchor=(1, 0.5))
        major_ticks = np.arange(0, max_length, max_interval)
        # minor_ticks = np.arange(0, max_length, min_interval)
        ax.set_xticks(major_ticks)
        # ax.set_xticks(minor_ticks, minor=True)
        ax.set_xlim(xmin=1)
        plt.title('NEAT Generation')
        plt.ylabel('Fitness')
        plt.xlabel('Generation')
        plt.savefig(save_path + 'records.png', bbox_inches='tight')

    def contain_connection(self, gene):
        return self.gene_list.__contains__(gene)

    def initialize_game(self):
        species = self.species[self.current_species]
        genome = species.genomes[self.current_genome]
        genome.generate_network()
        print ""
        print "\ngeneration[%d]---species[%d]-------genome [%d]------len genome = %d " % (
            self.generation_number, self.current_species + 1,
            self.current_genome + 1, len(species.genomes))

    def increase_genome(self):
        species = self.species[self.current_species]

        if self.current_genome + 1 >= len(species.genomes):
            self.current_species += 1
            self.current_genome = 0

            if self.current_species >= len(self.species):
                self.create_new_generation()
                self.current_species = 0
                self.species_id = 0

        else:
            self.current_genome += 1

    def speciate(self, genome):
        for species in self.species:
            if len(species.genomes) > 0:
                if genome.same_species(species.genomes[0]):
                    species.genomes.append(genome)
                    species.genomes[len(species.genomes) - 1].genome_id = species.get_next_genome_id()
                    return

        new_species = Species(self.innovation)
        new_species.genomes.append(genome)
        new_species.genomes[0].genome_id = new_species.get_next_genome_id()
        new_species.species_id = self.get_next_species_id()
        self.species.append(new_species)

    def get_next_species_id(self):
        current_species_id = self.species_id
        self.species_id += 1
        return current_species_id

    def get_next_generation_number(self):
        current_generation_number = self.generation_number
        self.generation_number += 1
        return current_generation_number

    def rank_globally(self):
        genomes = []
        for species in self.species:
            for genome in species.genomes:
                genomes.append(genome)
        genomes.sort()
        for i in xrange(0, len(genomes)):
            genomes[i].global_rank = i + 1

    def remove_stale_species(self):
        survive = []

        for species in self.species:
            species.genomes.sort()
            if len(species.genomes) > 1:
                if species.genomes[1].fitness >= species.top_fitness:
                    species.top_fitness = species.genomes[1].fitness
                    species.staleness = 0
                else:
                    species.staleness += 1

            if species.staleness < STAGNATED_SPECIES_THRESHOLD or species.top_fitness >= self.max_fitness:
                survive.append(species)

        self.species = survive

    def take_half_best_species(self):
        self.species.sort()
        species = self.species[: len(self.species) / 2 + 1]
        self.species = []
        for sp in species:
            self.species.append(sp)

    def take_best_genomes_in_species(self, take_only_the_best):
        for species in self.species:
            if take_only_the_best:
                species.genomes.sort()
                species.genomes = [species.genomes[0]]
            else:
                species.take_best_genomes()

    def calculate_total_average_fitness(self):
        average = 0
        for species in self.species:
            average += species.average_fitness
        return average
