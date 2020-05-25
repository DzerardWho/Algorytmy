import sys

sys.path.append(".")
from datatypes.graph import Graph



if __name__ == '__main__':
    inputs = {'1': r".\inputs\input1.txt",
              '2': r".\inputs\input2.txt",
              '3': r".\inputs\input3.txt"}
    try:
        fp = inputs[sys.argv[1]]
    except (KeyError, IndexError):
        print('Please provide number 1 2 or 3 as a parameter to select input graph')
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

            Graph.print_graph(graph.get_spanning_tree(), 'spanning tree')
