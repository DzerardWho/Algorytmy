from __future__ import annotations

import time
from typing import Iterable, Optional, Sized
import re

import numpy as np
from graphviz import Digraph

from .node import Node


class Graph(Sized):
    def __init__(self, numOfNodes: int):
        if numOfNodes <= 0:
            raise ValueError("Graph needs at least one node.")

        self.nodes: Iterable[Node] = np.array(
            [Node(i) for i in range(numOfNodes)]
        )

    @staticmethod
    def __connectNodes(parent: Node, child: Node, weight: int):
        parent.addChild(child, weight)

    def connectNodes(self, parentIdx: int, childIdx: int, weight: int = 0):
        if parentIdx >= self.nodes.shape[0] or childIdx >= self.nodes.shape[0]:
            raise IndexError("Index out of range.")

        self.__connectNodes(*self.nodes[[parentIdx, childIdx]], weight)

    def __getitem__(self, index: int) -> Node:
        return self.nodes[index]

    def __iter__(self):
        # Można dodać własną implementację,
        # aby zablokować bezpośredni dostęp do self.nodes ???
        return iter(self.nodes)

    def __len__(self):
        return self.nodes.shape[0]

    def first(self):
        return self.nodes[0]

    def render(self, name: Optional[str] = None) -> str:
        graph = Digraph(name or f"graph_{time.strftime('%H.%M-%d.%m.%Y')}")
        for node in self.nodes:
            graph.node(node.interIdx, label=f'T{node.label}')
        for node in self.nodes:
            internIdx = node.interIdx
            for child, weight in node.children.items():
                graph.edge(internIdx, child.interIdx, str(weight))
        graph.render(format='png')
        return graph.name

    @classmethod
    def fromString(cls, data: str):
        header, data = data.split('\n', 1)
        tmp = header.split(' ')
        if not (len(tmp) == 2 or tmp[1].isdigit()):
            raise ValueError("'tasks' header must contain info about number "
                             "of nodes.")
        numOfNodes = int(tmp[1])
        rawData = data.splitlines()

        if len(rawData) != numOfNodes:
            raise ValueError("Incorrect number of nodes.")

        graph = cls(numOfNodes)
        edgeRegex = re.compile(r'(\d*)\(([+-]?\d*)\)')
        for i in rawData:
            parent, numOfConnections, *connections = i.split(' ')
            parent = int(parent[1:])
            numOfConnections = int(numOfConnections)
            if numOfConnections != len(connections):
                raise ValueError(f'Task T{parent}: incorrect number of '
                                 'connections')
            for i in connections:
                child, weight = edgeRegex.findall(i)[0]
                child, weight = int(child), int(weight)

                if child >= numOfNodes:
                    raise ValueError(f'Task T{parent}: index {child} out '
                                     'of range.')

                graph.connectNodes(parent, child, weight)

        return graph
