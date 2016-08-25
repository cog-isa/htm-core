from dendrite_graph.draw_graph_pygraphviz import draw_graph
from main_image_drawer import draw_image
import sys

from apps.settings import TemporalSettings
from gens.make_bubble import MakeBubble
from temporalPooler.htm__region import Region
from copy import deepcopy
import os

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
        self.edges2.append(deepcopy(a))
        self.edges2.append(deepcopy(b))
        self.graph_edges.append([self.DendritesNode(t, state), self.DendritesNode(to, ans)])
        # print("**", t, to)
        self.dfs(ans, cnt + 1)

    def __init__(self, tp, agent_finish):
        self.tp_level_one = tp
        tp_level_one_settings = tp.temporal_settings
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

        self.graph_edges = []
        index = 0
        os.system('rm -rf pic/')
        if not os.path.exists('pic/'):
            os.makedirs('pic/')
        for current in self.dendrites:
            self.edges = []
            self.edges2 = []
            # print("id" + str(current.id) + ":" + str(current.position_x_y))
            active_cells = set()
            for i in current.synapses:
                if i.permanence > tp_level_one_settings.synapse_threshold:
                    active_cells.add(i.id_to)
            if len(active_cells) < tp_level_one_settings.dendrite_activate_threshold:
                continue
            # print("acells:" + str(active_cells))
            ans = []
            for den in self.dendrites:
                q = 0
                for j in den.synapses:
                    if j.id_to in active_cells and j.permanence > tp_level_one_settings.synapse_threshold:
                        q += 1
                if q >= tp_level_one_settings.dendrite_activate_threshold:
                    ans.append(den)
            # print("---" * 5)
            # for t in ans:
            # print(t.position_x_y)
            self.dfs(ans)
            # if sys.platform == "linux":

            size = self.tp_level_one.temporal_settings.region_size
            p = [[0 for _ in range(size)] for _ in range(size)]
            for i in range(len(self.edges2)):
                for x in range(len(self.edges2[i])):
                    for y in range(len(self.edges2[i][x])):
                        if self.edges2[i][x][y]:
                            p[x][y] = 1
            # if p[7][4]:
            if len(self.edges) > 0:
                p[agent_finish[0]][agent_finish[1]] = 2

                # p[agent_finish[0]][agent_finish[1]] = 3
                draw_image("pic/image" + str(index), p)

            # draw_graph("pic/refactoring" + str(index), [(self.make_string_(p), "1")])
            index += 1
            # draw_graph("refactoring", self.edges)
