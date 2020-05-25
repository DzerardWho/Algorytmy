import sys

sys.path.append(".")
from datatypes.node import Node
from datatypes.graph import Graph
import random
import copy

if __name__ == '__main__':
    fps = [r".\inputs\input_subtree1.txt", r".\inputs\input_subtree2.txt"]

    trees = []

    for fp in fps:
        graph = Graph()
        with open(fp, "r") as f:
            first_line = f.readline()
            nr_of_nodes = int(first_line.split(" ")[-1])
            graph.create_nodes(nr_of_nodes)
            for i in range(nr_of_nodes):
                row = f.readline()
                graph.parse_row_to_children(row, i)
            trees.append(graph.get_spanning_tree())

    random.seed()

    Graph.print_graph(trees[0], "Pierwszy graf")
    Graph.print_graph(trees[1], "Drugi graf")

    r1 = random.randint(1, len(trees[0].nodes) - 1)
    r2 = random.randint(1, len(trees[1].nodes) - 1)

    print(
        f"Z pierwszego grafu usuwam poddrzewo zaczynajace się w wierzcholku T{r1} i w jego miejsce\n dodaję poddrzewo z "
        f"drugiego grafu zaczynające się w punkcie T{r2} i wszystkie 'doklejone' wierzchołki w nazwie zawierają "
        f"literę P, zamiast T")

    graphA = copy.deepcopy(trees[0])
    node_to_remove = f'T{r1}'
    parent = graphA.nodes[node_to_remove].parents[0]
    nodes_to_remove = graphA.bfs(graphA.nodes[node_to_remove])
    for node_tr in nodes_to_remove[::-1]:
        graphA.remove_connection(graphA.edges[f'{node_tr.parents[0].name}_{node_tr.name}'])
        del graphA.nodes[node_tr.name]

    nodes_to_append = trees[1].bfs(trees[1].nodes[f'T{r2}'])

    for node in nodes_to_append:
        graphA.add_node(Node(f'P{node.name[1:]}'))
    for node in nodes_to_append:
        for child in node.children:
            graphA.connect_nodes(graphA.nodes[f'P{node.name[1:]}'], graphA.nodes[f'P{child.name[1:]}'], 0)
            graphA.nodes[f'P{node.name[1:]}'].add_child(graphA.nodes[f'P{child.name[1:]}'])
            graphA.nodes[f'P{child.name[1:]}'].add_parent(graphA.nodes[f'P{node.name[1:]}'])

    graphA.connect_nodes(parent, graphA.nodes[f'P{r2}'], 0)
    parent.add_child(graphA.nodes[f'P{r2}'])
    graphA.nodes[f'P{r2}'].add_parent(parent)

    Graph.print_graph(graphA, "Połączony graf")
