from util import PASSIVE, ACTIVE


class Cell:
    def __init__(self, _id):
        self.id = _id
        self.dendrites = []
        self.state = PASSIVE
        self.new_state = PASSIVE
        self.state_mem = []
        self.passive_time = 0
        self.was_active = False

    def update_new_state(self, state):
        self.new_state = state

    def apply_new_state(self):
        self.state_mem.append(self.state)
        self.state = self.new_state
        self.passive_time += 1
        if self.state == ACTIVE:
            self.passive_time = 0
        self.new_state = PASSIVE



