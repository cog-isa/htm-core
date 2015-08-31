# -*- coding: utf8 -*-
from math import sqrt

__author__ = 'AVPetrov'


def get_distance(p1,p2):
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)


def kth_score(overlaps, k):
    return sorted(overlaps)[len(overlaps) - k]
