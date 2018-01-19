from NEAT.gene import *
from NEAT.neuron import *
from config import *


class Genome(object):
    def __init__(self, innovation):
        self.innovation = innovation
        self.genome_id = 0
        self.genes = []
        self.fitness = 0
        self.max_neuron = 0
        self.global_rank = 0
        self.network = {}
        self.mutate_rates = [WEIGHT_MUTATION_RATE_IN_GENOME,
                             ADD_CONNECTION_MUTATION_RATE,
                             BIAS_MUTATION_CHANCE,
                             ADD_NODE_MUTATION_RATE,
                             ENABLE_MUTATION_CHANCE,
                             DISABLE_MUTATION_CHANCE]

    def __eq__(self, other):
        if isinstance(other, Genome):
            return False
        return self.genome_id == other.genome_id

    def __cmp__(self, other):
        if self.fitness > other.fitness:
            return -1
        elif self.fitness < other.fitness:
            return 1
        else:
            if self.genome_id < other.genome_id:
                return -1
            elif self.genome_id > other.genome_id:
                return 1
            else:
                return 0

    def copy_genome(self):
        new_genome = Genome(self.innovation)
        new_genome.max_neuron = self.max_neuron
        new_genome.genome_id = self.genome_id
        for i in xrange(0, len(self.mutate_rates)):
            new_genome.mutate_rates[i] = self.mutate_rates[i]
        self.genes.sort()
        for gene in self.genes:
            new_genome.genes.append(gene.copy_gene())
        return new_genome

    def generate_network(self):
        for i in xrange(0, INPUT_NEURONS):
            self.network[i] = Neuron()
        for i in xrange(0, OUTPUT_NEURONS):
            self.network[i + INPUT_NEURONS] = Neuron()

        self.genes.sort()

        for gene in self.genes:
            if gene.enabled:
                if gene.output not in self.network.keys():
                    self.network[gene.output] = Neuron()
                self.network[gene.output].inputs.append(gene)
                if gene.input not in self.network.keys():
                    self.network[gene.input] = Neuron()

    def contain_connection(self, gene):
        return self.genes.__contains__(gene)

    def get_disjoint(self, other_genome):
        disjoint_genes = 0.0
        self.genes.sort()
        other_genome.genes.sort()
        for gene1 in self.genes:
            if other_genome.genes.__contains__(gene1):
                disjoint_genes += 1.0

        return disjoint_genes / max(len(self.genes), len(other_genome.genes))

    def get_excess(self, other_genome):
        if len(self.genes) == 0 and len(other_genome.genes):
            return 0
        excess_genes = 0.0
        self.genes.sort()
        other_genome.genes.sort()
        biggest_innovation_id = self.genes[len(self.genes) - 1].innovation_number
        biggest_innovation_id2 = other_genome.genes[len(other_genome.genes) - 1].innovation_number
        temp_genome = self if biggest_innovation_id > biggest_innovation_id2 else other_genome
        for gene in temp_genome.genes:
            if gene.innovation_number > biggest_innovation_id:
                excess_genes += 1.0

        n = max(len(self.genes), len(self.genes))
        return excess_genes / n

    def evaluate_network(self, inputs):
        for i in xrange(0, len(inputs)):
            self.network[i].value = inputs[i]

        # hidden node
        for neuron_id, neuron in self.network.items():
            # if neuron_id >= INPUT_NEURONS + OUTPUT_NEURONS:
                # print "in neuron hidden"
            sum_weight = 0.0
            for gene in neuron.inputs:
                neuron2 = self.network.get(gene.input)
                sum_weight += gene.weight * neuron2.value
            if len(neuron.inputs) > 0:
                neuron.value = neuron.sigmoid(sum_weight)

        # # output
        # for neuron_id, neuron in self.network.items():
        #     if INPUT_NEURONS <= neuron_id < OUTPUT_NEURONS:
        #         sum_weight = 0.0
        #         for gene in neuron.inputs:
        #             neuron2 = self.network.get(gene.input)
        #             sum_weight += gene.weight * neuron2.value
        #         if len(neuron.inputs) > 0:
        #             neuron.value = neuron.sigmoid(sum_weight)

        outputs = []
        for i in xrange(0, OUTPUT_NEURONS):
            outputs.append(self.network[INPUT_NEURONS + i].value)
        # print(outputs)
        return outputs

    def mutate(self):

        for i in xrange(0, len(self.mutate_rates)):
            self.mutate_rates[i] *= (0.95 if np.random.uniform() < 0.5 else 1.2)
        # mutate weight
        if np.random.uniform() < self.mutate_rates[0]:
            self.mutate_weight()

        # mutate connection
        # print "mutation connection"
        self.mutate_step(self.mutate_connection(False), self.mutate_rates[1])
        # print "\nmutation bias"

        self.mutate_step(self.mutate_connection(True), self.mutate_rates[2])

        # mutate node
        # print "\nmutation node"

        self.mutate_step(self.mutate_node(), self.mutate_rates[3])

        # mutate enable
        self.mutate_step(self.enable_disable_mutate(True), self.mutate_rates[4])

        # mutate disable
        self.mutate_step(self.enable_disable_mutate(False), self.mutate_rates[5])

    def mutate_weight(self):
        self.genes.sort()
        for gene in self.genes:
            gene.mutate_weight()

    def mutate_step(self, mutate_type, rate):
        n = rate * 1.0
        while n >= 0:
            if np.random.uniform() < n:
                mutate_type
            n -= 1

    def enable_disable_mutate(self, enable):
        genes_list = []
        self.genes.sort()
        for gene in self.genes:
            if gene.enabled != enable:
                genes_list.append(gene)

        if len(genes_list) == 0:
            return

        random_gene = np.random.choice(genes_list)
        random_gene.enabled = not random_gene.enabled
        pass

    def mutate_connection(self, force_bias):
        id_neuron_1 = self.random_neuron(False, True)
        id_neuron_2 = self.random_neuron(True, False)

        new_gene = Gene()
        new_gene.input = id_neuron_1
        new_gene.output = id_neuron_2
        if force_bias:
            new_gene.input = INPUT_NEURONS - 1
        if self.contain_connection(new_gene):
            return
        new_gene.weight = np.random.uniform(low=-1, high=1)
        if self.innovation.contain_links(new_gene):
            new_gene.innovation_number = self.innovation.get_innovation(new_gene)
        else:
            new_gene.innovation_number = self.innovation.get_next_innovation_number()
            self.innovation.list_gene.append(new_gene)
        # print "new gene = %s" % new_gene
        self.genes.append(new_gene)
        self.genes.sort()

        # self.network[id_neuron_2].inputs.append(new_gene)

    # adds a new random node and assigns it a random activation gate
    def mutate_node(self):
        # if there are no connections, don't add a new node
        if len(self.genes) == 0:
            return
        # choose random gene
        random_gene = np.random.choice(self.genes)

        # proceed if connection is active
        if not random_gene.enabled:
            return

        # first disable connection directly between two node
        random_gene.enabled = False
        ++self.max_neuron
        neuron_id = self.max_neuron
        new_neuron = Neuron()

        gene1 = random_gene.copy_gene()
        gene1.output = neuron_id
        gene1.weight = 1.0
        gene1.enabled = True

        gene2 = random_gene.copy_gene()
        gene2.input = neuron_id
        gene2.enabled = True

        if self.contain_connection(gene1) or self.contain_connection(gene2):
            return

        if self.innovation.contain_links(gene1):
            gene1.innovation_number = self.innovation.get_innovation(gene1)
        else:
            gene1.innovation_number = self.innovation.get_next_innovation_number()
            self.innovation.list_gene.append(gene1)
        self.genes.append(gene1)

        if self.innovation.contain_links(gene2):
            gene2.innovation_number = self.innovation.get_innovation(gene2)
        else:
            gene2.innovation_number = self.innovation.get_next_innovation_number()
            self.innovation.list_gene.append(gene2)
        self.genes.append(gene2)

        self.genes.sort()

        new_neuron.inputs.append(gene1)
        self.network[neuron_id] = new_neuron

    def same_species(self, genome):
        de = C1 * self.get_excess(genome)
        dd = C2 * self.get_disjoint(genome)
        dw = C3 * self.get_avg_weight_difference(genome)
        return dd + dw + de < COMPATIBILITY_THRESHOLD

    def random_neuron(self, not_input, not_output):
        neurons = []
        if not not_input:
            for i in xrange(0, INPUT_NEURONS):
                neurons.append(i)

        if not not_output:
            for i in xrange(0, OUTPUT_NEURONS):
                neurons.append(INPUT_NEURONS + i)

        for gene in self.genes:
            if (not not_input or gene.input >= INPUT_NEURONS) and \
                    (not not_output or gene.input >= INPUT_NEURONS + OUTPUT_NEURONS):
                neurons.append(gene.input)

            if (not not_input or gene.output >= INPUT_NEURONS) and \
                    (not not_output or gene.output >= INPUT_NEURONS + OUTPUT_NEURONS):
                neurons.append(gene.output)

        return neurons[np.random.randint(0, len(neurons))]

    def get_avg_weight_difference(self, comparison_genome):
        sum_weight = 0.0
        count = 0
        self.genes.sort()
        comparison_genome.genes.sort()
        for gene in self.genes:
            if comparison_genome.genes.__contains__(gene):
                    sum_weight += abs(gene.weight - comparison_genome.genes[comparison_genome.genes.index(gene)].weight)
                    count += 1
        return sum_weight / count if count > 0 else 0.5

    def __str__(self):
        self.genes.sort()
        return "             \n".join(map(str, self.genes))

    def __repr__(self):
        return self.__str__()
