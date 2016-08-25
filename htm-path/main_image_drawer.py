import imageio
import numpy as np


def draw_image(filename, a):
    size = 30
    p = np.empty((len(a) * size, len(a) * size, 3))
    for ii in range(len(a)):
        for jj in range(len(a)):
            i = ii * size
            j = jj * size
            for I in range(size):
                for J in range(size):
                    p[I + i][J + j] = np.array([255, 255, 255])
                    if a[ii][jj] == 1:
                        p[i + I][j + J] = np.array([0, 255, 0])
                    if a[ii][jj] == 2:
                        p[i + I][j + J] = np.array([255, 0, 0])
                    if ii == 3 and jj == 5:
                        p[i + I][j + J] = np.array([0, 0, 255])

    imageio.imwrite(filename + ".jpg", p)


def main():
    aa = [[1, 1, 0], [0, 0, 0], [1, 0, 0]]
    draw_image("hello", aa)


if __name__ == "__main__":
    main()