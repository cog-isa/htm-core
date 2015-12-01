from copy import deepcopy

import spatialPooler.sp_region as sp
import temporalPooler.htm__region as tp
from apps.settings import *


def zip_binary_matrix(a):
    res = 0
    x = 1
    for i, I in enumerate(a):
        for j, J in enumerate(a):
            if a[i][j]:
                res += x
            x *= 2
    return res


def unzip_binary_matrix(q, size):
    res = [[0 for _ in range(size)] for _ in range(size)]
    x = 1
    for i, I in enumerate(res):
        for j, J in enumerate(res):
            res[i][j] = int((q & x) > 0)
            x *= 2
    return res


def main():
    generator = MakeBubble(input_settings.GENERATOR, temporal_settings.REGION_SIZE_N, input_settings.SCALE)

    spatial_settings.yinput = spatial_settings.xinput * input_settings.SCALE
    spatial_settings.xinput = spatial_settings.xinput * input_settings.SCALE
    spatial_settings.ydimension = spatial_settings.xdimension

    r_s = sp.Region(spatial_settings, input_settings.MAPPER)
    r_t = tp.Region(spatial_settings.xdimension, temporal_settings.COLUMN_SIZE)

    for i in range(input_settings.STEPS_NUMBER):
        data = generator.get_data()
        generator.out()
        inp_t = r_s.step_forward(data)
        for j in inp_t:
            print(j)
        r_t.step_forward(inp_t)
        r_t.out_prediction()
        generator.move()

    # движуха

    start_patterns = []
    cells_column = {}
    for i, I in enumerate(r_t.columns):
        for j, J in enumerate(I):
            for cell, Cell in enumerate(r_t.columns[i][j].cells):
                # сохраняем принадлежность клетки какой-то колонке
                cells_column[Cell.id] = [i, j]
                for dendrite, Dendrite in enumerate(Cell.dendrites):
                    start_patterns.append(Dendrite)

    nodes = []

    for Dendrite in start_patterns:
        sz = len(generator.get_data())
        p = [[0 for _ in range(sz)] for _ in range(sz)]
        for i in Dendrite.synapses:
            x, y = cells_column[i.id_to]
            p[x][y] = 1

        nodes.append(p)

    def matrix_equals(x, y):
        # проверяем размеры
        if len(x) != len(y):
            return False
        if len(x[0]) != len(y[0]):
            return False
        # если размеры совпали - провреяем совпадение элементов
        for i in range(len(x)):
            for j in range(len(x[0])):
                if x[i][j] != y[i][j]:
                    return False
        return True

    def find_duplicate_matrix(a, q):
        for i in a:
            if matrix_equals(i, q):
                return True
        return False

    def kill_duplicates(a):
        res = []
        for i in a:
            if not find_duplicate_matrix(res, i):
                res.append(i)
        return res

    print("-----" * 5)
    nodes = kill_duplicates(nodes)
    for i in nodes:
        for j in i:
            print(j)
        print()

    for i, I in enumerate(nodes):
        print(i, "***" * 3)
        q = deepcopy(I)
        mem = []
        while not find_duplicate_matrix(mem, q):
            mem.append(q)
            r_t.step_forward(q)
            q = r_t.get_binary_prediction()

        for i in mem:
            for j in i:
                print(j)
            print()
        print("---" * 3)


    # тест сжатия в число
    a = [[1, 1, 1],
     [1, 1, 1],
     [0, 1, 1]]
    p = zip_binary_matrix(a)
    t = unzip_binary_matrix(p, len(a))
    for i in t:
        print(i)

if __name__ == "__main__":
    main()
