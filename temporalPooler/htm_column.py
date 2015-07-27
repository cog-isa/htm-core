from htm_cell import Cell
from util import *


class Column:

    def __init__(self, size):
        self.cells = [Cell(0) for _ in range(size)]
        self.state = PASSIVE

