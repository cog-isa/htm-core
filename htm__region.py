from input_generators import TestSimpleSteps
from htm_cell import Cell
from htm_column import Column
from htm_dendrite import Dendrite
from htm_synapse import Synapse
from util import ACTIVE, PREDICTION, PASSIVE


class Region:
    def __init__(self, region_size, column_size):
        self.region_size = region_size
        self.columns = [[Column(column_size) for jj in range(region_size)] for ii in range(region_size)]
        self.initial_permanence = 0.5
        cnt = 0
        self.ptr_to_cell = {}
        self.ok_times = 0
        self.ok = 0
        self.max_ok_times = 0
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
                    if I.state_mem:

                        if I.state == ACTIVE:
                            res.append(I)
        return res

    def step_forward(self, a):
        self.a = a
        active_cells = self.get_active_cells()
        self.ok = 0
        for i in range(self.region_size):
            for j in range(self.region_size):
                skill = False

                for cell in self.columns[i][j].cells:
                    active_den = None
                    for den in cell.dendrites:
                        if den.active:
                            active_den = den

                    if active_den:
                        active_den.active = False

                    if cell.state == PREDICTION and a[i][j]:
                        # TODO Корректировать вес только синапсов активных клеток
                        self.ok_times += 1

                        self.ok = 1
                        # Увеличим силу дендрита
                        cell.update_new_state(ACTIVE)

                        skill = True
                        for syn in active_den.synapses:
                            syn.change_permanence(0.01)
                            # syn.permanence += 0.01


                    if cell.state == PREDICTION and not a[i][j]:
                        self.ok = 0
                        for syn in active_den.synapses:
                            syn.change_permanence(-0.05)
                            # syn.permanence -= 0.05
                        # Уменьшим силу дендрита
                        pass


                if skill:
                    continue


                # если активация этой колонки не была предсказана
                if a[i][j]:
                    for I in self.columns[i][j].cells:
                        I.update_new_state(ACTIVE)
                    # выберем клетку с максимальным временем простоя, назначим ее активной,
                    # присоединим к клетке дендрит из активных на прошлом шаге клеток
                    ptr = 0
                    for I in range(len(self.columns[i][j].cells)):
                        if self.columns[i][j].cells[ptr].passive_time < self.columns[i][j].cells[I].passive_time:
                            ptr = I
                    new_dendrite = Dendrite()

                    for k in active_cells:
                        new_dendrite.add_synapse(Synapse(k.id, self.initial_permanence))

                    self.columns[i][j].cells[ptr].dendrites.append(new_dendrite)




        we_make_prediction = False

        if not self.ok:
            self.ok_times = 0
        else:
             print('GOOD_JOB')
        self.max_ok_times = max(self.max_ok_times, self.ok_times)

        for i in range(self.region_size):
            for j in range(self.region_size):

                mx = 0
                dendrite_mx = None
                cell_for_update = self.columns[i][j].cells[0]

                for current_cell in self.columns[i][j].cells:
                    threshold = 0.35

                    for dendrite in current_cell.dendrites:
                        q = 0
                        for syn in dendrite.synapses:
                            if self.ptr_to_cell[syn.id_to].new_state == ACTIVE and syn.permanence > threshold:
                                q += 1

                        if q > mx:
                            mx = q

                            cell_for_update = current_cell
                            dendrite_mx = dendrite
                            # print("active ", cell_for_update.id, " predicted_by: ", self.ptr_to_cell[dendrite_mx.synapses[0].id_to].id, dendrite_mx)

                if mx and cell_for_update.new_state == PASSIVE:
                    dendrite_mx.active = True
                    cell_for_update.update_new_state(PREDICTION)
                    we_make_prediction = True


        for i in range(self.region_size):
            for j in range(self.region_size):
                for I in self.columns[i][j].cells:
                    I.apply_new_state()

    def out_prediction(self):
        res = [["" for _ in range(self.region_size)] for __ in range(self.region_size)]
        for i in range(self.region_size):
            for j in range(self.region_size):
                # if self.a[i][j]:
                #     res[i][j] += 'A'
                cnt = 0
                for cell in self.columns[i][j].cells:
                    cnt += 1
                    if cell.state == PREDICTION:
                        res[i][j] += "P" + str(cnt)
                    if cell.passive_time == 0:
                        res[i][j] += "A" + str(cnt)
        print("Правильно предсказано раз: ", self.ok_times)
        print("Максимально правильно предсказано раз: ", self.max_ok_times)
        for i in res:
            print(i)
        print()