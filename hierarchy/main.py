from copy import deepcopy

import temporalPooler.htm__region as tp
from apps.settings import *
from hierarchy.CombinedGenerator import CombineGenerator
from hierarchy.util import zip_binary_matrix, unzip_binary_matrix


def main():
    # немного двигаем SimpleSteps вперед, чтобы первончальная вершина вела в однозначное место
    tss1 = TestSimpleSteps(3)
    tss1.move()
    tss2 = TestSimpleSteps(3)
    tss2.move()

    generator = CombineGenerator([tss1, tss2])
    input_size = len(generator.empty)

    r_t = tp.Region(input_size, 4)

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
        p = [[0 for _ in range(sz)] for _ in range(sz)]
        for i in Dendrite.synapses:
            x, y = cells_column[i.id_to]
            p[x][y] = 1

        nodes.append(p)

    # удаляем дубликаты
    nodes = set(map(zip_binary_matrix, nodes))
    for i in nodes:
        print(i)

    # теперь для каждого паттерна будет смотреть что предскажет тп
    # для начала будет подавать тп на вход пустоту, чтобы он не создал новых дендритов (божественный костыль)
    # новые дендриты, на самом деле, могут добавляться, но количество синапсов у них будет нулевое
    empty_input = deepcopy(generator.empty)

    for I in nodes:
        ss = set()
        current_input = I
        chain = [current_input]
        while 1:
            r_t.step_forward(empty_input)
            r_t.step_forward(unzip_binary_matrix(current_input, input_size))
            prediction = zip_binary_matrix(r_t.get_binary_prediction())
            r_t.step_forward(empty_input)
            if prediction in ss or prediction == 0:
                break
            ss.add(prediction)
            current_input = prediction
            chain.append(prediction)
        print("***" * 5)
        for i in chain:
            for j in unzip_binary_matrix(i, input_size):
                print(j)
            print()


if __name__ == "__main__":
    main()
