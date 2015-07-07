class Synapse:
    def __init__(self, id_to, permanence):
        self.id_to = id_to
        self.permanence = permanence

    def change_permanence(self, delta):
        self.permanence += delta
        if self.permanence > 1:
            self.permanence = 1
        if self.permanence < 0:
            self.permanence = 0