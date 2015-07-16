from htm__region import Region
from settings import *
# generator = GENERATOR(REGION_SIZE_N)


def read_reg(f, n):
    res = []
    for i in range(n):
        p = []
        q = f.readline().split(" ")
        for j in q:
            try:
                p.append(int(j))
            except:
                pass
        res.append(p)
    f.readline()
    return res


def equal(x, y):
    if not x:
        return False
    for i in range(len(x)):
        for j in range(len(x[0])):
            if x[i][j] != y[i][j]:
                return False
    return True
f = open("out.txt", "r")

n, m, steps = f.readline().split(" ")
n = int(n)

steps = int(steps)


r = Region(n, COLUMN_SIZE)
b = []
a = []
for I in range(steps):
    print('---------------------')
    # generator.out()
    b = a
    a = read_reg(f, n)
    # if equal(b, a):
    #      continue
    for i in a:
        print(i)
    r.step_forward(a)
    r.out_prediction()
    # generator.move()


f.close()