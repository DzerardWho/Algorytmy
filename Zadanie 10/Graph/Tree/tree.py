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

    @staticmethod
    def kruskal(graph: Graph) -> Tree:
        edges = []
        tree = Tree()

        labelToIdx = {}
        for k, v in graph.nodes.items():
            tree.addNode((v.label, k))
            labelToIdx[v.label] = k
            edges.extend(v.edges)

        edges.sort(key=lambda x: x[0])
        treeNodes = {
            i: tree[i] for i in graph.nodes
        }

        usedNodes = 0
        allNodes = len(treeNodes)

        for weight, parent, child in edges:
            child = treeNodes[labelToIdx[child.label]]
            if child.parent:
                continue

            parent = treeNodes[labelToIdx[parent.label]]
            if parent.root is child.root:
                continue

            parent.addChild(child, weight)
            usedNodes += 1

            if usedNodes == allNodes:
                break
        return tree

    @staticmethod
    def prim(graph: Graph) -> Tree:
        import heapq
        from dataclasses import dataclass, field

        @dataclass(order=True)
        class Edge:
            weight: int
            parent: str = field(compare=False)
            child: str = field(compare=False)

        labelToIdx = {v.label: k for k, v in graph.nodes.items()}
        treeNodes = {}
        tree = Tree()

        queue = []

        def addNodesToQueue(node):
            for edge in node.edges:
                heapq.heappush(queue, Edge(*edge))
            label = node.label
            idx = labelToIdx[label]
            n = tree.addNode((label, idx))
            treeNodes[idx] = n
            return n

        addNodesToQueue(graph.firstValue())

        usedNodesCount = 0
        allNodes = len(labelToIdx)

        while len(queue) or usedNodesCount == allNodes:
            edge = heapq.heappop(queue)
            child = edge.child

            if labelToIdx[child.label] in treeNodes:
                continue

            parent = treeNodes[labelToIdx[edge.parent.label]]
            parent.addChild(addNodesToQueue(child), edge.weight)

            usedNodesCount += 1
        return tree
