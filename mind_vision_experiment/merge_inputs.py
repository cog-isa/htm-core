def merge_input(a):
    size = 0
    for i in a:
        size += len(i)
    res = [[0 for _ in range(size)] for __ in range(size)]
    t = 0

    for i, I in enumerate(a):
        assert(len(I) == len(I[0]))
        for x in range(len(I)):
            for y in range(len(I[0])):
                res[t + x][t + y] = I[x][y]
        t += len(I)

    for i in res:
        print(i)


def test():
    i1 = [[0, 0, 1],
          [1, 0, 1],
          [1, 0, 1],
          ]
    i2 = [[1, 0, 1, 0],
          [1, 0, 1, 0],
          [1, 1, 1, 0],
          [1, 0, 1, 0],
          ]
    i3 = [[1, 0, 1, 0, 1],
          [1, 0, 1, 0, 1],
          [1, 1, 1, 0, 1],
          [1, 0, 1, 0, 1],
          [1, 0, 1, 0, 1],
          ]
    merge_input([i1, i2, i3])


if __name__ == "__main__":
    test()
