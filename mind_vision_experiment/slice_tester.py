def compute_restrictions(input_size, mapper_size):
    for h in range(int(input_size / mapper_size), input_size + 1):
        for x in range(1, h + 1):
            if (input_size - h + x) % x == 0:
                k = (input_size - h + x) / x
                if k == mapper_size:
                    return h, x, k
    return False


for i in range(1, 10):
    for j in range(1, i + 1):
        print(i, j)
        if compute_restrictions(i, j):
            print(compute_restrictions(i, j))
        else:
            print("!!!! can't find slice !!!!")
            break
