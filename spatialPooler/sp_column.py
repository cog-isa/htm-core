# -*- coding: utf8 -*-
import random

from spatialPooler.sp_cell import Cell
from spatialPooler.sp_synapse import Synapse
from spatialPooler.utils import get_distance

__author__ = 'AVPetrov'


class Column:
    def __init__(self, coords, bottom_indices, region):
        self.setting = region.settings
        self.bottom_indices = bottom_indices
        self.potential_radius = self.setting.potential_radius
        self.connected_pct = self.setting.connected_pct
        self.r = region
        self.is_active = False
        self.neighbors = []
        self.col_coords = coords
        self.cells = [Cell(0) for i in range(0, self.setting.cells_per_column+1)]
        # хэш синапсов: индекс элемента с которым соединение и сам синапс
        self.potential_synapses = {}
        self.boost_factor = 1
        self.init_synapses()
        self.update_neighbors(self.setting.initial_inhibition_radius)

    def get_index(self):
        return self.col_coords[0]*self.setting.ydimension+self.col_coords[1]

    # /**
    #  * Изменение списка соседних колонок, которые отстоят от данной в круге радиусом inhibitionRadius
    #  * @param inhibitionRadius радиус подавления (в начале назначется из настроек, потом берется как усредненный
    #  * радиус рецептивного поля)
    #  */
    def update_neighbors(self, inhibition_radius):
        self.neighbors = []
        for k in range(self.col_coords[0] - inhibition_radius, self.col_coords[0] + inhibition_radius+1):
            if 0 <= k < self.setting.xdimension:
                for m in range(self.col_coords[1] - inhibition_radius, self.col_coords[1] + inhibition_radius+1):
                    if 0 <= m < self.setting.ydimension:
                        if k != self.col_coords[0] or m != self.col_coords[1]:
                            self.neighbors.append(k * self.setting.ydimension + m)

    def get_neighbors(self):
        return self.neighbors

    def set_is_active(self, is_active):
        self.is_active = is_active

    def get_is_active(self):
        return self.is_active

    def get_coord(self):
        return self.col_coords

    def get_potential_synapses(self):
        return self.potential_synapses

    def get_connected_synapses(self):
        conn_syn = []
        for s in self.potential_synapses.values():
            if s.is_connected():
                conn_syn.append(s)
        return conn_syn

    def get_boost_factor(self):
        return self.boost_factor

    def set_boost_factor(self, boost_factor):
        self.boost_factor = 1  # boost_factor

    def stimulate(self):
        for synapse in self.potential_synapses.values():
            synapse.increase_permanence()

    def init_synapses(self):
        center = self.bottom_indices[len(self.bottom_indices)//2]

        if not self.setting.debug:
            random.shuffle(self.bottom_indices)

        # // выберем только часть синапсов для данной колонки (если set.connectedPct<1)
        # // предполагается, что set.connectedPct<1, в том случае, если рецептивные поля различных колонок пересекаются
        num_potential = round(len(self.bottom_indices) * self.connected_pct)
        for i in range(0, num_potential):
            coord = self.bottom_indices[i]
            index = coord[0]*self.setting.yinput+coord[1]
            synapse = Synapse(self.setting, index, 0)
            # //радиальное затухание перманентности от центра рецептивного поля колонки
            # //double k = MathUtils.distFromCenter(index, set.potentialRadius, set.xDimension, set.yDimension);
            k = get_distance(coord, center)
            synapse.init_permanence(k)
            self.potential_synapses[index] = synapse
