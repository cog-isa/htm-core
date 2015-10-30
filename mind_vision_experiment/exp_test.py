from random import randrange

from mind_vision_experiment.binary_image_converter import read_numbers
from mind_vision_experiment.slice_tester import hello
from temporalPooler.region_merge import merged_move2
from temporalPooler.htm__region import Region


def out_matrix(matrix):
    for i in matrix:
        print(i)


def main():
    numbers = read_numbers()
    three = numbers[3][0]

    place = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]

    for i in three:
        print(i)
    print()

    q = hello(three, place)
    print("SIZE: ", len(q), len(q[0]))
    for i in q:
        print(i)

    # важно чтобы id клеток разных регионов не пересекались!!!
    r = [Region(len(q), 4, 0),
         Region(len(place), 4, 10000)]

    for step in range(700):
        s = 0
        for p in place:
            s += sum(p)
        if s == 0 or step < 10:
            for i, I in enumerate(place):
                for j, J in enumerate(I):
                    place[i][j] = 0
            place[randrange(len(place))][randrange(len(place))] = 1

        merged_move2(r, [hello(three, place), place])
        print("----" * 10)
        r[0].out_prediction()
        r[1].out_prediction()
        new_place = r[1].out_binary_prediction()
        place = new_place


if __name__ == "__main__":
    main()
