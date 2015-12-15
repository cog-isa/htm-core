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
        for j, J in enumerate(a):
            if a[i][j]:
                res += x
            x *= 2
    return res


def unzip_binary_matrix(a, size):
    res = [[0 for _ in range(size)] for _ in range(size)]
    x = 1
    for i, I in enumerate(res):
        for j, J in enumerate(res):
            res[i][j] = int((a & x) > 0)
            x *= 2
    return res