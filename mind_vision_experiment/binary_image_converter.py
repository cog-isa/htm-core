def read_number(data):
    q = []
    x = []
    for i, e in enumerate(data):
        if i % 28 == 0 and i > 0:
            q.append(x)
            x = []
        x.append(1 if int(e) > 70 else 0)
    return q


def read_numbers():
    # читает числа из csv файла, бинаризует их и раскладывает в словарь

    data = {}
    with open("train.csv", "r") as f:
        f.readline()
        mx_size = 100
        for i in range(mx_size):
            s = f.readline().split(",")
            v = int(s[0])
            d = s[1:]
            q = read_number(d)
            if not q:
                print("close input, have images", i)
                break
            if v in data:
                data[v].append(q)
            else:
                data[v] = [q]
    return data


def main():
    # тест
    q = read_numbers()
    for i in q[3][0]:
        print(i)


if __name__ == "__main__":
    main()
