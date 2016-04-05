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

    #поиск в глубину
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

    def __init__(self, pre_learning_steps):
        self.generator = MakeBubble(input_generators.TestSimpleSteps, 3, 1)
        tp_level_one_settings = TemporalSettings(region_size=3, column_size=4, initial_permanence=0.5,
                                                 dendrite_activate_threshold=2, dendrite_permanence_inc_delta=0.02,
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
            print(current.position_x_y)
            active_cells = set()
            for i in current.synapses:
                if i.permanence > tp_level_one_settings.synapse_threshold:
                    active_cells.add(i.id_to)
            if len(active_cells) < tp_level_one_settings.dendrite_activate_threshold:
                continue
            print(active_cells)
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
            print(s)

        print("----" * 9)

        self.tp_level_one.temporal_settings.dendrite_permanence_dec_delta = 0
        self.tp_level_one.temporal_settings.dendrite_permanence_inc_delta = 0
        self.tp_level_one.temporal_settings.initial_permanence = 0

    def move(self):
        self.tp_level_one.step_forward(self.generator.get_data())
        self.generator.move()
        cur = 0
        for i in self.dendrites:
            if i.active:
                cur |= 2 ** i.id
        f = False
        for i in self.chains:
            for j in i.a:
                if j.id == cur:
                    print("found:", cur)
                    f = True
        if not f:
            # print()
            print("not found")
            # print("----" * 5)
            # print("cur:", cur)
            # for i in self.chains:
            #     for j in i.a:
            #         print(j.id)
            # print("----" * 5)

def main():
    f = Foo(1000)
    for i in range(1000):
        f.move()


if __name__ == "__main__":
    main()