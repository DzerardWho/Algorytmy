from __future__ import annotations

import time
from typing import Callable, Tuple
from random import choice

from .node import Node
from ..graph import Graph


class Tree(Graph):
    nodeClass = Node

    def __init__(self):
        super().__init__()

    def render(self, name: str = None) -> str:
        return super().render(
            name or f"tree_{time.strftime('%H.%M-%d.%m.%Y')}"
        )

    def swapSubtrees(self, other: Tree):
        def getIds(nodes):
            return {i.label: i for i in nodes}

        def removeNodes(tree, nodes):
            for i in nodes:
                tree.pop(i, None)

        def getRandomNode(nodes):
            if len(nodes) > 1:
                return nodes[choice(list(nodes.keys())[1:])]
            else:
                raise ValueError("Nie można użyć korzenia do zamiany")

        selfNode = getRandomNode(self.nodes)
        otherNode = getRandomNode(other.nodes)
        # selfNode = self['T0']
        # otherNode = other['T21']

        selfNewNodes = getIds(selfNode.collectChildren())
        otherNewNodes = getIds(otherNode.collectChildren())

        removeNodes(self.nodes, selfNewNodes)
        removeNodes(other.nodes, otherNewNodes)

        self.nodes.update(otherNewNodes)
        other.nodes.update(selfNewNodes)

        selfNode.swapParents(otherNode)

    @staticmethod
    def fromString(
            data: str,
            genIdx: Callable[[str], str] = None,
            parseEdgeData: Callable[[str], str or Tuple[str, int]] = None
    ) -> Tree:
        return Tree.fromGraph(Graph.fromString(data, genIdx, parseEdgeData))

    @staticmethod
    def fromGraph(graph: Graph) -> Tree:
        out = Tree()
        nodes = graph.breadthTraversal()
        for i in nodes:
            out.addNode(i.label)
        for i in nodes:
            parent = out[i.label]
            for node, weight in i.children.items():
                out.connectNodeInternal(parent, node.label, weight)
        return out
