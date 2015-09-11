from temporalPooler.htm_cell import Cell
from temporalPooler.util import *


class Column:
    """
    Колонка региона
    """
    def __init__(self, size):
        """
        инициализация колонки
        :param size: размер колонки - количество клеток в ней
        :return:
        """
        self.cells = [Cell(0) for _ in range(size)]
        self.state = PASSIVE
