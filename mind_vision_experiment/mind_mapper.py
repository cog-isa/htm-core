from gens.input_generators import Cross, MakeBubble


def point_in(x, y, x1, y1, x2, y2):
    eps = 0
    return x1 - eps < x < x2 + eps and y1 - eps < y < y2 + eps


def hello(generator_data, to_map_data):
    h = len(generator_data) * 1.0 / len(to_map_data)
    # print(h)

    x, y = -1, -1
    for i, elem in enumerate(to_map_data):
        for j, _ in enumerate(elem):
            if to_map_data[i][j]:
                x, y = i, j
    assert (x != -1 and y != -1)
    # print(x, y)
    res = []

    for i, elem in enumerate(generator_data):
        q = []
        for j, _ in enumerate(elem):
            ok = False
            for tx in range(2):
                for ty in range(2):
                    if ok:
                        break
                    if point_in(i + tx, j + ty, x * h, y * h, x * h + h, y * h + h):
                        q.append(generator_data[i][j])
                        ok = True
        if q:
            res.append(q)

    return res


def main():
    # потестим
    generator = MakeBubble(Cross, 5, 1)
    generator.out()
    q = hello(generator.get_data(),
              [[0, 1],
               [0, 0]])
    for i in q:
        print(i)

if __name__ == "__main__":
    main()
