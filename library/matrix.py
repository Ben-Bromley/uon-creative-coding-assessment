import numpy as np


class Matrix:

    #
    def __init__(self):
        self.matrix = []

    #
    def generate(self):
        for i in range(0xFFFFFF, 0x000000, -5):
            if (i % 6400000 == 0):
                print(".", end="")
            self.matrix.append([i & 255, ((i >> 8) & 255), ((i >> 16) & 255)])

        return np.array(self.matrix)


#
if __name__ == "__main__":
    matrix = Matrix()
    print('Generating Matrix...')
    print(matrix.generate())
