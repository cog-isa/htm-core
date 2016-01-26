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

    # [19:49:34] Скрынник Алексей: т - номера дендритов
    # [19:49:37] Скрынник Алексей: текущие
    # [19:49:43] Скрынник Алексей: to - номера дендритов куда идем
    # [19:49:51] Скрынник Алексей: a - матрица дендритов текущих
    # [19:49:59] Скрынник Алексей: клетки, которые они активируют
    # [19:50:06] Скрынник Алексей: b - матрица дендритов куда идем
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

#only for linux
def draw_graph(file_name, res):
    import pygraphviz as pgv # на Windows не смогли собрать pygraphviz
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

def draw_graph(file_name, res):
    f = open(file_name, 'w')
    s = """
<!doctype html>
<html>
<head>
  <title>Network | Basic usage</title>

  <script type="text/javascript" src="vis.js"></script>
  <link href="/vis.css" rel="stylesheet" type="text/css" />

  <style type="text/css">
    #mynetwork {
      width: 600px;
      height: 400px;
      border: 1px solid lightgray;
    }
  </style>
</head>
<body>

<p>
  Create a simple network with some nodes and edges.
</p>

<div id="mynetwork"></div> """ + edges + """

<script type="text/javascript">
  // create an array with nodes
  var nodes = new vis.DataSet([
    {id: 1, label: 'Node 1'},
    {id: 2, label: 'Node 2'},
    {id: 3, label: 'Node 3'},
    {id: 4, label: 'Node 4'},
    {id: 5, label: 'Node 5'}
  ]);

  // create an array with edges
  var edges = new vis.DataSet([
    {from: 1, to: 3},
    {from: 1, to: 2},
    {from: 2, to: 4},
    {from: 2, to: 5}
  ]);

  // create a network
  var container = document.getElementById('mynetwork');
  var data = {
    nodes: nodes,
    edges: edges
  };
  var options = {};
  var network = new vis.Network(container, data, options);
</script>

</body>
</html>
"""
    f.write(s)
    f.close()

if __name__ == "__main__":
   # / draw_graph("out.html",[])
    main()