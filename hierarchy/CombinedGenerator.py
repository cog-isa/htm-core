from copy import deepcopy

from hierarchy.util import get_period, zip_binary_matrix

from apps.settings import *
from mind_vision_experiment.merge_inputs import merge_input


class CombineGenerator:
    def __init__(self, gens: []):
        self.gens = gens
        self.cur_gen_ind = 0
        self.cur_gen_cnt = 0

        # вычисляем первоначальную матрицу данных
        data = []
        for i in self.gens:
            data.append(i.get_data())

        self.a = merge_input(data)
        for i, I in enumerate(self.a):
            for j, J in enumerate(I):
                self.a[i][j] = 0

        # сохрнаяем пустую матрицу, будем выводить ее в качестве разделителя
        self.empty = deepcopy(self.a)

        # считаем период каждого генератора
        self.gens_periods = []

        # количество шагов генератора для которого будет предвычисляться период
        period_calc_size = 100

        for gen in self.gens:
            a = []
            t = deepcopy(gen)
            for i in range(period_calc_size):
                a.append(zip_binary_matrix(gen.get_data()))
                gen.move()
            self.gens_periods.append(get_period(a))
            gen = t
        print(self.gens_periods)

    def move(self):
        # обнуляем a - матрицу результата
        self.a = deepcopy(self.empty)

        if self.cur_gen_cnt == self.gens_periods[self.cur_gen_ind]:
            # начинаем использовать следующий генератор
            self.cur_gen_ind = (self.cur_gen_ind + 1) % len(self.gens)
            self.cur_gen_cnt = 0
        else:
            self.gens[self.cur_gen_ind].move()
            self.cur_gen_cnt += 1

            # считаем индекс с которого будем заполнять значение в матрице
            start_matrix_index = 0
            for i, gen in enumerate(self.gens):
                if i == self.cur_gen_ind:
                    break
                start_matrix_index += len(gen.get_data())
            cur_gen_data = self.gens[self.cur_gen_ind].get_data()

            for i, I in enumerate(cur_gen_data):
                for j, J in enumerate(I):
                    self.a[i + start_matrix_index][j + start_matrix_index] = cur_gen_data[i][j]

    def get_data(self):
        return deepcopy(self.a)

    def out(self):
        for i in self.get_data():
            print(i)
        print()


def test():
    tss1 = TestSimpleSteps(3)
    tss1.move()
    tss2 = TestSimpleSteps(3)
    tss2.move()
    cg = CombineGenerator([tss1, tss2])
    for i in range(20):
        cg.out()
        cg.move()


if __name__ == "__main__":
    test()
