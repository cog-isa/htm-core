# -*- coding: utf8 -*-
from spatialPooler.sp_column import Column

__author__ = 'AVPetrov'


class Region:
    def __init__(self, setting, mapper):
        self.mapper = mapper
        self.columns = []
        self.setting = setting
        bottom_indices = mapper.map_all((self.setting.xinput, self.setting.yinput),
                                       (self.setting.xdimension, self.setting.ydimension),
                                       self.setting.potential_radius)

        for i in range(0, self.setting.xdimension):
            for j in range(0, self.setting.ydimension):
                self.columns.append((Column((i, j), bottom_indices[i*self.setting.ydimension+j], self)))

        return

    def get_columns(self):
        return self.columns

    def get_input_w(self):
        return self.setting.xinput

    def get_input_h(self):
        return self.setting.yinput

    def get_col_w(self):
        return self.setting.xdimension

    def get_col_h(self):
        return self.setting.ydimension
