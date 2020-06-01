from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(order=True)
class Edge:
    parent: Node = field(compare=False)
    child: Node = field(compare=False)
    weight: int


class Node:
    def __init__(self, label: int):
        self.children: Dict[Node, int] = {}
        self.parents: Dict[Node, int] = {}
        self.label = label
        self.interIdx = str(id(self))

    def addChild(self, node: Node, weight: int = 0):
        self.children[node] = weight
        node.parents[self] = weight

    # nie mam pojęcia czy do czegoś się to przyda
    def removeChildren(
            self,
            label: int = None,
            child: Node = None
    ) -> int or None:
        if child is None:
            if label is None:
                return
            child = next(
                filter(lambda x: x.label == label, self.children),
                None
            )
        if child:
            child.parents.pop(self, None)
            return self.children.pop(child, None)

    def collectChildren(self) -> List[Node]:
        out = [self]
        for i in self.children:
            out.extend(i.collectChildren())
        return out

    def collectChildrenLabels(self) -> List[int]:
        return [i.label for i in self.collectChildren()]

    @property
    def edges(self) -> List[Edge]:
        return [Edge(self, k, v) for k, v in self.children.items()]

    def __str__(self):
        return f'T{self.label}'

    def __repr__(self):
        return f'T{self.label} {len(self.children)} ' \
               f'{" ".join([f"{k}({v})" for k, v in self.children.items()])}'

    def __getitem__(self, key: Node) -> int:
        return self.children[key]
