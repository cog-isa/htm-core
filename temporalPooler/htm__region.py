from htm_column import Column
from htm_dendrite import Dendrite
from util import ACTIVE, PREDICTION, PASSIVE
from settings import *
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
        self.t = 0
        self.cell_count = 0
        self.a = a
        active_cells = self.get_active_cells()
        self.ok = 0
        for i in range(self.region_size):
            for j in range(self.region_size):
                current_column = self.columns[i][j]

                ololo = False


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

                        ololo = True


                    if cell.state == PREDICTION and not a[i][j]:
                        # Предсказание активности данной клетки было выполнено неправильно

                        for syn in active_den.synapses:
                            if syn.id_to in [a_cell.id for a_cell in active_cells]:
                                syn.change_permanence(DENDRITE_PERMANENCE_DEC_DELTA)
                                # ОЧЕНЬ ВАЖНЫЙ МОМЕНт
                                # нам нужно понять,что активность какой-то клетки привела к неправильному предсказанию
                                # такую клетку стоит заменить в колонке
                                # если клетка активность клетки часто приводит к неправильным предсказаниям
                                # увеличим порог ошибки этой клетки,для последующего перестроения структуры связей
                                self.ptr_to_cell[syn.id_to].passive_time = -100
                                self.ptr_to_cell[syn.id_to].error_impulse += 1


                # hard_learning = False
                if a[i][j] and (not self.check_column_state(current_column, a[i][j])):

                    # если активация этой колонки не была предсказана

                    # cnt = 0
                    # for cell in current_column.cells:
                    #     print("A%d " % cnt, cell.passive_time)
                    #     cnt += 1

                    new_active_cell = current_column.cells[0]
                    # [randrange(0, len(current_column.cells))]
                    # print('A1 passive time: ', current_column.cells[0].passive_time)
                    cnt = 0
                    for cell in current_column.cells:
                        if new_active_cell.passive_time < cell.passive_time:
                            new_active_cell = cell
                            print('active_cnt :', cnt, new_active_cell.passive_time)
                        cnt += 1
                    new_dendrite = Dendrite(active_cells)
                    for den in new_active_cell.dendrites:
                        if den.equal(new_dendrite):
                            new_dendrite = None
                            for syn in den.synapses:
                                syn.change_permanence(DENDRITE_PERMANENCE_INC_DELTA)
                            break

                    # for den in new_active_cell.dendrites:

                    # присоединим к клетке дендрит из активных на прошлом шаге клеток
                    # но прежде проверим может такой дендрит уже существует, тогда просто увеличим силу его синапсов
                    # добавляем дендрит, подключенный к активным клеткам
                    # new_active_cell.update_new_state(ACTIVE)

                    if new_dendrite:
                        new_active_cell.dendrites.append(new_dendrite)


                    # ВАЖНО
                    ok = False
                    while not ok:
                        for I in current_column.cells:
                            if randrange(3) == 2:
                                I.update_new_state(ACTIVE)
                                ok = True
                    # выберем клетку с максимальным временем простоя, назначим ее активной,
                if ololo:
                    for cell1 in current_column.cells:
                        if cell1.passive_time > PASSIVE_TIME_TO_ACTIVE_THRESHOLD and cell1.new_state != ACTIVE:
                            for cell in current_column.cells:
                                cell.new_state = PASSIVE

                            new_active_cell = current_column.cells[0]

                            for cell in current_column.cells:
                                if new_active_cell.passive_time < cell.passive_time:
                                    new_active_cell = cell
                            new_active_cell.update_new_state(ACTIVE)
                            cell1.ololo = True
                            for other_cell in current_column.cells:
                                if other_cell != cell1:
                                    if other_cell.new_state == ACTIVE:
                                        other_cell.new_state = PASSIVE
                            break

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
                # if mx:
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
    def out_prediction_to_file(self, f):
        for i in range(self.region_size):
            for j in range(self.region_size):
                current_column = self.columns[i][j]
                active = False
                for cell in current_column.cells:
                    if cell.state == PREDICTION:
                        active = True
                if active:
                    f.write("1 ")
                else:
                    f.write("0 ")
            f.write("\n")
        f.write("\n")

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
                    if cell.passive_time == 0 and not cell.ololo:
                        res[i][j] += "A" + str(cnt)
                    # клетка активировалсь из-за долгого простоя
                    if cell.ololo:
                        res[i][j] += "O" + str(cnt)
                        cell.ololo = False

        # print("Процент предыдущего правильного предсказания: ", self.t * 1.0 / self.cell_count)
        print("Правильно предсказано раз: ", self.very_ok_times)
        print("Максимально правильно предсказано раз: ", self.max_ok_times)
        for i in res:
            print(i)
        print()