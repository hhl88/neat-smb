import numpy as np
import config
from genome import *
import random

class Species(object):
    def __init__(self, innovation):
        self.species_id = None
        self.genomes = []
        self.top_fitness = 0
        self.average_fitness = 0
        self.staleness = 0
        self.innovation = innovation
        self.genome_id = 0

        self.gene_list = []


    def get_next_genome_id(self):
        current_genome_id = self.genome_id
        self.genome_id += 1
        return current_genome_id

    def breed_child(self):
        new_genome = None
        self.genomes.sort()
        if len(self.genomes) > 1:
            if np.random.uniform() < config.CROSSOVER_CHANCE:
                random_num1 = random.randint(0, len(self.genomes) -1)
                random_num2 = 0
                while True:
                    random_num2 = random.randint(0, len(self.genomes) -1)
                    if random_num1 != random_num2:
                        break
                random_genome1 = self.genomes[random_num1]
                random_genome2 = self.genomes[random_num2]
                new_genome = self.crossover(random_genome1, random_genome2)
            else:
                new_genome = np.random.choice(self.genomes).copy_genome()
        else:
            new_genome = self.genomes[0].copy_genome()
        new_genome.genome_id = self.get_next_genome_id()
        return new_genome

    def crossover(self, genome, other_genome):
        genome1 = genome.copy_genome()
        genome2 = other_genome.copy_genome()

        if genome.fitness < other_genome.fitness:
            genome1 = other_genome.copy_genome()
            genome2 = genome.copy_genome()
        new_genome = Genome(self.innovation)
        genome1.genes.sort()
        genome2.genes.sort()

        temp = {}
        for gene in genome2.genes:
            temp[gene.innovation_number] = gene

        for gene1 in genome1.genes:
            g = gene1.copy_gene()
            if gene1.innovation_number in temp and np.random.uniform() >= 0.5 and temp[gene1.innovation_number].enabled:
                g = temp[gene1.innovation_number].copy_gene()
            new_genome.genes.append(g)
        new_genome.max_neuron = max(genome1.max_neuron, genome2.max_neuron)

        new_genome.genome_id = self.get_next_genome_id()

        for i in xrange(0, len(new_genome.mutate_rates)):
            new_genome.mutate_rates[i] = genome1.mutate_rates[i]
        new_genome.genes.sort()
        return new_genome

    def take_best_genomes(self):
        self.genomes.sort()
        # (n + d // 2) // d, where n is the dividend and d is the divisor.
        remaining = (len(self.genomes) + 2 // 2) / 2
        genomes = self.genomes[:remaining]
        self.genomes = []
        for genome in genomes:
            self.genomes.append(genome)

    def calculate_average_fitness(self):
        total = 0.0
        for genome in self.genomes:
            total += genome.global_rank
        self.average_fitness = total / len(self.genomes)

    def __cmp__(self, other):
        if self.top_fitness > other.top_fitness:
            return -1
        elif self.top_fitness < other.top_fitness:
            return 1
        else:
            return 0
