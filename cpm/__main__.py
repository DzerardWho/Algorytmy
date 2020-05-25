import sys

sys.path.append(r".")
from datatypes.graph import Graph

if __name__ == '__main__':
    inputs = {'1': r".\inputs\input1.txt",
              '2': r".\inputs\input2.txt",
              '3': r".\inputs\input3.txt",
              '4': r".\inputs\input_cpm.txt"}

    try:
        fp = inputs[sys.argv[1]]
    except (KeyError, IndexError):
        print('Please provide number 1 as a parameter to select input graph')
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
            proc_len = int(f.readline().split(" ")[-1])
            for i in range(proc_len):
                row = f.readline()
                # graph.parse_row_to_proc(row, i)
            # na razie używamy tylko P0, więc nie trzeba parsować
            f.readline()
            for i in range(nr_of_nodes):
                row = f.readline()
                graph.parse_row_to_times(row, i)
            f.readline()
            for i in range(nr_of_nodes):
                row = f.readline()
                # graph.parse_row_to_cost(row, i)
            no_of_comm = int(f.readline().split(" ")[-1])
            for i in range(no_of_comm):
                row = f.readline()
                graph.parse_row_to_comm(row, i)

            Graph.print_graph(graph, 'graph')
            print('szeregowanie listowe')
            print(graph.cpm())
