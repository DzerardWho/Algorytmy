from __future__ import annotations

import time
from typing import Callable, Dict, Iterable, Optional, Tuple, List, Type

from graphviz import Digraph

from .baseNode import BaseNode
from .node import Node


class Graph:
    nodeClass = Node

    def __init__(self):
        self.nodes: Dict[str, Type[BaseNode]] = {}

    def addNodes(
            self,
            data: Iterable[str or Tuple[str, str]]
    ) -> Graph:
        for i in data:
            self.addNode(i)
        return self

    def addNode(
            self,
            label: str or Tuple[str, str]
    ):
        if type(label) == tuple:
            self.nodes[label[1]] = self.nodeClass(label[0])
        else:
            self.nodes[label] = self.nodeClass(label)

    def getNode(self, idx: str) -> Type[BaseNode]:
        out = self.nodes.get(idx, None)
        if out is None:
            raise KeyError(f'Node with idx={idx} does not exist')
        return out

    __getitem__ = getNode

    def connectNode(self, idx: str, childIdx: str, weight: int = 0):
        self[idx].addChild(self[childIdx], weight)

    def connectNodeInternal(self, parent: Type[BaseNode], childIdx: str,
                            weight: int = 0):
        parent.addChild(self[childIdx], weight)

    def connectNodes(
            self,
            data: Dict[str, Iterable[str or Tuple[str, int]]]
    ):
        for k, v in data.items():
            node = self[k]
            for i in v:
                if type(i) == tuple:
                    self.connectNodeInternal(node, *i)
                else:
                    self.connectNodeInternal(node, i)

    def __str__(self) -> str:
        return '\n'.join([str(i) for i in self.nodes])

    def render(self, name: Optional[str] = None) -> str:
        graph = Digraph(name or f"graph_{time.strftime('%H.%M-%d.%m.%Y')}")
        nodes = self.breadthTraversal()
        for node in nodes:
            graph.node(node.interIdx, label=node.label)
        for node in nodes:
            internIdx = node.interIdx
            for child, weight in node.children.items():
                graph.edge(internIdx, child.interIdx, str(weight))
        graph.render(format='png')
        return graph.name

    @staticmethod
    def fromString(
            data: str,
            genIdx: Callable[[str], str] = None,
            parseEdgeData: Callable[[str], str or Tuple[str, int]] = None
    ) -> Graph:
        data = [i.strip() for i in data.split('\n')]
        nodes = []
        edges = {}
        for line in data:
            if line == '':
                continue
            label, _, *children = line.split()
            if parseEdgeData:
                children = [parseEdgeData(i) for i in children]
            else:
                children = [(i, 0) for i in children]
            if genIdx:
                label = (label, genIdx(label))
                edges[label[1]] = children
            else:
                edges[label] = children
            nodes.append(label)
        out = Graph()
        out.addNodes(nodes)
        out.connectNodes(edges)
        return out

    def depthTraversal(self) -> List[Type[BaseNode]]:
        out: List[Type[BaseNode]] = []
        stack: List[Type[BaseNode]] = []
        visitedNodes: List[Type[BaseNode]] = []

        for node in self.nodes.values():
            if node in visitedNodes:
                continue
            stack.append(node)
            visitedNodes.append(node)

            while len(stack):
                node = stack.pop()
                out.append(node)

                for childNode in reversed(node.children):
                    if childNode not in visitedNodes:
                        stack.append(childNode)
                        visitedNodes.append(childNode)
        return out

    def breadthTraversal(self) -> List[Type[BaseNode]]:
        out: List[Type[BaseNode]] = []
        queue: List[Type[BaseNode]] = []
        visitedNodes: List[Type[BaseNode]] = []

        for node in self.nodes.values():
            if node in visitedNodes:
                continue
            queue.append(node)
            visitedNodes.append(node)

            while len(queue):
                node = queue.pop(0)
                out.append(node)

                for childNode in reversed(node.children):
                    if childNode not in visitedNodes:
                        queue.append(childNode)
                        visitedNodes.append(childNode)
        return out

    @staticmethod
    def __isCycle(
        node: Type[BaseNode],
        visited: Dict[Type[BaseNode], bool],
        recursion: Dict[Type[BaseNode], bool]
    ) -> bool:
        visited[node] = True
        recursion[node] = True

        for child in node.children:
            if not visited[child]:
                if Graph.__isCycle(child, visited, recursion):
                    return True
            elif recursion[child]:
                return True
        recursion[node] = False
        return False

    def checkCycles(self) -> bool:
        nodes = self.nodes.values()
        recursion: Dict[Type[BaseNode], bool] = {i: False for i in nodes}
        visitedNodes: Dict[Type[BaseNode], bool] = recursion.copy()

        for node in nodes:
            if not visitedNodes[node] and \
                    Graph.__isCycle(node, visitedNodes, recursion):
                return True
        return False
