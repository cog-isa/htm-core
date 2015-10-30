def compute_restrictions(input_size, mapper_size):
    for h in range(int(input_size / mapper_size), input_size + 1):
        for x in range(1, h + 1):
            if (input_size - h + x) % x == 0:
                k = int((input_size - h + x) / x)
                if k == mapper_size:
                    return h, x, k
    return False


def hello(generator_data, to_map_data):
    size, offset, _ = compute_restrictions(len(generator_data), len(to_map_data))
    for i, I in enumerate(to_map_data):
        for j, J in enumerate(I):
            if to_map_data[i][j]:
                res = []
                for x in range(i * offset, i * offset + size):
                    q = []
                    for y in range(j * offset, j * offset + size):
                        q.append(generator_data[x][y])
                    res.append(q)
                return res
    raise (AttributeError, "no active bit exception")


def main():
    # test
    for i in range(1, 500):
        for j in range(1, i + 1):
            print(i, j)
            if compute_restrictions(i, j):
                print(compute_restrictions(i, j))
            else:
                raise (ArithmeticError, "~~~~ can't find slices params ~~~~~")


if __name__ == "__main__":
    main()
