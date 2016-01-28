def draw_graph(file_name, input_edges):
    from jsonpickle import json
    # переделаем edges для visjs
    # в mm лежит название вершины -> индекс, цифра

    mm = {}
    cnt = 0
    for i in input_edges:
        x, y = i
        if not x in mm:
            mm[x] = cnt
            cnt += 1
        if not y in mm:
            mm[y] = cnt
            cnt += 1
    # for i in mm:
    #     print(mm[i], i)
    # print()
    edges_str = "["
    for i in input_edges:
        x, y = i
        # print(mm[x], mm[y])  # ребро
        edges_str = edges_str + "[" + str(mm[x]) + "," + str(mm[y]) + "],"
    edges_str += "]"
    edges = edges_str
    nodes = json.encode(mm)
    s = """
    <!doctype html>
    <html>
    <head>
      <title>Network | Basic usage</title>

      <script type="text/javascript" src="vis.js"></script>
      <link href="vis.css" rel="stylesheet" type="text/css" />

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

    <div id="mynetwork"></div>

    <script type="text/javascript">
      var nodes_dict = """ + nodes + """
      var edges_list = """ + edges + """
     var nodes_visjs=[]
      // create an array with nodes
      for(n in nodes_dict)
        nodes_visjs.push({id:nodes_dict[n],label: n})

      var nodes = new vis.DataSet(nodes_visjs);

      var edges_visjs=[]
        console.log(edges_list)
      for(n in edges_list)
      {
        edges_visjs.push({from:edges_list[n][0],to: edges_list[n][1]})
        console.log(n)
      }

      // create an array with edges
      var edges = new vis.DataSet(edges_visjs);

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
    with open(file_name, 'w') as f:
        f.write(s)
        f.close()