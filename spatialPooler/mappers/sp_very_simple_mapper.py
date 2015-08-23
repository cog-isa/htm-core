# -*- coding: utf8 -*-
__author__ = 'AVPetrov'


# /**
#  * Класс очень простого маппера. Он не знает сколько всего колонок и просто проецирует колонку на входную матрицу -
#  * получает центр рецептивного поля с определенным радиусом
#  */
class verySimpleMapper:

    # // возвращает массив кортежей координат элементов входного поля inputWH, которые отнесены к колонке с координатами colCoord
    # // inputWH - размеры входного поля
    # // colCoord - координаты колонки в поле колонок (подразумевается, что размерность входного поля и поля колонок одинакова)
    # // radius - половина стороны квадрата с центром в колонке
    def mapOne(self,inputWH, colCoord, radius):
        indices = []
        for i in range(colCoord[0] - radius,colCoord[0] + radius+1):
            if (i >= 0 and i < inputWH[0]):
                for j in range(colCoord[1] - radius,colCoord[1] + radius+1):
                    if (j >= 0 and j < inputWH[1]):
                        indices.append((i,j));
        return indices;

    # // возвращает список, в котором для каждой колонки указаны индексы связанных с ней элементов нижлежащего слоя
    def mapAll(self, inputWH, colsWH, radius):
        if((inputWH[0] < colsWH[0])or(inputWH[1] < colsWH[1])):
            raise NameError("Колонок как минимум по одному из измерений больше, чем элементов нижлежащего слоя по соответствующему измерению.");

        if((inputWH[0] < colsWH[0]*(2*radius+1))or(inputWH[1] < colsWH[1]*(2*radius+1))):
            raise NameError("Число колонок, умноженное на 2*radius+1, как минимум по одному из измерений больше, чем элементов нижлежащего слоя по соответствующему измерению.");

        cols_map_input= []

        for i in range(0,colsWH[0]):
            for j in range(0,colsWH[1]):
                inputCenterX = (i)*(2*radius+1)+radius;
                inputCenterY = (j)*(2*radius+1)+radius;
                indices = self.mapOne(inputWH, (inputCenterX, inputCenterY), radius);
                cols_map_input.append(indices);

        return cols_map_input;