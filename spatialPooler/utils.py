# -*- coding: utf8 -*-
from math import sqrt

__author__ = 'AVPetrov'


def get_distance(p1,p2):
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


def kth_score(overlaps, k):
    return sorted(overlaps)[len(overlaps) - k]

def to_vector(m):
    output = []
    for i in m:
        for j in i:
            output.append(j)
    return output


def to_matrix(region):
    return [[region.get_columns()[j * region.get_col_h() + i].get_is_active() for i in range(region.get_col_h())] for j
            in range(region.get_col_w())]