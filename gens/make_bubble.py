__author__ = 'tv'


class MakeBubble:
    def __init__(self, inner_generator, square_size, scale):
        self.inner_generator = inner_generator(square_size)
        self.scale = scale
        self.square_size = square_size

    def move(self):
        self.inner_generator.move()

    def out(self):
        a = self.get_data()
        for i in a:
            print(i)
        print()

    def get_data(self):
        result = [[0 for _ in range(self.square_size * self.scale)] for _ in range(self.square_size * self.scale)]
        a = self.inner_generator.get_data()
        for i in range(self.square_size):
            for j in range(self.square_size):
                if a[i][j]:
                    for x in range(i * self.scale, (i + 1) * self.scale):
                        for y in range(j * self.scale, (j + 1) * self.scale):
                            result[x][y] = 1
        return result