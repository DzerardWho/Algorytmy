import sys

sys.path.append(r".")
from datatypes.graph import Graph

if __name__ == '__main__':
    inputs = {'1': r".\inputs\input2.txt",
              '2': r".\inputs\input_cpm.txt"}
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

            paths = graph.dijkstra()

            def print_parent_name(idk):
                if paths[idk].previous_id != -1:
                    print_parent_name(paths[idk].previous_id)
                print(idk, end=' ')

            for p in paths:
                print('sciezka: ')
                print_parent_name(p.id)
                print('')
                print('waga:')

                print(p.min_weight)
                print('')
