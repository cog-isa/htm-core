# -*- coding: utf8 -*-
from spatialPooler.sp_column import Column
from spatialPooler.utils import kth_score, to_vector, to_matrix
import random

__author__ = 'AVPetrov'


class Region:
    def __init__(self, settings, mapper):
        self.mapper = mapper
        self.columns = []
        self.settings = settings
        self.active_duty_cycles = [0 for i in range(self.settings.xdimension*self.settings.ydimension)]
        self.overlap_duty_cycles = [0 for i in range(self.settings.xdimension*self.settings.ydimension)]
        bottom_indices = mapper.map_all((self.settings.xinput, self.settings.yinput),
                                       (self.settings.xdimension, self.settings.ydimension),
                                       self.settings.potential_radius)

        for i in range(0, self.settings.xdimension):
            for j in range(0, self.settings.ydimension):
                self.columns.append((Column((i, j), bottom_indices[i*self.settings.ydimension+j], self)))

        return

    def get_columns(self):
        return self.columns

    def get_input_w(self):
        return self.settings.xinput

    def get_input_h(self):
        return self.settings.yinput

    def get_col_w(self):
        return self.settings.xdimension

    def get_col_h(self):
        return self.settings.ydimension

    def get_active_duty_cycles(self):
        return self.active_duty_cycles

    # Вычисление значения перекрытия каждой колонки с заданным входным вектором.
    # @param input - входной сигнал
    # @param cols - колонки
    # @return значения переключения для каждой колонки
    @staticmethod
    def update_overlaps(cols, inp):
        overlaps = [0 for i in range(len(cols))]
        i = 0
        for c in cols:
            for s in c.get_connected_synapses():
                overlaps[i] += (1 if inp[s.get_index_connect_to()] == 1 else 0)
            i += 1
        return overlaps

    # Вычисление колонок, остающихся победителями после применения взаимного подавления.
    def inhibition_phase(self, cols, overlaps):
        for c in cols:
            c.set_is_active(False)
        active_columns = []

        indexies = [i for i in range(len(cols))]
        random.shuffle(indexies)
        for indx in indexies:
            column = cols[indx]
            if len(column.get_neighbors()) > 0:
                # выборка перекрытий колонок, соседних с данной
                neighbor_overlaps = [overlaps[i] for i in column.get_neighbors()]
                # определить порог перекрытия
                minlocal_overlap = kth_score(neighbor_overlaps, self.settings.desired_local_activity)
                # если колонка имеет перекрытие большее, чем у соседей, то она становиться активной

                if overlaps[column.get_index()] > 0 and overlaps[column.get_index()] >= minlocal_overlap:
                    # для случая одинаковых оверлапов у выбраныных соседей
                    n = 0
                    for i in column.get_neighbors():
                        n += (1 if self.find_by_colindex(cols, i).get_is_active() else 0)
                    if n <= (self.settings.desired_local_activity-1):  # -1 - считая саму колонку
                        column.set_is_active(True)
                        active_columns.append(column)
                else:
                    column.set_is_active(False)
        return active_columns

    @staticmethod
    def find_by_colindex(cols, index):
        for c in cols:
            if c.get_index() == index:
                return c
        return None

    # Если синапс был активен (через него шел сигнал от входного вектора), его значение преманентности увеличивается,
    # а иначе - уменьшается.
    # @param inp - входной сигнал
    @staticmethod
    def update_synapses(cols, inp):
        for col in cols:
            for synapse in col.get_potential_synapses().values():
                if inp[synapse.get_index_connect_to()]:
                    synapse.increase_permanence()
                else:
                    synapse.decrease_permanence()

    def update_active_duty_cycle(self, cols):
        for i in range(len(cols)):
            self.active_duty_cycles[i] += 1 if cols[i].get_is_active() else 0

    def update_overlap_duty_cycle(self, col, overlaps):
        self.overlap_duty_cycles[col.get_index()] += 1 if overlaps[col.get_index()] > self.settings.min_overlap else 0

    # Если activeDutyCycle больше minValue, то значение ускорения равно 1. Ускорение начинает линейно увеличиваться
    # как только activeDutyCycle колонки падает ниже minDutyCycle.
    #
    # @param minValue - минимальнео число активных циклов
    def update_boost_factor(self, col, min_value):
        value = 1

        if self.active_duty_cycles[col.get_index()] < min_value :
                value = 1 + (min_value - self.active_duty_cycles[col.get_index()]) * (self.settings.max_boost - 1)
        col.set_boost_factor(value)

    # Обновление значений перманентности, фактора ускорения и радиуса подавления колонок.
    # Механизм ускорения работает в том случае, если колонка не побеждает достаточно долго (activeDutyCycle).
    # Если колонка плохо перекрывается с входным сигналом достоачно долго (overlapDutyCycle), то увеличиваются
    # перманентности.
    def learning_phase(self, cols, inp, overlaps):

        # 1. изменить значения перманентности всех синапсов проксимальных сегментов *активных* колонок
        self.update_synapses(cols, inp)

        for column in cols:
            # определить максимальное число срабатываний колонки среди соседей колонки и её самой колонку
            max_active_duty = 0
            for index in column.get_neighbors():
                max_active_duty = max_active_duty  if max_active_duty > self.active_duty_cycles[index] else self.active_duty_cycles[index]

            # определить минимальное число срабатываний (% от maxActiveDuty)
            min_duty_cycle = self.settings.min_duty_cycle_fraction * max_active_duty

            self.update_boost_factor(column,min_duty_cycle)

            self.update_overlap_duty_cycle(column,overlaps)
            # если колонка редко срабатывает стимулировать её
            if self.overlap_duty_cycles[column.get_index()] < min_duty_cycle:
                column.stimulate()

            # TODO: в оригинальной реализиации радиус менялся и соседи тоже...
            # column.update_neighbors(averageReceptiveFieldSize())

        # теперь обновим activeDutyCycle всех колонок.
        self.update_active_duty_cycle(cols)

    def step_forward(self, input):
        inp = to_vector(input)
        ov = self.update_overlaps(self.get_columns(), inp)
        self.inhibition_phase(self.get_columns(), ov)
        self.learning_phase(self.get_columns(),inp,ov)
        return to_matrix(self)

    def out_prediction(self):
        output=[[0 for i in range(0, self.get_input_h())] for i in range(0, self.get_input_w())]
        for col in self.columns:
            if col.get_is_active():
                for syn in col.get_potential_synapses():
                    x = syn.get_index_connect_to() / self.get_input_h()
                    y = syn.get_index_connect_to() % self.get_input_w()
                    output[x][y]=min(output[x][y]+syn.get_permanence(),1)
        return output
