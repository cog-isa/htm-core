from temporalPooler.htm_column import Column
from temporalPooler.util import ACTIVE, PREDICTION, PASSIVE
from apps.settings import *
from temporalPooler.htm_dendrite import Dendrite
from random import randrange


class Region:
    def __init__(self, region_size, column_size):
        self.region_size = region_size
        self.columns = [[Column(column_size) for _ in range(region_size)] for _ in range(region_size)]
        cnt = 0
        self.ptr_to_cell = {}
        self.ok_times = 0
        self.ok = 0
        self.max_ok_times = 0
        self.very_ok_times = 0
        self.a = None
        for i in self.columns:
            for j in i:
                for k in j.cells:
                    k.id = cnt
                    self.ptr_to_cell[k.id] = k
                    cnt += 1

    def get_active_cells(self):
        res = []
        for i in range(self.region_size):
            for j in range(self.region_size):
                for cell in self.columns[i][j].cells:
                    if cell.state == ACTIVE:
                        res.append(cell)
        return res

    @staticmethod
    def check_column_state(column, a):
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
        for i in range(self.region_size):
            for j in range(self.region_size):
                if not self.check_column_state(self.columns[i][j], a[i][j]):
                    return False
        return True

    def update_columns_state(self, a):
        # обновляем состояние колонок по поступившим данным от пространственного группировщика
        for i in range(self.region_size):
            for j in range(self.region_size):
                self.columns[i][j].state = ACTIVE if a[i][j] else PASSIVE

    @staticmethod
    def column_satisfies(column, active, prediction):
        # возвращает булевское значение, удовлетворяет ли колонка заданным параметрам,
        # если active или prediction является None - то колонка нам подходит точно
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
        # в зависимости от параметра возвращает нужные нам колонки

        return [self.columns[i][j] for i in range(self.region_size) for j in range(self.region_size) if
                self.column_satisfies(self.columns[i][j], active, prediction)]

    def step_forward(self, a):
        self.update_columns_state(a)

        # получаем активные на предыдущем шаге клетки
        active_cells = self.get_active_cells()

        for column in self.get_columns(active=True, prediction=True):
            # рассматриваем все колонки,которые были правильно предсказаны

            # первым делом проверим может в этой колонке есть клетка,которая очень давно не активировалсь, если она
            # есть тогда мы ее активируем

            for cell in column.cells:
                active_from_passive_time = False
                if cell.passive_time > PASSIVE_TIME_TO_ACTIVE_THRESHOLD:
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
                                    syn.change_permanence(DENDRITE_PERMANENCE_INC_DELTA)

        for column in self.get_columns(active=False, prediction=True):
            # рассматриваем все колонки,который были предсказаны неправильно

            # уменьшаем перманентность дендритов, которые привели к активации данной колонки
            for cell in column.cells:
                if cell.state == PREDICTION:
                    for dendrite in cell.dendrites:
                        if dendrite.active:
                            for syn in dendrite.synapses:
                                if syn.id_to in [a_cell.id for a_cell in active_cells]:
                                    syn.change_permanence(DENDRITE_PERMANENCE_DEC_DELTA)
            pass

        for column in self.get_columns(active=True, prediction=False):
            # рассматриваем все колонки, которые не были предсказаны

            # активируем каждую из клеток, также добалвяем новый дендрит или незначительно увеличиваем
            # перманентность у текущего если такой дендрит уже есть
            ok = False

            while not ok:
                for cell in column.cells:
                    if cell.new_state == PASSIVE and randrange(3) == 2:
                        cell.update_new_state(ACTIVE)
                        ok = True

                        new_den = Dendrite(active_cells)
                        for dendrite in cell.dendrites:
                            if dendrite.equal(new_den):
                                new_den = None
                                for synapse in dendrite.synapses:
                                    if synapse.id_to in [a_cell.id for a_cell in active_cells]:
                                        synapse.change_permanence(DENDRITE_PERMANENCE_INC_DELTA * 0.1)
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
                    dendrite.active = False

        # делаем предсказание
        for i in range(self.region_size):
            for j in range(self.region_size):
                current_column = self.columns[i][j]
                mx = 0
                dendrite_mx = None
                cell_for_update = current_column.cells[0]

                for current_cell in current_column.cells:
                    for dendrite in current_cell.dendrites:
                        q = 0
                        for syn in dendrite.synapses:
                            if self.ptr_to_cell[syn.id_to].new_state == ACTIVE and syn.permanence > SYNAPSE_THRESHOLD:
                                q += 1

                        if q > mx:
                            mx = q
                            cell_for_update = current_cell
                            dendrite_mx = dendrite

                if mx >= DENDRITE_ACTIVATE_THRESHOLD and cell_for_update.new_state == PASSIVE:
                    dendrite_mx.active = True
                    cell_for_update.update_new_state(PREDICTION)

        # проверяем предыдущее предсказание
        if self.prediction_was_ok(a):

            self.very_ok_times += 1
            self.max_ok_times = max(self.max_ok_times, self.very_ok_times)
            print('Предсказание было правильным.')
        else:
            self.very_ok_times = 0

        # досрочный выход если научились
        if self.max_ok_times > 50:
            exit(0)

        # применяем новое состояние клеток
        for i in range(self.region_size):
            for j in range(self.region_size):
                for cell in self.columns[i][j].cells:
                    cell.apply_new_state()

    def out_new_state(self):
        res = [["" for _ in range(self.region_size)] for _ in range(self.region_size)]
        for i in range(self.region_size):
            for j in range(self.region_size):
                cnt = 0
                for cell in self.columns[i][j].cells:
                    cnt += 1

                    if cell.new_state == PREDICTION:
                        res[i][j] += "P" + str(cnt)
                    if cell.new_state == ACTIVE and not cell.active_from_passive_time:
                        res[i][j] += "A" + str(cnt)
        for i in res:
            print(i)

    def out_prediction(self):
        # отображение информации
        res = [["" for _ in range(self.region_size)] for _ in range(self.region_size)]
        for i in range(self.region_size):
            for j in range(self.region_size):
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

        print("Правильно предсказано раз: ", self.very_ok_times)
        print("Максимально правильно предсказано раз: ", self.max_ok_times)
        for i in res:
            print(i)
        print()
