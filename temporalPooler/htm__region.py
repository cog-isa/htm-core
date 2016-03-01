from random import randrange

from apps.settings import TemporalSettings
from temporalPooler.htm_column import Column
from temporalPooler.util import ACTIVE, PREDICTION, PASSIVE
from temporalPooler.htm_dendrite import Dendrite


class Region:
    """
    Регион htm, реализует основую логику временного группировщика
    """

    def __init__(self, temporal_settings: TemporalSettings):
        """
        инициализация региона
        :param temporal_settings: настройки региона
        :return:
        """

        self.columns = [[Column(temporal_settings.column_size) for _ in range(temporal_settings.region_size)] for _ in
                        range(temporal_settings.region_size)]
        self.ptr_to_cell = {}
        self.ok_times = 0
        self.ok = 0
        self.max_ok_times = 0
        self.very_ok_times = 0
        self.a = None

        self.correctness = 0
        self.correctness_sum = 0
        self.correctness_steps = 0

        self.memorized_max_size = 500
        self.memorized_correctness = []

        self.average_correctness_max_size = 500
        self.average_correctness = []

        # забираем свободные id для клеток, чтобы не было ссылочных конфликтов с другими регионами
        self.start_cells_id = temporal_settings.free_id
        temporal_settings.free_id += len(self.columns) * len(self.columns[0]) * temporal_settings.column_size

        self.temporal_settings = temporal_settings

    def get_active_cells(self):
        """
        получить активные клетки
        :return: список активных клеток
        """
        res = []
        for i in range(self.temporal_settings.region_size):
            for j in range(self.temporal_settings.region_size):
                for cell in self.columns[i][j].cells:
                    if cell.state == ACTIVE:
                        res.append(cell)

        return res

    def update_correctness(self, a):
        """
        обновить значение правильности предсказания - поле self.correctness
        :param a: матрица активных колонок на текущем шаге
        :return:
        """
        events = 0
        errors = 0
        for i in range(self.temporal_settings.region_size):
            for j in range(self.temporal_settings.region_size):
                column_state = PASSIVE

                for cell in self.columns[i][j].cells:
                    if cell.state == PREDICTION:
                        column_state = PREDICTION
                        break

                if column_state == PREDICTION and a[i][j]:
                    events += 1
                if column_state != PREDICTION and a[i][j]:
                    events += 1
                    errors += 1
                if column_state == PREDICTION and not a[i][j]:
                    events += 1
                    errors += 1
        if events > 0:
            self.correctness = 1.0 * (events - errors) / events
        else:
            # на вход поступила пустая матрица и мы ничего не предсказали
            self.correctness = 1.0

        self.correctness_steps += 1
        self.correctness_sum += self.correctness

        # храним срез среднего ариф. интегральных сумм
        self.average_correctness.append(self.correctness_sum / self.correctness_steps)
        while len(self.average_correctness) > self.average_correctness_max_size:
            self.average_correctness = self.average_correctness[1:]

        # сохраняем значение correctness, храним не больше memorized_size последних значений
        self.memorized_correctness.append(self.correctness)
        while len(self.memorized_correctness) > self.memorized_max_size:
            self.memorized_correctness = self.memorized_correctness[1:]

    @staticmethod
    def check_column_state(column, a):
        """
        проверить состояние колонки - правильно ли предсказана/не прадсказана
        :param column: проверяемая колонка
        :param a: матрица активных колонок на текущем шаге
        :return: True или False, а в зависимости от результата
        """
        ok = False
        for cell in column.cells:
            if cell.state == PREDICTION and not a:
                return False
            if cell.state == PREDICTION and a:
                ok = True
        if not ok and a:
            return False
        return True

    def prediction_was_ok(self, a):
        """
        функция проверяет полную правильность предсказания
        :param a: матрица активных колонок на текущем шаге
        :return: True или False, а в зависимости от результата
        """
        for i in range(self.temporal_settings.region_size):
            for j in range(self.temporal_settings.region_size):
                if not self.check_column_state(self.columns[i][j], a[i][j]):
                    return False
        return True

    def update_columns_state(self, a):
        """
        функция обновляет состояние колонок
        :param a: матрица активных колонок на текущем шаге
        :return:
        """
        # обновляем состояние колонок по поступившим данным от пространственного группировщика
        for i in range(self.temporal_settings.region_size):
            for j in range(self.temporal_settings.region_size):
                self.columns[i][j].state = ACTIVE if a[i][j] else PASSIVE

    @staticmethod
    def column_satisfies(column, active, prediction):
        """
        возвращает булевское значение, удовлетворяет ли колонка заданным параметрам,
        если active или prediction является None - то колонка нам подходит точно
        :param column: проверяемая колонка
        :param active: булевская переменная,активная нам нужна колонка или нет ИЛИ None - этот параметр на не важен
        :param prediction: булевская переменная или None - этот параметр не важен
        :return: возвращает булевскую переменную - удовлетворяет ли требованиям данная колонка
        """

        if active is not None:
            if (column.state == ACTIVE and not active) or (column.state == PASSIVE and active):
                return False

        if prediction is not None:
            is_prediction = False
            for cell in column.cells:
                if cell.state == PREDICTION:
                    is_prediction = True
            if is_prediction != prediction:
                return False

        return True

    def get_columns(self, active=None, prediction=None):
        """
        проверяет каждую из колонок региона на соответвие требованиям,возвращает список подходящих колонок
        :param active: фильтр:
            True - нам подходят только активные колонки
            False - нам НЕ подходят активные колонки
            None - подходят и активные и неактивные
        :param prediction: фильтр:
            True - нам подходят только колонки находящиеся в состоянии предсказания
            False - нам НЕ подходят только колонки находящиеся в состоянии предсказания
            None - подходят любые
        :return: список подходящих колонок
        """

        return [self.columns[i][j] for i in range(self.temporal_settings.region_size) for j in
                range(self.temporal_settings.region_size) if
                self.column_satisfies(self.columns[i][j], active, prediction)]

    def get_ptr_to_cells(self):
        res = {}
        cnt = self.start_cells_id
        for i in self.columns:
            for j in i:
                for k in j.cells:
                    k.id = cnt
                    res[k.id] = k
                    cnt += 1
        return res

    def step_forward(self, a, do_not_make_prediction_and_apply_cell_states=None):
        """
        основная функция пересчета региона, выполняются такие функции как:
            - подсчет ошибки (проверка правильности предсказания)
            - вычисление слудющего состояния каждой из колонок
            - обновление перманетностей синапсов в дендритах и создание новых дендритов

        :param a: матрица активных колонок на текущем шаге
        :return:
        """
        # считаем ошибку
        self.update_correctness(a)

        # создаем словарь ссылок на клетки по id
        self.ptr_to_cell = self.get_ptr_to_cells()

        self.update_columns_state(a)

        # получаем активные на предыдущем шаге клетки
        active_cells = self.get_active_cells()

        for column in self.get_columns(active=True, prediction=True):
            # рассматриваем все колонки,которые были правильно предсказаны

            # первым делом проверим может в этой колонке есть клетка,которая очень давно не активировалсь, если она
            # есть тогда мы ее активируем

            for cell in column.cells:
                active_from_passive_time = False
                if cell.passive_time > self.temporal_settings.passive_time_to_active_threshold:
                    # назначаем следующее состояние клетки - активным
                    cell.update_new_state(ACTIVE)
                    active_from_passive_time = True
                    cell.active_from_passive_time = True
                if active_from_passive_time:
                    break

            # если такой клетки нет - то активируем клетку правильно сделавшую предсказание

            for cell in column.cells:
                if cell.state == PREDICTION:
                    # назначаем следующее состояние клетки - активным
                    cell.update_new_state(ACTIVE)

                    # увеличиваем перманентность дендритов, который привели к активации данной колонки
                    for dendrite in cell.dendrites:
                        if dendrite.active:
                            for syn in dendrite.synapses:
                                if syn.id_to in [a_cell.id for a_cell in active_cells]:
                                    syn.change_permanence(self.temporal_settings.dendrite_permanence_inc_delta)

        for column in self.get_columns(active=False, prediction=True):
            # рассматриваем все колонки,который были предсказаны неправильно

            # уменьшаем перманентность дендритов, которые привели к активации данной колонки
            for cell in column.cells:
                if cell.state == PREDICTION:
                    for dendrite in cell.dendrites:
                        if dendrite.active:
                            for syn in dendrite.synapses:
                                if syn.id_to in [a_cell.id for a_cell in active_cells]:
                                    syn.change_permanence(self.temporal_settings.dendrite_permanence_dec_delta)
            pass

        for column in self.get_columns(active=True, prediction=False):
            # рассматриваем все колонки, которые не были предсказаны

            # активируем каждую из клеток, также добавляем новый дендрит или незначительно увеличиваем
            # перманентность у текущего если такой дендрит уже есть
            ok = False

            while not ok:
                for cell in column.cells:
                    if cell.new_state == PASSIVE and randrange(3) == 2:
                        cell.update_new_state(ACTIVE)
                        ok = True

                        new_den = Dendrite(temporal_settings=self.temporal_settings, cells=active_cells)
                        for dendrite in cell.dendrites:
                            if dendrite.equal(new_den):
                                new_den = None
                                for synapse in dendrite.synapses:
                                    if synapse.id_to in [a_cell.id for a_cell in active_cells]:
                                        synapse.change_permanence(
                                            self.temporal_settings.dendrite_permanence_inc_delta * 0.1)
                                break
                        if new_den:
                            cell.dendrites.append(new_den)
            pass

        for _ in self.get_columns(active=False, prediction=False):
            # рассматриваем все колонки которые не были предсказаны и не активировались
            pass

        # обнуляем актиновность всех дендритов
        for column in self.get_columns():
            for cell in column.cells:
                for dendrite in cell.dendrites:
                    dendrite.was_active = dendrite.active
                    dendrite.active = False

        if not do_not_make_prediction_and_apply_cell_states:
            self.make_prediction()

        # проверяем предыдущее предсказание
        if self.prediction_was_ok(a):

            self.very_ok_times += 1
            self.max_ok_times = max(self.max_ok_times, self.very_ok_times)
            # print('Предсказание было правильным.')
        else:
            self.very_ok_times = 0
        if not do_not_make_prediction_and_apply_cell_states:
            self.apply_new_cell_state()
            # применяем новое состояние клеток

    def make_prediction(self):
        # делаем предсказание
        for i in range(self.temporal_settings.region_size):
            for j in range(self.temporal_settings.region_size):
                current_column = self.columns[i][j]
                mx = 0
                dendrite_mx = None
                cell_for_update = current_column.cells[0]

                for current_cell in current_column.cells:
                    for dendrite in current_cell.dendrites:
                        q = 0
                        for syn in dendrite.synapses:
                            if self.ptr_to_cell[syn.id_to].new_state == ACTIVE \
                                    and syn.permanence > self.temporal_settings.synapse_threshold:
                                q += 1
                        if q > mx and current_cell.new_state == PASSIVE:
                            # в состояние предсказание может перейти только пассивная клетка
                            mx = q
                            cell_for_update = current_cell
                            dendrite_mx = dendrite
                if mx >= self.temporal_settings.dendrite_activate_threshold:
                    dendrite_mx.active = True
                    cell_for_update.update_new_state(PREDICTION)

    def apply_new_cell_state(self):
        for i in range(self.temporal_settings.region_size):
            for j in range(self.temporal_settings.region_size):
                for cell in self.columns[i][j].cells:
                    cell.apply_new_state()

    def out_prediction(self):
        """
        вывод текстовой информации состояния региона
        :return:
        """
        res = [["" for _ in range(self.temporal_settings.region_size)] for _ in
               range(self.temporal_settings.region_size)]
        for i in range(self.temporal_settings.region_size):
            for j in range(self.temporal_settings.region_size):
                cnt = 0
                for cell in self.columns[i][j].cells:
                    cnt += 1

                    if cell.state == PREDICTION:
                        res[i][j] += "P" + str(cnt)
                    if cell.state == ACTIVE and not cell.active_from_passive_time:
                        res[i][j] += "A" + str(cnt)
                    # клетка активировалсь из-за долгого простоя
                    if cell.active_from_passive_time:
                        res[i][j] += "O" + str(cnt)
                        cell.active_from_passive_time = False
                if res[i][j] == '':
                    res[i][j] = "  "
        print("Правильно предсказано раз: ", self.very_ok_times)
        print("Максимально правильно предсказано раз: ", self.max_ok_times)
        print("Корректность: ", self.correctness_sum / self.correctness_steps)
        for i in res:
            print(i)
        print()

    def get_binary_prediction(self):
        """
        вывод информации о колонках в состоянии предсказания
        :return:матрица состояния состояния колонок 1 если колонка в состоянии предсказания
        """

        res = [[0 for _ in range(self.temporal_settings.region_size)] for _ in
               range(self.temporal_settings.region_size)]

        for i in range(self.temporal_settings.region_size):
            for j in range(self.temporal_settings.region_size):
                for cell in self.columns[i][j].cells:
                    if cell.state == PREDICTION:
                        res[i][j] = 1
        return res

    def get_predicted_cells_ids(self):
        """
        отдает список id-шников активных клеток региона
        :return: список id-шников активных клеток региона
        """
        t = []
        for i in range(self.temporal_settings.region_size):
            for j in range(self.temporal_settings.region_size):
                for cell in self.columns[i][j].cells:
                    if cell.state == PREDICTION:
                        t.append(cell)
        return map(lambda x: x.id, t)