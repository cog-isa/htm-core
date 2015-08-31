# -*- coding: utf8 -*-
__author__ = 'AVPetrov'


# /**
#  * Класс очень простого маппера. Он не знает сколько всего колонок и просто проецирует колонку на входную матрицу -
#  * получает центр рецептивного поля с определенным радиусом
#  */
class VerySimpleMapper:

    # // возвращает массив кортежей координат элементов входного поля inputWH, которые отнесены к колонке
    # // с координатами colCoord
    # // inputWH - размеры входного поля
    # // colCoord - координаты колонки в поле колонок (подразумевается, что размерность входного поля и поля колонок
    # // одинакова)
    # // radius - половина стороны квадрата с центром в колонке
    @staticmethod
    def map_оne(input_wh, colcoord, radius):
        indices = []
        for i in range(colcoord[0] - radius, colcoord[0] + radius + 1):
            if 0 <= i < input_wh[0]:
                for j in range(colcoord[1] - radius, colcoord[1] + radius + 1):
                    if 0 <= j < input_wh[1]:
                        indices.append((i, j))
        return indices

    # // возвращает список, в котором для каждой колонки указаны индексы связанных с ней элементов нижлежащего слоя
    def map_all(self, input_wh, cols_wh, radius):
        if (input_wh[0] < cols_wh[0])or(input_wh[1] < cols_wh[1]):
            raise NameError("Колонок как минимум по одному из измерений больше, чем элементов нижлежащего слоя "
                            "по соответствующему измерению.")

        if (input_wh[0] < cols_wh[0]*(2*radius+1))or(input_wh[1] < cols_wh[1]*(2*radius+1)):
            raise NameError("Число колонок, умноженное на 2*radius+1, как минимум по одному из измерений больше, "
                            "чем элементов нижлежащего слоя по соответствующему измерению.")

        cols_map_input = []

        for i in range(0, cols_wh[0]):
            for j in range(0, cols_wh[1]):
                input_center_x = i * (2 * radius + 1) + radius
                input_center_y = j * (2 * radius + 1) + radius
                indices = self.map_оne(input_wh, (input_center_x, input_center_y), radius)
                cols_map_input.append(indices)

        return cols_map_input
