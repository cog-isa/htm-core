# -*- coding: utf8 -*-
from math import floor

__author__ = 'AVPetrov'


class SimpleMapper:
    """
    Класс простого маппера. Отличается от очень простого маппера учетом количества колонок
    """
    @staticmethod
    def map_one(input_wh, colcoord, radius):
        """
        возвращает массив кортежей координат элементов входного поля input_wh, которые отнесены к колонке с координатами colcoord
        :param input_wh: размеры входного поля
        :param colcoord: координаты колонки в поле колонок (подразумевается, что размерность входного поля и поля колонок одинакова)
        :param radius: половина стороны квадрата с центром в колонке
        :return: массив кортежей координат элементов входного поля input_wh, которые отнесены к колонке с координатами colcoord
        """
        indices = []
        for i in range(colcoord[0] - radius, colcoord[0] + radius+1):
            if 0 <= i < input_wh[0]:
                for j in range(colcoord[1] - radius, colcoord[1] + radius+1):
                    if 0 <= j < input_wh[1]:
                        indices.append((i, j))
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
                input_center_x = i + floor((input_wh[0] - cols_wh[0]) / 2)
                input_center_y = j + floor((input_wh[1] - cols_wh[1]) / 2)
                indices = self.map_one(input_wh, (input_center_x, input_center_y), radius)
                cols_map_input.append(indices)

        return cols_map_input
