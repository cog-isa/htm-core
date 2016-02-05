from apps.settings import TemporalSettings
from temporalPooler.htm_synapse import Synapse


class Dendrite:
    """
    дендрит,подключенный к клетке
    """

    def __init__(self, temporal_settings: TemporalSettings, cells=None):
        """
        инициализация дендрита
        :param cells: клетки к которым он подключается
        :return:
        """
        self.prediction = False
        self.synapses = []
        self.active = False
        self.was_active = False
        self.temporal_settings = temporal_settings

        if cells:
            self.synapses = [Synapse(id_to=cell.id, permanence=self.temporal_settings.initial_permanence) for cell in
                             cells]

    def add_synapse(self, synapse):
        """
        добавление синапса
        :param synapse: добавляемый синапс
        :return:
        """
        self.synapses.append(synapse)

    def get_synapses(self):
        """
        получить синапсы
        :return:список синапсов дендрита
        """
        return self.synapses

    def equal(self, other):
        """
        проверить дендриты на эквивалентность - совпадение всех синапсов (перманентности синапсов могу отличаться)
        :param other: второй дендрит
        :return: булевское значение - эквивалентны или нет
        """
        a = set()
        b = set()
        for i in self.synapses:
            a.add(i.id_to)
        for i in other.synapses:
            b.add(i.id_to)
        return len(a ^ b) == 0
