def get_period(a, k=None):
    if k:
        ok = True
        for i in range(k):
            j = i + k
            while j < len(a):
                if a[j] != a[j - k]:
                    ok = False
                    break
                j += k
        if ok:
            return k
    else:
        for i in range(1, len(a) + 1):
            if get_period(a, i):
                return i


def zip_binary_matrix(a: []):
    res = 0
    x = 1
    for i, I in enumerate(a):
        for j, J in enumerate(I):
            if a[i][j]:
                res += x
            x *= 2
    return res


def unzip_binary_matrix(a, size):
    res = [[0 for _ in range(size)] for _ in range(size)]
    x = 1
    for i, I in enumerate(res):
        for j, J in enumerate(I):
            res[i][j] = int((a & x) > 0)
            x *= 2
    return res


def zip_binary_3(a):
    res = 0
    x = 1
    for i, I in enumerate(a):
        for j, J in enumerate(I):
            for k, K in enumerate(J):
                if a[i][j][k]:
                    res += x
            x *= 2
    return res


def unzip_binary_3(a, size, column_size):
    res = [[[0 for _ in range(column_size)] for _ in range(size)] for _ in range(size)]
    x = 1
    for i, I in enumerate(res):
        for j, J in enumerate(I):
            for k, K in enumerate(J):
                res[i][j][k] = int((a & x) > 0)
                x *= 2
    return res


def unzip_binary_3_to_matrix(a, size, column_size):
    t = unzip_binary_3(a, size, column_size)
    res = [[0 for _ in range(size)] for _ in range(size)]
    for i, I in enumerate(res):
        for j, J in enumerate(I):
            res[i][j] = int(sum(t[i][j]) > 0)
    return res