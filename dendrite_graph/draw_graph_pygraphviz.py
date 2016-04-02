import pygraphviz as pgv


def draw_graph(file_name, res):
    """
    нарисовать граф, сохранить картинку в директории
    :param file_name: имя файла
    :param res: список дуг, если задан и вес ребра, то он тоже будет нарисован
    :return:
    """
    g_out = pgv.AGraph(strict=False, directed=True)
    g_out.graph_attr['width'] = '123.0'
    g_out.graph_attr['height'] = '123.0'
    for i in res:
        # try:
            g_out.add_edge(i[0], i[1], color='black')
            edge = g_out.get_edge(i[0], i[1])

            if len(i) > 2:
                edge.attr['label'] = i[2]
            # edge.attr['color'] = 'green'
        # except:
        #     pass
    # g_out.layout(prog='neato')
    # g_out.layout(prog='circo')
    g_out.layout(prog='dot')
    g_out.draw(file_name + ".png")
    # g_out.draw(file_name + ".ps")


def main():
    draw_graph("test", [("A", "B", 'test'), (2, 3)])


if __name__ == "__main__":
    main()