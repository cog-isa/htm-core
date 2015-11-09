from random import randrange

from mind_vision_experiment.binary_image_converter import read_numbers
from mind_vision_experiment.slice_tester import hello
from temporalPooler.region_merge import merged_move2
from temporalPooler.htm__region import Region


def out_matrix(matrix):
    for i in matrix:
        print(i)


def make_bubble(a, scale):
    square_size = len(a)
    result = [[0 for _ in range(square_size * scale)] for _ in range(square_size * scale)]
    for i in range(square_size):
        for j in range(square_size):
            if a[i][j]:
                for x in range(i * scale, (i + 1) * scale):
                    for y in range(j * scale, (j + 1) * scale):
                        result[x][y] = 1
    return result


def zip_bubbled_data(a, scale):
    x = 0
    y = 0
    res = []
    while x < len(a):
        y = 0
        q = []
        while y < len(a):
            q.append(a[x][y])
            y += scale
        res.append(q)
        x += scale
    return res


def get_sum(a):
    res = 0
    for i in a:
        res += sum(i)
    return res


def main():
    numbers = read_numbers()
    three = numbers[3][0]

    place = [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0]]
    for i in three:
        print(i)
    print()

    BUBBLE_SIZE = 7

    q = hello(three, place)
    print("SIZE: ", len(q), len(q[0]))
    for i in q:
        print(i)
    bubbled_place = make_bubble(place, BUBBLE_SIZE)
    out_matrix(bubbled_place)
    out_matrix(zip_bubbled_data(bubbled_place, BUBBLE_SIZE))

    # важно чтобы id клеток разных регионов не пересекались!!!
    r = [Region(len(q), 4, 0),
         Region(len(bubbled_place), 1, 10000)]

    for step in range(200):
        s = 0
        x = -1
        y = -1
        for i, I in enumerate(place):
            for j, J in enumerate(I):
                if place[i][j] == 1:
                    x, y = i, j
                    break

        print("-----" * 10)
        for i in place:
            print(i)
        print("-----" * 10)
        for i, I in enumerate(place):
            for j, J in enumerate(I):
                place[i][j] = 0

        if (x == -1 and y == -1) or step < 10:
            while 1:
                x = randrange(len(place))
                y = randrange(len(place))
                place[x][y] = 1
                if get_sum(hello(three, place)):
                    break
                place[x][y] = 0
        else:
            place[x][y] = 1

        merged_move2(r, [hello(three, place), make_bubble(place, BUBBLE_SIZE)])
        print("----" * 10)
        r[0].out_prediction()
        r[1].out_prediction()
        new_place = zip_bubbled_data(r[1].out_binary_prediction(), BUBBLE_SIZE)
        place = new_place


if __name__ == "__main__":
    main()
