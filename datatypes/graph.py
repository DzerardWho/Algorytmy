import copy
import re
from dataclasses import dataclass

from datatypes.egde import Edge
from datatypes.node import Node


class Graph:
    nodes: dict
    edges: dict
    proc = None
    times = None
    const = None
    comm = None

    def __init__(self):
        self.comms = []
        self.nodes = {}
        self.edges = {}

    def add_node(self, node):
        self.nodes[node.name] = node

    def add_edge(self, edge):
        self.edges[edge.name] = edge

    def remove_edge(self, edge):
        del self.edges[edge.name]

    def create_nodes(self, number_of_nodes):
        for i in range(number_of_nodes):
            new_node = Node('T' + str(i))
            self.add_node(new_node)

    @staticmethod
    def parse_edge_data_to_node_name_and_weight(data: str):
        row_data = re.split("[()]", data)
        return row_data[0], row_data[1]

    def connect_nodes(self, node_from: Node, node_to: Node, weight):
        new_edge = Edge(f'{node_from.name}_{node_to.name}', int(weight), node_from, node_to)
        self.add_edge(new_edge)

    def remove_connection(self, edge):
        node_from = edge.from_node
        node_to = edge.to_node
        node_to.remove_parent(node_from)
        node_from.remove_child(node_to)
        self.remove_edge(edge)

    def parse_row_to_children(self, row, id):
        row_data = row.split(" ")
        name = row_data[0]
        nr_of_children = row_data[1]
        assert int(nr_of_children) == len(row_data[2:])
        for item in row_data[2:]:
            name_node_to, weight = self.parse_edge_data_to_node_name_and_weight(item)
            self.connect_nodes(self.nodes[f'T{id}'], self.nodes[f'T{name_node_to}'], weight)
            self.nodes['T' + str(id)].add_child(self.nodes[f'T{name_node_to}'])
            self.nodes[f'T{name_node_to}'].add_parent(self.nodes['T' + str(id)])

    def __repr__(self):
        return f'Graph with {len(self.nodes)} nodes and {len(self.edges)} edges'

    def get_spanning_tree(self):
        tree = copy.deepcopy(self)
        visited_nodes = []
        edges_to_remove = []
        for key, node in tree.nodes.items():
            for child in node.children:
                if child not in visited_nodes:
                    visited_nodes.append(child)
                else:
                    try:
                        edges_to_remove.append(tree.edges[f'{node.name}_{child.name}'])
                    except KeyError:
                        pass
        for edge in edges_to_remove:
            tree.remove_connection(edge)
        return tree

    def dfs(self, starting_node: Node):
        visited_nodes = []
        stack_lifo = [starting_node]
        while stack_lifo:
            current_node = stack_lifo.pop()
            if current_node not in visited_nodes:
                visited_nodes.append(current_node)
                for child in current_node.children[::-1]:
                    if child not in stack_lifo:
                        stack_lifo.append(child)
        return visited_nodes

    def bfs(self, starting_node):
        visited_nodes = []
        queue_fifo = [starting_node]
        while queue_fifo:
            current_node = queue_fifo.pop(0)
            if current_node not in visited_nodes:
                visited_nodes.append(current_node)
                for child in current_node.children:
                    if child not in queue_fifo:
                        queue_fifo.append(child)
        return visited_nodes

    @staticmethod
    def print_graph(graph, name):
        print(f"{name}: with {len(graph.edges)} edges")
        for key, value in graph.nodes.items():
            print(f'{value}')
        print('')

    def has_cycle(self, starting_node: Node):
        visited_nodes = []
        stack_lifo = [starting_node]
        while stack_lifo:
            current_node = stack_lifo.pop()
            if current_node not in visited_nodes:
                visited_nodes.append(current_node)
                for child in current_node.children[::-1]:
                    if child not in stack_lifo:
                        stack_lifo.append(child)
            else:
                for child in current_node.children[::-1]:
                    if child in visited_nodes:
                        return True

        return False

    @staticmethod
    def edge_with_min_weight(edges):
        min_edge = edges[0]
        for edge in edges:
            if edge.weight < min_edge.weight:
                min_edge = edge

        return min_edge

    def mst_prim(self, start_node):
        mst_prim = Graph()
        visited_nodes = [start_node]
        chosen_edges = []
        edges = []
        current_node = start_node
        while len(visited_nodes) != len(self.nodes):
            edges.extend([self.edges[f'{current_node.name}_{child.name}'] for child in current_node.children])
            edges = [edge for edge in edges if edge.to_node not in visited_nodes]
            _edge = Graph.edge_with_min_weight(edges)
            chosen_edges.append(_edge)
            current_node = _edge.to_node
            visited_nodes.append(current_node)
        for node in visited_nodes:
            mst_prim.add_node(node)
        for edge in chosen_edges:
            mst_prim.connect_nodes(edge.from_node, edge.to_node, edge.weight)
        return mst_prim

    def mst_kruskal(self, start_node):
        mst_kruskal = Graph()
        visited_nodes = [start_node]
        chosen_edges = []
        sorted_edges = sorted(self.edges, key=lambda e: self.edges[e].weight)
        sorted_edges.reverse()
        while len(visited_nodes) != len(self.nodes):
            current_edge = sorted_edges.pop()
            if not self.edges[current_edge].to_node in visited_nodes:
                visited_nodes.append(self.edges[current_edge].to_node)
                chosen_edges.append(self.edges[current_edge])
        for node in visited_nodes:
            mst_kruskal.add_node(node)
        for edge in chosen_edges:
            mst_kruskal.connect_nodes(edge.from_node, edge.to_node, edge.weight)
        return mst_kruskal

    def get_path_time(self, path) -> float:
        total_time = 0.0
        bw = self.get_bandwidth()
        prev = None
        for node in path:
            total_time += self.get_time(node)
            if prev:
                transmission_t = self.edges[f'{prev}_{node}'].weight / bw
                total_time += transmission_t
            prev = node

        return total_time

    def get_nodes_with_no_children(self):
        leafs = []
        for _name, _node in self.nodes.items():
            if not _node.children:
                leafs.append(_node)
        return leafs

    def dfs(self, starting_node: Node):
        visited_nodes = []
        stack_lifo = [starting_node]
        while stack_lifo:
            current_node = stack_lifo.pop()
            if current_node not in visited_nodes:
                visited_nodes.append(current_node)
                for child in current_node.children[::-1]:
                    if child not in stack_lifo:
                        stack_lifo.append(child)
        return visited_nodes

    def get_all_paths_in_graph(self, root_name=0):
        leafs = self.get_nodes_with_no_children()
        leafs = [l.name for l in leafs]
        all_paths = [[f'T{0}']]
        for _name, _node in self.nodes.items():
            for child in _node.children:
                for path in all_paths:
                    if self.nodes[path[-1]] in child.parents:
                        new_path = path[:]
                        new_path.append(child.name)
                        all_paths.append(new_path)
        # filter paths, so only ones with leaf at the and will stay
        out = [path for path in all_paths if path[-1] in leafs]
        out = [ele for ind, ele in enumerate(out) if ele not in out[:ind]]
        return out

    def cpm(self, start_node_nr=0):
        node_order = []
        paths = self.get_all_paths_in_graph()
        # paths = [['T0','T2'], ['T0','T3'],....]
        times_paths = [[self.get_path_time(path), path] for path in paths]
        while len(node_order) != len(self.nodes):
            critical_time_path = times_paths[0]
            for time_path in times_paths:
                if time_path[0] > critical_time_path[0]:
                    critical_time_path = time_path
            task = critical_time_path[1][0]
            node_order.append(task)
            time = self.get_time(task)
            times_paths = self.remove_task_from_times_paths(times_paths, task, time)
            times_paths = [tp for tp in times_paths if tp[1]]
        return node_order

    def remove_task_from_times_paths(self, times_paths, task, time):
        reduced_times_paths = []
        for time_path in times_paths:
            if time_path[1][0] == task:
                reduced_times_paths.append([time_path[0] - time, time_path[1][1:]])
            else:
                reduced_times_paths.append([time_path[0], time_path[1]])
        return reduced_times_paths

    def parse_row_to_proc(self, row, i):
        pass

    def parse_row_to_cost(self, row, i):
        pass

    def parse_row_to_times(self, row, i):
        times = row.split(' ')
        self.nodes[f'T{i}'].set_times(times)

    def parse_row_to_comm(self, row, i):
        comm = row.split(' ')
        self.comms.append(comm)

    def get_bandwidth(self, nr_of_channel=0):
        pos_of_bandwidth = 2
        return float(self.comms[nr_of_channel][pos_of_bandwidth])

    def get_time(self, node_name, proc=0):
        return float(self.nodes[node_name].times[proc])

    def dijkstra(self, starting_node='T0'):
        @dataclass
        class DijPath:
            id: int
            isVisited: bool
            min_weight: int
            previous_id: int

        min_paths = [DijPath(i, False, 0, -1) for i, (_, node) in enumerate(self.nodes.items())]

        current_node = 0
        for i in range(len(self.nodes.keys())-1):
            min_paths[current_node].isVisited = True
            for child in self.nodes[f'T{current_node}'].children:
                _c_id = int(child.name[1:])
                edge_cost = self.edges[f'T{current_node}_T{_c_id}'].weight
                new_cost = edge_cost + min_paths[current_node].min_weight
                current_cost = min_paths[_c_id].min_weight
                if current_cost == 0 or new_cost < current_cost:
                    min_paths[_c_id].min_weight = new_cost
                    min_paths[_c_id].previous_id = current_node
            # select node with lowest cost of path
            not_visited = [p for p in min_paths if not p.isVisited and p.min_weight > 0]
            lowest = not_visited[0]
            for p in not_visited:
                if p.min_weight < lowest.min_weight:
                    lowest = p

            current_node = lowest.id

        return min_paths
