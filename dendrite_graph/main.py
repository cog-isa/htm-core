import sys
from copy import deepcopy
import temporalPooler.htm__region as tp
from apps.settings import *
from dendrite_graph.draw_graph_pygraphviz import draw_graph as draw_graph_pg
from dendrite_graph.draw_graph_vis import draw_graph as draw_graph_vis
from gens import input_generators

used = {}

edges = []

dendrites = []
SIZE = 2
id_to_Cell = {}


def make_string(t):
    res = ""
    for i in range(0, 1000):
        if t & (2 ** i):
            res = res + ' ' + str(i)

    return res


def make_string_(a):
    res = ""
    for i in a:
        res += str(i) + "\n"
    return res


graph_edges = []


class DendritesNode:
    def __init__(self, id, dendrites):
        self.id = id
        self.dendrites = dendrites


def dfs(state, cnt=0):
    t = 0
    for i in state:
        t += 2 ** i.id
    if t == 0:
        return
    if t in used:
        return
    used[t] = True
    active_cells = set()
    for current in state:
        active_cells.add(current.id_to)
    ans = []
    for den in dendrites:
        q = 0
        for j in den.synapses:
            if j.id_to in active_cells and j.permanence > temporal_settings.SYNAPSE_THRESHOLD:
                q += 1
        if q >= temporal_settings.DENDRITE_ACTIVATE_THRESHOLD:
            ans.append(den)
    to = 0
    for i in ans:
        to += 2 ** i.id
    a = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    for i in state:
        for j in i.synapses:
            x, y = id_to_Cell[j.id_to].position_x_y
            a[x][y] = 1
            # a[i.position_x_y[0]][i.position_x_y[1]] = 1
    b = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    # for i in ans:
    # for j in i.synapses:
    # x, y = id_to_Cell[j.id_to].position_x_y
    # b[x][y] = 1
    for i in state:
        b[i.position_x_y[0]][i.position_x_y[1]] = 1

    # т - номера дендритов
    # текущие
    # to - номера дендритов куда идем
    # a - матрица дендритов текущих
    # клетки, которые они активируют
    # b - матрица дендритов куда идем
    edges.append([make_string(t) + "\n" + make_string_(a), make_string(to) + "\n" + make_string_(b)])
    graph_edges.append([DendritesNode(t, state), DendritesNode(to, ans)])
    print("**", t, to)
    # edges.append([make_string(t), make_string(to)])
    dfs(ans, cnt + 1)


graph_used_vertex = set()


def dfs_chain(t, chain):
    if t.id in graph_used_vertex:
        return
    graph_used_vertex.add(t.id)
    chain.append(t)
    edges_to_go = []
    for i in graph_edges:
        x, y = i
        if x.id == t.id:
            edges_to_go.append(i)
    if len(edges_to_go) == 1:
        _, to = edges_to_go[0]
        cnt = 0
        for i in graph_edges:
            x, y = i
            if y.id == to.id:
                cnt += 1
        if cnt == 1:
            dfs_chain(to, chain)


class Chain:
    def __init__(self, a, id):
        self.a = a
        self.id = id


def main():
    # немного двигаем SimpleSteps вперед, чтобы первончальная вершина вела в однозначное место
    tss1 = TestSimpleSteps(3)
    tss2 = TestSimpleSteps(3)

    # generator = CombineGenerator([tss1, tss2])
    # input_size = len(generator.empty)


    # ТО ЧТО НУЖНО ВЕРНУТь
    #generator = input_generators.Hierarchy2l(4)

    generator = MakeBubble(input_generators.H3, 2, 1)
    # generator = TestSimpleSteps(2)
    input_size = 2

    CELLS_IN_COLUMN = 4
    r_t = tp.Region(input_size, CELLS_IN_COLUMN)

    for i in range(input_settings.STEPS_NUMBER):
        data = generator.get_data()
        generator.out()
        r_t.step_forward(data)
        r_t.out_prediction()
        generator.move()

    dendrite_id_cnt = 0
    id_to_dendrite_map = {}

    for i, I in enumerate(r_t.columns):
        for j, J in enumerate(I):
            for cell, Cell in enumerate(r_t.columns[i][j].cells):
                id_to_Cell[Cell.id] = Cell
                Cell.position_x_y = [i, j]
                for dendrite, Dendrite in enumerate(Cell.dendrites):
                    dendrites.append(Dendrite)
                    Dendrite.id = dendrite_id_cnt
                    Dendrite.id_to = Cell.id
                    dendrite_id_cnt += 1
                    Dendrite.position_x_y = [i, j]
                    id_to_dendrite_map[Dendrite.id] = Dendrite
    for current in dendrites:
        print(current.position_x_yw)
        active_cells = set()
        for i in current.synapses:
            if i.permanence > temporal_settings.SYNAPSE_THRESHOLD:
                active_cells.add(i.id_to)
        if len(active_cells) < temporal_settings.DENDRITE_ACTIVATE_THRESHOLD:
            continue
        print(active_cells)
        ans = []
        for den in dendrites:
            q = 0
            for j in den.synapses:
                if j.id_to in active_cells and j.permanence > temporal_settings.SYNAPSE_THRESHOLD:
                    q += 1
            if q >= temporal_settings.DENDRITE_ACTIVATE_THRESHOLD:
                ans.append(den)
        print("---" * 5)
        for t in ans:
            print(t.position_x_y)
        dfs(ans)

    if sys.platform == "linux":
        draw_graph_pg("hello.png", edges)
    else:
        draw_graph_vis("out.html", edges)
    exit(0)
    #
    #
    # РАЗБИВАЕМ ГРАФ НА ЦЕПОЧКИ
    print("******" * 9)
    for i in graph_edges:
        x, y = i
        print(make_string(x.id), " -> ", make_string(y.id))

    print("----" * 4)
    # не работаем с циклами
    chains = []
    chain_cnt = 0
    while 1:
        # выбираем вершины, у которых нет входов, строим из них цепочку, помечаем дуги как рассмотренные
        edges_with_in_greater_zero = set()
        for i in graph_edges:
            x, y = i
            edges_with_in_greater_zero.add(y.id)
        t = None
        for i in graph_edges:
            x, y = i
            if x.id not in graph_used_vertex and x.id not in edges_with_in_greater_zero:
                t = x
                break
        if not t:
            break
        chain = []
        dfs_chain(t, chain)
        chains.append(Chain(chain, chain_cnt))
        chain_cnt += 1

    while 1:
        t = None
        for i in graph_edges:
            x, y = i
            if x.id not in graph_used_vertex and y.id not in graph_used_vertex:
                t = x
                break
        if not t:
            break
        chain = []
        dfs_chain(t, chain)
        chains.append(Chain(chain, chain_cnt))
        chain_cnt += 1

    for i in chains:
        s = ""
        for j in i.a:
            s += "[" + make_string(j.id) + "]"
        print(s)
    print("----" * 9)

    data_for_second_layer = []

    previous_chain = None
    for D in range(10000):
        data = generator.get_data()
        # generator.out()
        r_t.step_forward(data)
        # r_t.out_prediction()

        active_dens = []
        for i, I in enumerate(r_t.columns):
            # отключаем изменения
            global temporal_settings
            temporal_settings.DENDRITE_PERMANENCE_DEC_DELTA = 0
            temporal_settings.DENDRITE_PERMANENCE_INC_DELTA = 0
            # никаких пэссив тайм
            temporal_settings.PASSIVE_TIME_TO_ACTIVE_THRESHOLD = 100000000000
            for j, J in enumerate(I):
                for cell, Cell in enumerate(r_t.columns[i][j].cells):
                    id_to_Cell[Cell.id] = Cell
                    Cell.position_x_y = [i, j]
                    for dendrite, Dendrite in enumerate(Cell.dendrites):
                        if Dendrite.was_active:
                            active_dens.append(Dendrite)
            temporal_settings = TemporalSettings()

        t = 0
        for i in active_dens:
            t += 2 ** i.id
        # print(make_string(t))
        generator.move()
        current_chain = None

        for chain in chains:
            for i in chain.a:
                # print((i.id, t)
                if int(i.id) == int(t):
                    current_chain = chain
                    # print("ok")
        # print(current_chain)
        if current_chain is None:
            data_for_second_layer.append(previous_chain)
        previous_chain = current_chain
    data_for_second_layer = data_for_second_layer[1:]
    second_size = len(chains)
    empty_input = [[0 for _ in range(second_size)] for _ in range(second_size)]


    a = []

    for i in data_for_second_layer:
        input_data = deepcopy(empty_input)
        input_data[0][i.id] = 1
        a.append(deepcopy(input_data))
        # generator.out()

    temporal_settings.DENDRITE_ACTIVATE_THRESHOLD = 5

    CELLS_IN_COLUMN = 4
    generator = MakeBubble2(SequenceLoader, second_size, 2, a)
    second_r_t = tp.Region(len(generator.get_data()), CELLS_IN_COLUMN)
    for i in range(1000):
        data = generator.get_data()
        generator.move()
        second_r_t.step_forward(data)
        second_r_t.out_prediction()

class MakeBubble2:
    def __init__(self, inner_generator, square_size, scale, a):
        self.inner_generator = inner_generator(square_size, a)
        self.scale = scale
        self.square_size = square_size

    def move(self):
        self.inner_generator.move()

    def out(self):
        a = self.get_data()
        for i in a:
            print(i)
        print()

    def get_data(self):
        result = [[0 for _ in range(self.square_size * self.scale)] for _ in range(self.square_size * self.scale)]
        a = self.inner_generator.get_data()
        for i in range(self.square_size):
            for j in range(self.square_size):
                if a[i][j]:
                    for x in range(i * self.scale, (i + 1) * self.scale):
                        for y in range(j * self.scale, (j + 1) * self.scale):
                            result[x][y] = 1
        return result

if __name__ == "__main__":
    main()