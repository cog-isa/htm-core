from settings import *
from htm_synapse import Synapse


class Dendrite:
    def __init__(self, cells=None):
        self.prediction = False
        self.synapses = []
        self.active = False

        if cells:
            self.synapses = [Synapse(id_to=cell.id, permanence=INITIAL_PERMANENCE) for cell in cells]

    def add_synapse(self, synapse):
        self.synapses.append(synapse)

    def get_synapses(self):
        return self.synapses

    def equal(self, other):
        a = set()
        b = set()
        for i in self.synapses:
            a.add(i.id_to)
        for i in other.synapses:
            b.add(i.id_to)
        return len(a ^ b) == 0