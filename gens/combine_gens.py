from gens.input_generators import TestSimpleSteps, Cross

__author__ = 'AVPetrov'

class StepsAndCross:
    def __init__(self, square_size):
        self.simplesteps = TestSimpleSteps(square_size)
        self.cross = Cross(square_size)
        self.inner_generator = self.simplesteps
        self.steps = 0
        self.square_size = square_size

    def move(self):
        if self.steps < self.square_size * 2:
            self.inner_generator = self.simplesteps
        else:
            self.inner_generator = self.cross
        if self.steps > self.square_size * 4:
            self.steps = 0
        self.steps += 1

        self.inner_generator.move()

    def out(self):
        a = self.get_data()
        for i in a:
            print(i)
        print()

    def get_data(self):
        return self.inner_generator.get_data()
