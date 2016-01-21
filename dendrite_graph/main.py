import pygraphviz as pgv

import temporalPooler.htm__region as tp
from apps.settings import *
from hierarchy.CombinedGenerator import CombineGenerator

used = {}

edges = []

dendrites = []
SIZE = 6


def make_string(t):
    res = ""
    for i in range(0, 100):
        if t & (2 ** i):
            res = res + ' ' + str(i)

    return res


def make_string_(a):
    res = ""
    for i in a:
        res += str(i) + "\n"
    return res


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
        a[i.position_x_y[0]][i.position_x_y[1]] = 1
    b = [[0 for _ in range(SIZE)] for _ in range(SIZE)]
    for i in ans:
        b[i.position_x_y[0]][i.position_x_y[1]] = 1

    edges.append([make_string(t) + "\n" + make_string_(a), make_string(to) + "\n" + make_string_(b)])

    # edges.append([make_string(t), make_string(to)])
    dfs(ans, cnt + 1)


def main():
    # немного двигаем SimpleSteps вперед, чтобы первончальная вершина вела в однозначное место
    tss1 = TestSimpleSteps(3)
    # tss1.move()
    tss2 = TestSimpleSteps(3)
    # tss2.move()

    generator = CombineGenerator([tss1, tss2])
    input_size = len(generator.empty)
    CELLS_IN_COLUMN = 3
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
                for dendrite, Dendrite in enumerate(Cell.dendrites):
                    dendrites.append(Dendrite)
                    Dendrite.id = dendrite_id_cnt
                    Dendrite.id_to = Cell.id
                    dendrite_id_cnt += 1
                    Dendrite.position_x_y = [i, j]
                    id_to_dendrite_map[Dendrite.id] = Dendrite
    for current in dendrites:
        active_cells = set()
        for i in current.synapses:
            if i.permanence > temporal_settings.SYNAPSE_THRESHOLD:
                active_cells.add(i.id_to)
        if len(active_cells) < temporal_settings.DENDRITE_ACTIVATE_THRESHOLD:
            continue
        ans = []
        for den in dendrites:
            q = 0
            for j in den.synapses:
                if j.id_to in active_cells and j.permanence > temporal_settings.SYNAPSE_THRESHOLD:
                    q += 1
            if q >= temporal_settings.DENDRITE_ACTIVATE_THRESHOLD:
                ans.append(den)
        dfs(ans)
    draw_graph("hello.png", edges)


def draw_graph(file_name, res):
    g_out = pgv.AGraph(strict=False, directed=True)

    for i in res:
        try:
            g_out.add_edge(i[0], i[1], color='black')
            edge = g_out.get_edge(i[0], i[1])

            if i[3] == "active":
                edge.attr['color'] = 'green'

            edge.attr['label'] = i[2]
        except:
            pass
    g_out.layout(prog='dot')
    g_out.draw(file_name)


if __name__ == "__main__":
    main()