import sys

from apps.settings import TemporalSettings
from gens.make_bubble import MakeBubble
from gens import input_generators
from temporalPooler.htm__region import Region


if sys.platform == "linux":
    from dendrite_graph.draw_graph_pygraphviz import draw_graph as draw_graph_pg
else:
    from dendrite_graph.draw_graph_vis import draw_graph as draw_graph_vis


class Foo:
    class Chain:
        def __init__(self, a, id_):
            self.a = a
            self.id = id_

    class DendritesNode:
        def __init__(self, id_, dendrites):
            self.id = id_
            self.dendrites = dendrites

    @staticmethod
    def make_string(t):
        res = ""
        for i in range(0, 1000):
            if t & (2 ** i):
                res = res + ' ' + str(i)

        return res

    @staticmethod
    def make_string_(a):
        res = ""
        for i in a:
            res += str(i) + "\n"
        return res

    def dfs_chain(self, t, chain):
        if t.id in self.graph_used_vertex:
            return
        self.graph_used_vertex.add(t.id)
        chain.append(t)
        edges_to_go = []
        for i in self.graph_edges:
            x, y = i
            if x.id == t.id:
                edges_to_go.append(i)
        if len(edges_to_go) == 1:
            _, to = edges_to_go[0]
            cnt = 0
            for i in self.graph_edges:
                x, y = i
                if y.id == to.id:
                    cnt += 1
            if cnt == 1:
                self.dfs_chain(to, chain)

    # поиск в глубину
    def dfs(self, state, cnt=0):
        size = self.tp_level_one.temporal_settings.region_size

        t = 0
        for i in state:
            t |= 2 ** i.id
        if t == 0:
            return
        if t in self.used:
            return
        self.used[t] = True
        active_cells = set()
        for current in state:
            active_cells.add(current.id_to)
        ans = []
        for den in self.dendrites:
            q = 0
            for j in den.synapses:
                if j.id_to in active_cells and j.permanence > self.tp_level_one.temporal_settings.synapse_threshold:
                    q += 1
            if q >= self.tp_level_one.temporal_settings.dendrite_activate_threshold:
                ans.append(den)
        to = 0
        for i in ans:
            to |= 2 ** i.id
        a = [[0 for _ in range(size)] for _ in range(size)]
        for i in state:
            for j in i.synapses:
                x, y = self.id_to_Cell[j.id_to].position_x_y
                a[x][y] = 1
        b = [[0 for _ in range(size)] for _ in range(size)]
        for i in state:
            b[i.position_x_y[0]][i.position_x_y[1]] = 1

        self.edges.append(
            [self.make_string(t) + "\n" + self.make_string_(a), self.make_string(to) + "\n" + self.make_string_(b)])
        self.graph_edges.append([self.DendritesNode(t, state), self.DendritesNode(to, ans)])
        print("**", t, to)
        self.dfs(ans, cnt + 1)

    def __init__(self, pre_learning_steps, input_generator, region_size):
        self.generator = input_generator
        tp_level_one_settings = TemporalSettings(region_size=region_size, column_size=2, initial_permanence=0.5,
                                                 dendrite_activate_threshold=1, dendrite_permanence_inc_delta=0.02,
                                                 dendrite_permanence_dec_delta=-0.1,
                                                 passive_time_to_active_threshold=1000,
                                                 synapse_threshold=0.45)
        self.tp_level_one = Region(tp_level_one_settings)
        for i in range(pre_learning_steps):
            self.tp_level_one.step_forward(self.generator.get_data())
            self.tp_level_one.out_prediction()
            self.generator.move()

        # замораживаем состояние региона
        tp_level_one_settings.dendrite_permanence_dec_delta = tp_level_one_settings.dendrite_permanence_inc_delta = 0.0
        tp_level_one_settings.passive_time_to_active_threshold = 10000000000000000000

        dendrite_id_cnt = 0
        self.id_to_dendrite_map = {}
        self.id_to_Cell = {}
        self.dendrites = []

        for i, I in enumerate(self.tp_level_one.columns):
            for j, J in enumerate(I):
                for cell, Cell in enumerate(self.tp_level_one.columns[i][j].cells):
                    self.id_to_Cell[Cell.id] = Cell
                    Cell.position_x_y = [i, j]
                    for dendrite, Dendrite in enumerate(Cell.dendrites):
                        self.dendrites.append(Dendrite)
                        Dendrite.id = dendrite_id_cnt
                        Dendrite.id_to = Cell.id
                        dendrite_id_cnt += 1
                        Dendrite.position_x_y = [i, j]
                        self.id_to_dendrite_map[Dendrite.id] = Dendrite

        self.used = {}
        self.edges = []
        self.graph_edges = []

        for current in self.dendrites:
            print("id" + str(current.id) + ":" + str(current.position_x_y))
            active_cells = set()
            for i in current.synapses:
                if i.permanence > tp_level_one_settings.synapse_threshold:
                    active_cells.add(i.id_to)
            if len(active_cells) < tp_level_one_settings.dendrite_activate_threshold:
                continue
            print("acells:" + str(active_cells))
            ans = []
            for den in self.dendrites:
                q = 0
                for j in den.synapses:
                    if j.id_to in active_cells and j.permanence > tp_level_one_settings.synapse_threshold:
                        q += 1
                if q >= tp_level_one_settings.dendrite_activate_threshold:
                    ans.append(den)
            print("---" * 5)
            for t in ans:
                print(t.position_x_y)
            self.dfs(ans)
        if sys.platform == "linux":
            draw_graph_pg("refactoring", self.edges)
        else:
            draw_graph_vis("out.html", self.edges)

        self.graph_used_vertex = set()
        self.chains = []
        chain_cnt = 0
        while 1:
            edges_with_in_greater_zero = set()
            for i in self.graph_edges:
                x, y = i
                edges_with_in_greater_zero.add(y.id)
            t = None
            for i in self.graph_edges:
                x, y = i
                if x.id not in self.graph_used_vertex and x.id not in edges_with_in_greater_zero:
                    t = x
                    break
            if not t:
                break
            chain = []
            self.dfs_chain(t, chain)
            self.chains.append(self.Chain(chain, chain_cnt))
            chain_cnt += 1

        while 1:
            t = None
            for i in self.graph_edges:
                x, y = i
                if x.id not in self.graph_used_vertex and y.id not in self.graph_used_vertex:
                    t = x
                    break
            if not t:
                break
            chain = []
            self.dfs_chain(t, chain)
            self.chains.append(self.Chain(chain, chain_cnt))
            chain_cnt += 1

        for i in self.chains:
            s = ""
            for j in i.a:
                s += "[" + self.make_string(j.id) + "]"
            print("chain" + str(s))

        print("----" * 9)

        self.tp_level_one.temporal_settings.dendrite_permanence_dec_delta = 0
        self.tp_level_one.temporal_settings.dendrite_permanence_inc_delta = 0
        self.tp_level_one.temporal_settings.initial_permanence = 0
        self.column_dendrite_dependencies = {}

        for i, I in enumerate(self.tp_level_one.columns):
            for j, J in enumerate(I):
                for cell, Cell in enumerate(self.tp_level_one.columns[i][j].cells):
                    for dendrite_left, DendriteLeft in enumerate(Cell.dendrites):
                        if DendriteLeft.id not in self.column_dendrite_dependencies.keys():
                            self.column_dendrite_dependencies[DendriteLeft.id] = set()
                        for cellRight, CellRight in enumerate(self.tp_level_one.columns[i][j].cells):
                            for dendrite_right, DendriteRight in enumerate(CellRight.dendrites):
                                if DendriteLeft.id != DendriteRight.id:
                                    self.column_dendrite_dependencies[DendriteLeft.id].add(DendriteRight.id)

        self.my_states = {}

        # пока задается жестко, предполагается, что данная велечина, потом будет приходить как параметр
        self.output_size = 15

    def move(self):
        self.tp_level_one.step_forward(self.generator.get_data())
        self.generator.move()
        cur = 0
        for i in self.dendrites:
            if i.active:
                cur |= 2 ** i.id
                # print(2 ** i.id)

        # создаем битовый вектор в котором хранится информация о том, какие дендриты не могут быть в данной комбинации
        reverse_bit_vector = 0

        for i in self.dendrites:
            if i.active:
                # print(self.column_dendrite_dependencies.keys())
                # print(i.id)
                for j, J in enumerate(self.column_dendrite_dependencies[i.id]):
                    reverse_bit_vector |= 2 ** J
        f = False
        if cur & reverse_bit_vector:
            raise KeyError("Конфликт текущего дендрита и активируемого", cur, reverse_bit_vector,
                           cur & reverse_bit_vector, self.column_dendrite_dependencies[cur & reverse_bit_vector])
        for i in self.chains:
            for j in i.a:
                state_id = j.id
                state_id |= reverse_bit_vector
                state_id ^= reverse_bit_vector
                if state_id == cur:
                    my_state = cur
                    if my_state not in self.my_states:
                        self.my_states[my_state] = len(self.my_states)
                    # проверяем умещается ли у нас выход для второго слоя
                    assert (len(self.my_states) < self.output_size ** 2)
                    print("found:", cur)
                    f = True
                    return encode(self.my_states[my_state], self.output_size)

        if not f:
            # print()
            print("not found", cur)
            # print("----" * 5)
            # print("cur:", cur)
            # for i in self.chains:
            # for j in i.a:
            # print(j.id)
            # print("----" * 5)


def encode(id_, size):
    assert (id_ < size ** 2)
    a = [[0 for _ in range(size)] for _ in range(size)]
    a[id_ // size][id_ % size] = 1
    return a


input_robot = [[46, 12],
               [45, 12],
               [44, 13],
               [45, 11],
               [44, 13],
               [45, 11],
               [44, 13],
               [44, 11],
               [44, 13],
               [44, 11],
               [44, 13],
               [44, 11],
               [43, 13],
               [44, 11],
               [43, 13],
               [44, 11],
               [43, 13],
               [43, 11],
               [43, 13],
               [43, 11],
               [43, 13],
               [43, 11],
               [42, 14],
               [43, 10],
               [42, 14],
               [43, 10],
               [42, 14],
               [43, 10],
               [42, 14],
               [42, 10],
               [42, 14],
               [42, 10],
               [42, 14],
               [42, 10],
               [41, 14],
               [42, 10],
               [41, 14],
               [42, 10],
               [41, 14],
               [41, 10],
               [41, 14],
               [41, 9],
               [41, 14],
               [41, 9],
               [41, 14],
               [41, 9],
               [40, 15],
               [41, 9],
               [40, 15],
               [40, 9],
               [40, 15],
               [40, 9],
               [40, 15],
               [40, 9],
               [40, 15],
               [40, 9],
               [40, 15],
               [40, 8],
               [40, 15],
               [39, 8],
               [39, 15],
               [39, 8],
               [39, 15],
               [39, 8],
               [39, 15],
               [39, 8],
               [39, 15],
               [38, 8],
               [39, 15],
               [38, 8],
               [39, 15],
               [38, 8],
               [39, 16],
               [38, 7],
               [38, 16],
               [37, 7],
               [38, 16],
               [37, 7],
               [38, 16],
               [37, 7],
               [38, 16],
               [37, 7],
               [38, 16],
               [36, 7],
               [38, 16],
               [36, 7],
               [38, 16],
               [36, 6],
               [37, 16],
               [36, 6],
               [37, 16],
               [35, 6],
               [37, 16],
               [35, 6],
               [37, 16],
               [35, 6],
               [37, 16],
               [35, 6],
               [37, 16],
               [34, 5],
               [37, 16],
               [34, 5],
               [37, 17],
               [34, 5],
               [36, 17],
               [33, 5],
               [36, 17],
               [33, 6],
               [36, 17],
               [33, 7],
               [36, 17],
               [33, 8],
               [36, 17],
               [33, 9],
               [36, 17],
               [34, 10],
               [36, 17],
               [34, 11],
               [36, 17],
               [34, 11],
               [35, 17],
               [34, 12],
               [35, 17],
               [34, 13],
               [35, 17],
               [34, 13],
               [35, 17],
               [34, 14],
               [35, 17],
               [34, 15],
               [35, 17],
               [34, 15],
               [35, 17],
               [34, 16],
               [35, 18],
               [34, 16],
               [34, 18],
               [34, 16],
               [34, 18],
               [34, 17],
               [34, 18],
               [34, 17],
               [34, 18],
               [26, 11],
               [25, 10],
               [25, 11],
               [23, 8],
               [25, 11],
               [20, 5],
               [25, 12],
               [19, 4],
               [25, 12],
               [19, 5],
               [25, 12],
               [19, 5],
               [25, 12],
               [18, 5],
               [24, 12],
               [18, 5],
               [24, 12],
               [18, 5],
               [24, 13],
               [18, 6],
               [24, 13],
               [17, 6],
               [24, 13],
               [17, 6],
               [24, 13],
               [17, 6],
               [24, 13],
               [17, 7],
               [23, 14],
               [17, 7],
               [23, 14],
               [16, 7],
               [23, 14],
               [16, 7],
               [23, 14],
               [16, 7],
               [23, 14],
               [16, 8],
               [23, 14],
               [15, 8],
               [22, 15],
               [15, 8],
               [22, 15],
               [15, 8],
               [22, 15],
               [15, 9],
               [22, 15],
               [14, 9],
               [22, 15],
               [14, 9],
               [22, 15],
               [14, 9],
               [21, 16],
               [14, 9],
               [21, 16],
               [13, 10],
               [21, 16],
               [13, 10],
               [21, 16],
               [13, 10],
               [21, 16],
               [12, 10],
               [21, 17],
               [12, 11],
               [21, 17],
               [12, 11],
               [20, 17],
               [12, 11],
               [20, 17],
               [14, 13],
               [20, 17],
               [15, 14],
               [20, 17],
               [16, 15],
               [20, 18],
               [17, 16],
               [20, 18],
               [18, 17],
               [19, 18],
               [11, 19],
               [11, 20],
               [12, 20],
               [10, 20],
               [12, 20],
               [10, 20],
               [12, 21],
               [9, 20],
               [12, 21],
               [9, 20],
               [12, 21],
               [8, 21],
               [13, 22],
               [8, 21],
               [13, 22],
               [7, 21],
               [13, 23],
               [7, 21],
               [13, 23],
               [6, 21],
               [13, 23],
               [6, 22],
               [14, 24],
               [5, 22],
               [14, 24],
               [5, 22],
               [14, 24],
               [14, 25],
               [15, 25],
               [15, 26],
               [15, 27],
               [14, 27],
               [14, 28],
               [13, 28],
               [12, 29],
               [11, 29],
               [11, 30],
               [10, 30],
               [9, 30]]


def main():
    b = []
    for i in input_robot:
        a = [[0 for _ in range(50)] for _ in range(50)]
        a[i[0]][i[1]] = 1
        b.append(a)
    input_maker = input_generators.SequenceLoader(50, b)
    f = Foo(1000, input_maker, 50)

    for_second_layer = []
    for i in range(1000):
        output = f.move()
        if output:
            for j in output:
                print(j)
            print()

            for_second_layer.append(output)

    f2 = Foo(600, input_generators.SequenceLoader(15, for_second_layer), 15)


if __name__ == "__main__":
    main()
