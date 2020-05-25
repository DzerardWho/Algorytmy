from __future__ import annotations

import time
from typing import Callable, Dict, List, Tuple

from .graph import Graph


class Tree(Graph):
    def __init__(
        self,
        data: Dict[str or Tuple[str, str], List[Tuple[str, str]]] = None
    ):
        super().__init__(data)
        self.usedNodes: List[str] = []

    def addNode(
        self,
        label: str or Tuple[str, str],
        neighbors: List[Tuple[str, str]]
    ) -> None:
        neighbors = [i for i in neighbors if i[0] not in self.usedNodes]
        self.usedNodes.extend([i[0] for i in neighbors])
        super().addNode(label, neighbors)

    def render(self, name: str = None) -> str:
        return super().render(
            name or f"tree_{time.strftime('%H.%M-%d.%m.%Y')}"
        )

    @staticmethod
    def fromGraph(graph: Graph) -> Tree:
        out = Tree()
        for node in graph.iterNodes():
            out.addNode((node.label, node.idx), node.neigbours)
        return out

    @staticmethod
    def fromString(
        data: str,
        genIdx: Callable[[str], str] = None,
        parseEdgeData: Callable[[str], str or Tuple[str, str]] = None
    ) -> Tree:
        return Tree.fromGraph(
            super(Tree, Tree).fromString(
                data, genIdx=genIdx,
                parseEdgeData=parseEdgeData
            )
        )
