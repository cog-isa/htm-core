class Synapse:

    def __init__(self, id_to, permanence):
        self.id_to = id_to
        self.permanence = permanence

    def change_permanence(self, delta):
        self.permanence += delta
        self.permanence = min(1.0, self.permanence)
        self.permanence = max(0.0, self.permanence)
