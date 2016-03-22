# -*- coding: utf8 -*-
from math import floor
from random import randrange

__author__ = 'AVPetrov'


class RandomMapper:
    """
    Класс случайного маппера
    """
    def map_one(self, input_wh, colcoord, radius):
        """
        возвращает массив кортежей координат элементов входного поля input_wh, которые отнесены к колонке с координатами colcoord
        :param input_wh: размеры входного поля
        :param colcoord: координаты колонки в поле колонок (подразумевается, что размерность входного поля и поля колонок одинакова)
        :param radius: половина стороны квадрата с центром в колонке
        :return: массив кортежей координат элементов входного поля input_wh, которые отнесены к колонке с координатами colcoord
        """
        indices = []

        i = 0
        while i < radius*radius:
            indices.append((randrange(0,input_wh[0]), randrange(0,input_wh[1])))
            i = i + 1

        return indices

    def map_all(self, input_wh, cols_wh, radius):
        """
        возвращает список, в котором для каждой колонки указаны индексы связанных с ней элементов нижлежащего слоя
        :param input_wh: размеры входного поля
        :param colcoord: координаты колонки в поле колонок (подразумевается, что размерность входного поля и поля колонок одинакова)
        :param radius: половина стороны квадрата с центром в колонке
        :return: список, в котором для каждой колонки указаны индексы связанных с ней элементов нижлежащего слоя
        """
        if (input_wh[0] < cols_wh[0])or(input_wh[1] < cols_wh[1]):
            raise NameError("Колонок как минимум по одному из измерений больше, чем элементов нижлежащего слоя "
                            "по соответствующему измерению.")

        cols_map_input = []

        for i in range(0, cols_wh[0]):
            for j in range(0, cols_wh[1]):
                indices = self.map_one(input_wh, 0, radius)
                cols_map_input.append(indices)

        return cols_map_input
