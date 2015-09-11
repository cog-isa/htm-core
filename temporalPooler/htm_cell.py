from temporalPooler.util import PASSIVE, ACTIVE
from random import randrange


class Cell:
    """
    Клетка колонки
    """

    def __init__(self, _id):
        """
        конструктор класса
        :param _id: id клетки
        :return:
        """

        self.id = _id
        self.dendrites = []
        self.state = PASSIVE
        self.new_state = PASSIVE
        self.passive_time = 0
        self.was_active = False
        self.active_from_passive_time = False

    def update_new_state(self, state):
        """
        заменяет новое состояние клетки на полученное параметров
        :param state: новое состояние клетки
        :return:
        """
        self.new_state = state

    def apply_new_state(self):
        """
        обновляет состояние клетки,а также пересчитывает поле passive_time в зависимости от состояние клетки
        :return:
        """
        self.state = self.new_state
        # очень важно
        self.passive_time += 40 + randrange(0, 10)
        if self.state == ACTIVE:
            self.passive_time = 0
        self.new_state = PASSIVE
