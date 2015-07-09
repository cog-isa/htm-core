from htm_column import Column
from htm_dendrite import Dendrite
from util import ACTIVE, PREDICTION, PASSIVE
from settings import *


class Region:
    def __init__(self, region_size, column_size):
        self.region_size = region_size
        self.columns = [[Column(column_size) for jj in range(region_size)] for ii in range(region_size)]
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
                for I in self.columns[i][j].cells:
                    if I.state == ACTIVE:
                        res.append(I)
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

    def step_forward(self, a):
        self.a = a
        active_cells = self.get_active_cells()
        self.ok = 0
        for i in range(self.region_size):
            for j in range(self.region_size):
                current_column = self.columns[i][j]

                for cell in current_column.cells:
                    active_den = None
                    for den in cell.dendrites:
                        if den.active:
                            active_den = den

                    if active_den:
                        active_den.active = False

                    if cell.state == PREDICTION and a[i][j]:
                        # Предсказание активности данной клетки было выполнено правильно

                        # Назначим следующее состояние клетки активным и увеличим перманентность синапсов связанных
                        # с активными клетками
                        cell.update_new_state(ACTIVE)

                        for syn in active_den.synapses:
                            if syn.id_to in [a_cell.id for a_cell in active_cells]:
                                syn.change_permanence(DENDRITE_PERMANENCE_INC_DELTA)

                    if cell.state == PREDICTION and not a[i][j]:
                        # Предсказание активности данной клетки было выполнено неправильно

                        for syn in active_den.synapses:
                            if syn.id_to in [a_cell.id for a_cell in active_cells]:
                                syn.change_permanence(DENDRITE_PERMANENCE_DEC_DELTA)
                                # syn.dec_permanence()
                                # syn.change_permanence(-0.07)
                                # syn.permanence -= 0.05
                        # Уменьшим силу дендрита
                        pass

                if not self.check_column_state(current_column, a[i][j]) and a[i][j]:
                    # если активация этой колонки не была предсказана

                    for I in current_column.cells:
                        I.update_new_state(ACTIVE)
                    # выберем клетку с максимальным временем простоя, назначим ее активной,
                    # присоединим к клетке дендрит из активных на прошлом шаге клеток
                    new_active_cell = current_column.cells[0]

                    for cell in current_column.cells:
                        if new_active_cell.passive_time < cell.passive_time:
                            new_active_cell = cell

                    # добавляем дендрит, подключенный к активным клеткам
                    new_active_cell.dendrites.append(Dendrite(active_cells))

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

                if mx and cell_for_update.new_state == PASSIVE:
                    dendrite_mx.active = True
                    cell_for_update.update_new_state(PREDICTION)

        # проверяем предыдущее предсказание
        if self.prediction_was_ok(a):
            self.very_ok_times += 1
            self.max_ok_times = max(self.max_ok_times, self.very_ok_times)
            print('Предсказание было правильным.')
        else:
            self.very_ok_times = 0

        # применяем новое состояние клеток
        for i in range(self.region_size):
            for j in range(self.region_size):
                for I in self.columns[i][j].cells:
                    I.apply_new_state()

    def out_prediction(self):
        # отображение информации
        res = [["" for _ in range(self.region_size)] for __ in range(self.region_size)]
        for i in range(self.region_size):
            for j in range(self.region_size):
                cnt = 0
                for cell in self.columns[i][j].cells:
                    cnt += 1
                    if cell.state == PREDICTION:
                        res[i][j] += "P" + str(cnt)
                    if cell.passive_time == 0:
                        res[i][j] += "A" + str(cnt)

        print("Правильно предсказано раз: ", self.very_ok_times)
        print("Максимально правильно предсказано раз: ", self.max_ok_times)
        for i in res:
            print(i)
        print()