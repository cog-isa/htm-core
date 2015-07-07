class Dendrite:
    def __init__(self):
        self.prediction = False
        self.synapses = []
        self.active = False

    def add_synapse(self, synapse):
        self.synapses.append(synapse)

    def get_synapses(self):
        return self.synapses