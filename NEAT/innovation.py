

class Innovation(object):

    def __init__(self):
        self.current_innovation_number = 1
        self.list_gene = []

    def get_next_innovation_number(self):
        innovation_number = self.current_innovation_number
        self.current_innovation_number += 1
        return innovation_number

    def contain_links(self, gene):
        return self.list_gene.__contains__(gene)

    def get_innovation(self, gene):
        self.list_gene.sort()
        return self.list_gene[self.list_gene.index(gene)].innovation_number
