import sys

sys.path.append(".")
from datatypes.graph import Graph

if __name__ == '__main__':
    inputs = {'1': r".\inputs\MST_input_1.txt",
              '2': r".\inputs\MST_input_2.txt"}
    try:
        fp = inputs[sys.argv[1]]
    except (KeyError, IndexError):
        print('Please provide number 1 or 2 as a parameter to select input graph')
        pass
    else:
        graph = Graph()
        with open(fp, "r") as f:
            first_line = f.readline()
            nr_of_nodes = int(first_line.split(" ")[-1])
            graph.create_nodes(nr_of_nodes)
            for i in range(nr_of_nodes):
                row = f.readline()
                graph.parse_row_to_children(row, i)

            Graph.print_graph(graph, 'graph')

            print("MST - algorytm Prima")

            Graph.print_graph(graph.mst_prim(start_node=graph.nodes['T0']), 'Prim MST')

            print("MST - algorytm Kruskala")

            Graph.print_graph(graph.mst_kruskal(start_node=graph.nodes['T0']), 'Kruskal MST')
