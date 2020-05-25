class Node:

    def __init__(self, name):
        self.name = name
        self.children = []
        self.parents = []
        self.times = []

    def add_parent(self, node):
        self.parents.append(node)

    def add_child(self, node):
        self.children.append(node)

    def remove_child(self, node):
        self.children.remove(node)

    def remove_parent(self, node):
        self.parents.remove(node)

    def set_times(self, times):
        self.times = times

    def __repr__(self):
        return f'Node {self.name}, children: {[child.name for child in self.children]}'
