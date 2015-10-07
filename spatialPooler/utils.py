# -*- coding: utf8 -*-
from math import sqrt

__author__ = 'AVPetrov'


def get_distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def kth_score(overlaps, k):
    if len(overlaps) >= k:
        return sorted(overlaps)[len(overlaps) - k]
    else:
        return sorted(overlaps)[len(overlaps) - 1]


def to_vector(m):
    output = []
    for i in m:
        for j in i:
            output.append(j)
    return output


def to_binvector(m):
    '''
    :param m: матрица booleans
    :return: матрица int
    '''
    output = []
    for i in m:
        for j in i:
            output.append(1 if j else 0)
    return output


def to_matrix(region):
    return [[region.get_columns()[j * region.get_col_h() + i].get_is_active() for i in range(region.get_col_h())] for j
            in range(region.get_col_w())]


def to_binmatrix(m):
    output = [[]]
    r = 0
    for i in m:
        output.append([])
        for j in i:
            output[r].append(1 if j else 0)
        r = r + 1
    return output
