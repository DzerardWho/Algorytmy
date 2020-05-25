from __future__ import annotations

from typing import Dict

from .baseNode import BaseNode


class Node(BaseNode):
    def __init__(self, label: str):
        super().__init__(label)
        self.parents: Dict[Node, int] = {}

    def addChild(self, node: Node, weight: int = 0):
        super().addChild(node, weight)
        node.parents[self] = weight
