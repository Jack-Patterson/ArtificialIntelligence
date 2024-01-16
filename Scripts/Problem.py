class Problem:
    number_of_genes: int
    max_val: int
    min_val: int

    def __init__(self):
        self.number_of_genes = 8
        self.max_val = 10
        self.min_val = -10

    @staticmethod
    def cost(x):
        total = 0
        for i in x:
            total += i ** 2

        return total
