from temporalPooler.htm_cell import Cell
from temporalPooler.util import *


class Column:

    def __init__(self, size):
        self.cells = [Cell(0) for _ in range(size)]
        self.state = PASSIVE
