# only for linux
def draw_graph(file_name, res):
    import pygraphviz as pgv  # на Windows не смогли собрать pygraphviz

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