class Edge:
    def __init__(self, name, weight: int, from_node, to_node):
        self.name = name
        self.weight = weight
        self.from_node = from_node
        self.to_node = to_node

    def __repr__(self):
        return f'Edge {self.name} ({self.weight}), from {self.from_node.name} to {self.to_node.name}'
