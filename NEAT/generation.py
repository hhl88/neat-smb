from config import *
import innovation as Innovation
from NEAT.species import *
from NEAT.genome import *
import math


class Generation(object):
    def __init__(self):
        self.solution_genome = None
        self.species = []
        self.current_species = 0
        self.current_genome = 0
        self.population_fitness = 0
        self.generation_number = 1
        self.species_id = 0
        self.max_fitness = 0
        self.innovation = Innovation.Innovation()

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
        for species in self.species:
            breed = int(math.floor(species.average_fitness * POPULATION / sum_fitness))
            for i in xrange(0, breed):
                childs.append(species.breed_child())

        self.take_best_genomes_in_species(True)

        while len(childs) + len(self.species) < POPULATION:
            random_sp = np.random.choice(self.species)
            childs.append(random_sp.breed_child())
        for genome in childs:
            genome.mutate()
            self.speciate(genome)
        self.get_next_generation_number()

    def contain_connection(self, gene):
        return self.gene_list.__contains__(gene)

    def initialize_game(self):
        species = self.species[self.current_species]
        genome = species.genomes[self.current_genome]
        genome.generate_network()

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
            if len(species.genomes) >1:
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
