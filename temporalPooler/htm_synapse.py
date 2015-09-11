class Synapse:
    """
    синапс дендрита
    """

    def __init__(self, id_to, permanence):
        """
        инициализация синапса
        :param id_to: клетка,к которой подключен синапс
        :param permanence: перманентность - значение его силы
        :return:
        """
        self.id_to = id_to
        self.permanence = permanence

    def change_permanence(self, delta):
        """
        изменить перманентность синапса
        :param delta: дельта,на которую будет изменена перманетность
        перманетность может лежать в отрезке - [0,1]
        :return:
        """
        self.permanence += delta
        self.permanence = min(1.0, self.permanence)
        self.permanence = max(0.0, self.permanence)
