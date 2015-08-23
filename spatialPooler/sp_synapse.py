# -*- coding: utf8 -*-
import random

__author__ = 'AVPetrov'


class Synapse:
    def __init__(self, settings, index_connect_to, init_permanence):
        self.settings = settings
        self.index_connect_to = index_connect_to
        self.permanence = init_permanence
        self.rand = random.Random()
        self.rand.seed = 10

    # /**
    #  * Случайные значения преманентности должны быть из малого диапазона около connectedPerm
    #  */
    def init_permanence(self, k):
        if self.settings.debug:
            self.permanence = self.settings.connected_perm
            self.permanence *= (1/(0.5 if k == 0 else k))
        else:
            if self.rand.nextDouble() <= self.settings.connected_pct:
                self.permanence = self.settings.connected_perm + self.rand.random() * self.settings.permanence_inc / 4.0
            else:
                self.permanence = self.settings.connected_perm - self.rand.random() * self.settings.permanence_inc / 4.0
                self.permanence *= (1/(0.5 if k == 0 else k))

    def increase_permanence(self):
        self.permanence += self.settings.permanence_inc
        self.permanence = 1 if self.permanence > 1 else self.permanence

    def decrease_permanence(self):
        self.permanence -= self.settings.permanence_dec
        self.permanence = 0 if self.permanence < 0 else self.permanence

    def is_connected(self):
        if self.settings.debug:
            return True
        else:
            return self.permanence > self.settings.connected_perm

    # /* connectToIndex - это либо номер бита из сигнала снизу, либо номер клетки (аксон) при латеральной связи */
    def get_index_connect_to(self):
        return self.index_connect_to

    # /* Получить степени связанности между аксоном и дендритом. */
    def get_permanence(self):
        return self.permanence

    # /* Установить степени связанности между аксоном и дендритом. */
    def set_permanence(self, permanence):
        self.permanence = permanence
