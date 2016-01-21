from copy import deepcopy

import temporalPooler.htm__region as tp
from apps.settings import *
from hierarchy.CombinedGenerator import CombineGenerator
from hierarchy.util import zip_binary_matrix, unzip_binary_matrix, zip_binary_3, unzip_binary_3_to_matrix, \
    unzip_binary_3


class ListOfSynapse:
    def __init__(self, a):
        self.a = set(a)

    def __eq__(self, other):
        return not (self.a - other.a)

    def __hash__(self):
        x = 0
        for i in self.a:
            x += 2 ** i
        return x

    def to_column_active_matrix(self, size, cells_columns: {}):
        res = [[0 for _ in range(size)] for _ in range(size)]
        for i in self.a:
            x, y = cells_columns[i]
            res[x][y] = 1
        return res

def main():
    # немного двигаем SimpleSteps вперед, чтобы первончальная вершина вела в однозначное место
    tss1 = TestSimpleSteps(3)
    tss1.move()
    tss2 = TestSimpleSteps(3)
    tss2.move()

    generator = CombineGenerator([tss1, tss2])
    input_size = len(generator.empty)
    CELLS_IN_COLUMN = 4
    r_t = tp.Region(input_size, CELLS_IN_COLUMN)

    for i in range(input_settings.STEPS_NUMBER):
        data = generator.get_data()
        generator.out()
        r_t.step_forward(data)
        r_t.out_prediction()
        generator.move()

    # на этом шаге мы уже имеем обученный регион тп

    # выделяем из дендритов все возможные паттерны
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
        p = []
        for i in Dendrite.synapses:
            x, y = cells_column[i.id_to]
            p.append(i.id_to)

        nodes.append(ListOfSynapse(p))

    """
    for D in nodes:
        res = [[0 for _ in range(sz)] for _ in range(sz)]
        for i, I in enumerate(res):
            for j, J in enumerate(I):
                res[i][j] = int(sum(D[i][j]) > 0)
        for i in res:
            print(i)
        print()
    exit(0)
    """
    # удаляем дубликаты
    sz = len(generator.get_data())
    nodes = set(nodes)
    # теперь для каждого паттерна будем смотреть что предскажет тп
    # для начала будет подавать тп на вход пустоту, чтобы он не создал новых дендритов (божественный костыль)
    # новые дендриты, на самом деле, могут добавляться, но количество синапсов у них будет нулевое
    empty_input = deepcopy(generator.empty)
    for I in nodes:
        ss = set()
        current_input = I
        chain = [current_input]

        while 1:
            r_t.step_forward(empty_input)
            r_t.step_forward(current_input.to_column_active_matrix(sz, cells_column))
            prediction = ListOfSynapse(r_t.get_predicted_cells_ids())
            r_t.step_forward(empty_input)
            if prediction in ss:
                break
            ss.add(prediction)
            current_input = prediction
            chain.append(prediction)
            t = list(map(lambda x: x.__hash__(), chain))
            print(t)
            print()
        print("***" * 5)
        for i in chain:
            for j in i.to_column_active_matrix(sz, cells_column):
                print(j)
            print()


if __name__ == "__main__":
    main()
