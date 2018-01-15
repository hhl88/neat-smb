# Configurations for NEAT
import numpy as np


INPUT_NEURONS = 320
OUTPUT_NEURONS = 4
POPULATION = 100
MAX_NODES = 254

C1 = 1.00
C2 = 2.0
C3 = 0.5
COMPATIBILITY_THRESHOLD = 1.0

WEIGHT_MUTATION_RATE_IN_GENOME = 0.8
UNIFORM_PERTURBED_WEIGHT_MUTATION_IN_GENE = 0.9


ADD_NODE_MUTATION_RATE = 0.5
ADD_CONNECTION_MUTATION_RATE = 2.0
BIAS_MUTATION_CHANCE = 0.4
DISABLE_MUTATION_CHANCE = 0.4
ENABLE_MUTATION_CHANCE = 0.2

INHERIT_DISABLED_GENE_RATE = 0.75
CROSSOVER_CHANCE = 0.75

INTERSPECIES_MATING_RATE = 0.001

STAGNATED_SPECIES_THRESHOLD = 15


MAX_GENOMES_WITH_TOP_FITNESS = 20

