from util import PASSIVE, ACTIVE
from random import randrange

class Cell:
    def __init__(self, _id):
        self.id = _id
        self.dendrites = []
        self.state = PASSIVE
        self.new_state = PASSIVE
        self.passive_time = 0
        self.was_active = False
        self.error_impulse = 0
        self.ololo = False

    def update_new_state(self, state):
        self.new_state = state

    def apply_new_state(self):
        self.state = self.new_state
        # очень важно
        self.passive_time += 40 + randrange(0, 10)
        if self.state == ACTIVE:
            self.passive_time = 0
        self.new_state = PASSIVE


