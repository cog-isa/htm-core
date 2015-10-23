from mind_vision_experiment.binary_image_converter import read_numbers
from mind_vision_experiment.mind_mapper import hello


def out_matrix(matrix):
    for i in matrix:
        print(i)


def main():
    numbers = read_numbers()
    three = numbers[3][0]
    # for i in three:
    #     print(i)

    cnt = 0
    for i, elem in enumerate(three):
        for j, e in enumerate(elem):
            three[i][j] = cnt
            cnt += 1

    place = [[1, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]

    # q = hello(three, place)
    # print("size: ", len(q), len(q[0]))

    for i, elem in enumerate(place):
        for j, e in enumerate(elem):
            place[i][j] = 1
            q = hello(three, place)
            print("size: ", len(q), len(q[0]))
            out_matrix(place)
            out_matrix(q)
            print()
            print()
            place[i][j] = 0


if __name__ == "__main__":
    main()
