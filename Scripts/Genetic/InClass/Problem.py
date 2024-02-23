from Utils import sphere


class Problem:
    number_of_genes: int
    max_val: int
    min_val: int

    def __init__(self):
        self.number_of_genes = 8
        self.max_val = 10
        self.min_val = -10
        self.cost = sphere
